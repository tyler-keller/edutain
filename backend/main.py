import re
import os
import sys
from ebooklib import epub
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from PIL import Image
from pix2tex.cli import LatexOCR
import genanki
import random
from openai import OpenAI
import tiktoken

# flow:
# upload epub
# convert epub to markdown
# convert images to latex
# create anki deck from epub title and type
# query gpt-4o for flashcard content for each chapter
# create anki cards from gpt-4o content
# upload anki deck

def epub_to_markdown(epub_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    book = epub.read_epub(epub_file)
    base_path = os.path.dirname(epub_file)
    for item in book.get_items():
        if isinstance(item, epub.EpubHtml):
            chapter_title = item.get_name().strip().replace(".xhtml", "")
            for x in ['/', '_']:
                chapter_title = chapter_title.replace(x, '-')
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
            output_file = os.path.join(output_dir, f"{chapter_title}.md")
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

def create_anki_deck(deck_name, deck_description):
    deck = genanki.Deck(
            model_id=str([random.randint(0, 9) for _ in range(30)]), 
            name=deck_name, 
            description=deck_description
        )
    return deck

def create_flashcards(book_title, chapter_title, chapter_text, model_id='gpt-3.5-turbo'):
    model_to_context_map = {
        'gpt-3.5-turbo': 16384,
        'gpt-3.5-turbo-0125': 16384,
        'gpt-4-turbo': 128_000,
        'gpt-4o': 128_000,
    }
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    tokens = encoding.encode(chapter_text)
    num_tokens = len(tokens)
    chunk_size = model_to_context_map[model_id] - 2048
    split_tokens = [tokens[i:i+chunk_size] for i in range(0, num_tokens, chunk_size)]
    flashcard_data = []
    for i, token_chunk in enumerate(split_tokens):
        chapter_text = encoding.decode(token_chunk)
        client = OpenAI()
        completion = client.chat.completions.create(
        model=model_id,
        response_format="json",
        messages=[
            {'role': 'system', 'content': '''You are an AI assistant that summarizes book content into flashcards. 
            The user will give you pieces of the book in an unclean markdown format. You are to take those pieces, identify key topics and return the most important concepts in flashcard format. 
            Only output the formatted flashcards. Your responses should be in the following format:
            ```json
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
            ```
            '''},
            {'role': 'user', 'content': f'''# **Book**: {book_title}
            ## **Chapter**: {chapter_title}
            **Text ({i} of {len(split_tokens)})**: {chapter_text}'''},
        ]
        )
        flashcard_data.append(completion.choices[0].message['content'])
    print(f"Flashcard data: {flashcard_data}")
    return flashcard_data

def create_anki_notes(anki_deck):
    pass

if __name__ == "__main__":
    epub_file = sys.argv[1]
    if epub_file is None:
        print("Please provide the path to the EPUB file")
        sys.exit(1)
    elif not epub_file.endswith('.epub'):
        print("Please provide a valid EPUB file")
        sys.exit(1)
    else:
        output_dir = f"output/{os.path.basename(epub_file).replace('.epub', '')}-chapters"
        epub_to_markdown(epub_file, output_dir)
        latex_output_dir = f"{output_dir}-latex"
        for md_file in os.listdir(output_dir):
            md_file_path = os.path.join(output_dir, md_file)
            if 'chapter' in md_file_path.split('/')[-1]:
                convert_markdown_images(md_file_path, latex_output_dir)
        deck_name = os.path.basename(epub_file).replace('.epub', '')

        # create_flashcards("Deep Learning", "Chapter Title", "Chapter Text")
