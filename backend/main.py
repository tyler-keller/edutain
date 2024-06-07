from ebooklib import epub
from markdownify import markdownify as md

def epub_to_markdown(epub_file, output_file):
    book = epub.read_epub(epub_file)
    content = ""
    
    for item in book.get_items():
        if isinstance(item, epub.EpubHtml):
            content += str(item.get_content())
    
    markdown_content = md(content)
    
    with open(output_file, "w") as file:
        file.write(markdown_content)

# Usage example
epub_file = "input/book.epub"
output_file = "output/book.md"
epub_to_markdown(epub_file, output_file)