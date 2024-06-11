from ebooklib import epub
from markdownify import markdownify as md
import os
import sys

def epub_to_markdown(epub_file, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    book = epub.read_epub(epub_file)
    chapter_count = 1
    
    for item in book.get_items():
        if isinstance(item, epub.EpubHtml):
            # Convert HTML content to Markdown
            chapter_title = item.get_name().strip().replace(".xhtml", "")
            for x in ['/', '_']:
                chapter_title = chapter_title.replace(x, '-')
            content = item.get_content()
            markdown_content = md(content)
            
            # Create output file name
            output_file = os.path.join(output_dir, f"{chapter_title}.md")
            
            # Write to the output file
            with open(output_file, "w") as file:
                file.write(markdown_content)
            
            chapter_count += 1

if __name__ == "__main__":
    # Usage example
    epub_file = sys.argv[1]
    # epub_file = "input/book.epub"
    output_dir = f"output/{epub_file.split('/')[-1].replace('.epub', '')}-chapters"
    epub_to_markdown(epub_file, output_dir)
