from flask import Flask, request, jsonify, send_file
from markdownify import markdownify as md
from transformers import AutoTokenizer
from pix2tex.cli import LatexOCR
from bs4 import BeautifulSoup
from ebooklib import epub
from PIL import Image
import genanki
import ollama
import random
import json
import re
import sys
import os


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


system_message = '''
You are an AI assistant that summarizes book content into flashcards.
The user will give you pieces of the book in an unclean markdown format. 
You are to take those pieces, identify key topics and return the most important concepts in flashcard format.
Only output the formatted flashcards and their respective chapter title. 
Your responses should be in the following format:
```json
{
    "chapter": "Introduction",
    "cards":
    [
        {
            "front": "What is the capital of France?",
            "back": "Paris"
        },
        {
            "front": "What is the capital of Spain?",
            "back": "Madrid"
        }
    ]
}
```
'''


def epub_to_markdown(epub_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    book = epub.read_epub(epub_file)
    for item in book.get_items():
        if isinstance(item, epub.EpubHtml):
            section_title = item.get_name().strip().replace(".xhtml", "")
            for x in ['/', '_']:
                section_title = section_title.replace(x, '-')
            content = item.get_content()
            soup = BeautifulSoup(content, 'html.parser')
            for img in soup.find_all('img'):
                img_src = img['src']
                try:
                    img_path = img_src.replace('../', '')
                    img_file = book.get_item_with_href(img_path)
                    if img_file is not None:
                        img_data = img_file.get_content()
                        img_name = os.path.basename(img_src)
                        
                        os.makedirs(f'{output_dir}/images', exist_ok=True)
                        img_output_path = os.path.join(f'{output_dir}/images', img_name)
                        with open(img_output_path, 'wb') as out_img_file:
                            out_img_file.write(img_data)
                        img['src'] = os.path.join('images', img_name)
                    else:
                        print(f"Image file not found for: {img_src}")
                except Exception as e:
                    print(f"Error extracting images: {e} {img_src}")
            markdown_content = md(str(soup))
            output_file = os.path.join(output_dir, f"{section_title}.md")
            with open(output_file, "w") as file:
                file.write(markdown_content)


def convert_image_to_latex(image_path):
    img = Image.open(image_path)
    model = LatexOCR()
    return model(img)


def convert_markdown_images(markdown_file, latex_output_dir):
    print(f'Converting images in {markdown_file}')
    os.makedirs(latex_output_dir, exist_ok=True)
    img_pattern = re.compile(r"!\[.*\]\((.*[\.png|\.jpg])\)")
    with open(markdown_file, 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        match = img_pattern.search(line)
        if match:
            img_path = match.group(1)
            img_path = os.path.join(os.path.dirname(markdown_file), img_path)
            latex_code = convert_image_to_latex(img_path)
            print(f"Converted image to LaTeX: {img_path} -> {latex_code}")
            lines[i] = f"$\n{latex_code}\n$\n"
    base_name = os.path.basename(markdown_file)
    latex_output_file = os.path.join(latex_output_dir, base_name)
    with open(latex_output_file, 'w') as file:
        file.writelines(lines)


def get_random_id():
    return int(''.join([str(random.randint(0, 9)) for _ in range(10)]))


def create_anki_deck(deck_name):
    deck = genanki.Deck(
            deck_id=get_random_id(),
            name=deck_name, 
        )
    return deck


def add_anki_notes(anki_deck, cards):
    qa_model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[
            {'name': 'Question'},
            {'name': 'Answer'},
        ],
        templates=[
            {
            'name': 'Card',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            },
    ])
    for card in cards:
        question = card['front']
        answer = card['back']
        anki_deck.add_note(
            genanki.Note(
                model=qa_model,
                fields=[question, answer]
            )
        )


def markdown_to_flashcards(book_title, input_dir, output_path, model_id='llama3', num_ctx=8192):
    data = {'title': book_title, 'chapters': []}
    chapter_decks = []
    files = os.listdir(input_dir)
    
    chapter_num = 1
    for file_name in files:
        regex = re.compile(r'chapter', re.IGNORECASE)
        if not (regex.search(file_name) and file_name.endswith('.md')):
            continue
        chapter_num += 1
        with open(os.path.join(input_dir, file_name), 'r') as file:
            text = file.read()
        tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
        tokens = tokenizer.tokenize(text)
        num_tokens = len(tokens)
        if num_tokens > num_ctx:
            split_tokens = [tokens[i:i+(num_ctx-1024)] for i in range(0, num_tokens, (num_ctx-1024))]
            split_texts = [tokenizer.convert_tokens_to_string(split_token) for split_token in split_tokens]
        else:
            split_texts = [text]
        for chapter_text in split_texts:
            print(f"Processing chapter {chapter_num} with {len(chapter_text)} tokens")
            response = ollama.chat(
                model=model_id,
                messages=[
                    {'role': 'system', 'content': system_message},
                    {'role': 'user', 'content': f'''# **Book**: {book_title}
                    Chapter Text: {chapter_text}
                    '''},
                ],
                stream=False,
                options={
                    'temperature': 0,
                    'num_ctx': num_ctx,
                }
            )
            model_response = response['message']['content']
            json_match = re.search(r'```json([\s\S]*?)```', model_response)
            
            if json_match and json_match.group(1):
                json_content = json_match.group(1).strip()
                content_dict = json.loads(json_content)
                
                chapter_title = content_dict['chapter']
                chapter_cards = content_dict['cards']
                
                data['chapters'].append({
                    'chapter': chapter_title,
                    'cards': chapter_cards
                })
                
                chapter_deck = create_anki_deck(f'{book_title}::({chapter_num}) {chapter_title}')
                add_anki_notes(chapter_deck, chapter_cards)
                chapter_decks.append(chapter_deck)
                
                print(f"Created Anki deck for Chapter {chapter_title} with {len(chapter_cards)} cards")
    
    genanki.Package(chapter_decks).write_to_file(output_path)
    print(f"Successfully created Anki deck at {output_path}")


@app.route('/upload', methods=['POST'])
def upload_epub():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.epub'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        book_title = os.path.basename(file_path).replace('.epub', '')
        markdown_dir = os.path.join(OUTPUT_FOLDER, f"{book_title}-chapters")
        apkg_output_path = os.path.join(OUTPUT_FOLDER, f"{book_title}-anki/{book_title}.apkg")
        os.makedirs(os.path.dirname(apkg_output_path), exist_ok=True)
        try:
            epub_to_markdown(file_path, markdown_dir)
            markdown_to_flashcards(book_title, markdown_dir, apkg_output_path, model_id='llama3-gradient:latest', num_ctx=100_000)
            return send_file(apkg_output_path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400


if __name__ == "__main__":
    app.run(debug=True)