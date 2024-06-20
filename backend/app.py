from flask import Flask, request, jsonify, send_file
from markdownify import markdownify as md
from transformers import AutoTokenizer
from firebase_admin import credentials
from firebase_admin import firestore
from pix2tex.cli import LatexOCR
from bs4 import BeautifulSoup
from ebooklib import epub
from PIL import Image
import firebase_admin
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


# you'll have to find a way to get the serviceAccountKey.json file if it's not in the same directory
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


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


def epub_to_markdown(epub_path, base_dir):
    book = epub.read_epub(epub_path)
    for item in book.get_items():
        if isinstance(item, epub.EpubHtml):
            section_title = item.get_id().strip().replace("_", "-")
            content = item.get_body_content()
            soup = BeautifulSoup(content, 'html.parser')
            markdown_content = md(str(soup))
            output_file = os.path.join(base_dir, 'markdown', f"{section_title}.md")
            with open(output_file, "w") as file:
                file.write(markdown_content)
        elif isinstance(item, epub.EpubImage):
            os.makedirs(os.path.join(base_dir, 'images'), exist_ok=True)
            image_path = os.path.join(base_dir, item.get_name())
            with open(image_path, 'wb') as file:
                file.write(item.get_content())


def markdown_to_flashcards(book_title, base_dir, model_id='llama3', num_ctx=8192):
    data = {'title': book_title, 'chapters': []}
    chapter_decks = []
    markdown_files = os.listdir(os.path.join(base_dir, 'markdown'))
    chapter_num = 1
    for file_name in markdown_files:
        # we have markdown files but some aren't chapters
        # doing some data analysis, chapters seem to follow a pattern
        # filenames might match c01.md, c02.md, etc. or chapter_01.md, chapter_02.md, etc. or chapter001.md, chapter002.md, etc.
        # lastly, all chapters character count is usually in the 50th percentile
        # so, if a filename contains the word 'chapter', ends with '.md', we can assume it's a chapter
        regex = re.compile(r'chapter', re.IGNORECASE)
        if not (regex.search(file_name) and file_name.endswith('.md')):
            continue
        chapter_num += 1
        with open(os.path.join(base_dir, 'markdown', file_name), 'r') as file:
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

                json.dump(data, open(f"{output_path.replace('.apkg', '.json')}", 'w'), indent=4)
                
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
        book_title = os.path.basename(file.filename).replace('.epub', '').lower().strip().replace(' ', '-')
        base_dir = os.path.join(OUTPUT_FOLDER, book_title)
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        dirs = {}
        for format in ['markdown', 'anki', 'json']:
            dir = os.path.join(base_dir, format)
            dirs[format] = dir
            os.makedirs(os.path.dirname(dir), exist_ok=True)
        try:
            epub_to_markdown(book_title, base_dir)
            markdown_to_flashcards(book_title, base_dir, model_id='llama3', num_ctx=8196)
            return send_file(os.path.join(OUTPUT_FOLDER, book_title, 'anki', f'{book_title}.apkg'), as_attachment=True)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400


if __name__ == "__main__":
    app.run(debug=True)