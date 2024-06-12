from ebooklib import epub
from markdownify import markdownify as md
from bs4 import BeautifulSoup
import os
import sys
from PIL import Image
from pix2tex.cli import LatexOCR


def epub_to_markdown(epub_file, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    book = epub.read_epub(epub_file)
    chapter_count = 1
    base_path = os.path.dirname(epub_file)
    
    for item in book.get_items():
        if isinstance(item, epub.EpubHtml):
            # Convert HTML content to Markdown
            chapter_title = item.get_name().strip().replace(".xhtml", "")
            for x in ['/', '_']:
                chapter_title = chapter_title.replace(x, '-')
            content = item.get_content()

            # Extract and save images
            soup = BeautifulSoup(content, 'html.parser')
            for img in soup.find_all('img'):
                img_src = img['src']
                try:
                    # Resolve the full path of the image
                    img_path = img_src.replace('../', '')
                    img_file = book.get_item_with_href(img_path)
                    if img_file is not None:
                        img_data = img_file.get_content()
                        img_name = os.path.basename(img_src)
                        
                        # Save image to the output directory
                        os.makedirs(f'{output_dir}/images', exist_ok=True)
                        img_output_path = os.path.join(f'{output_dir}/images', img_name)
                        with open(img_output_path, 'wb') as out_img_file:
                            out_img_file.write(img_data)
                        
                        # Update image src in the content
                        img['src'] = img_name
                    else:
                        print(f"Image file not found for: {img_src}")
                except Exception as e:
                    print(f"Error extracting images: {e} {img_src}")

            markdown_content = md(content)
            
            # Create output file name
            output_file = os.path.join(output_dir, f"{chapter_title}.md")
            
            # Write to the output file
            with open(output_file, "w") as file:
                file.write(markdown_content)
            
            chapter_count += 1

def convert_image_to_latex(image_path):
    img = Image.open(image_path)
    model = LatexOCR()
    return model(img)


if __name__ == "__main__":
    # Usage example
    epub_file = sys.argv[1]
    # epub_file = "input/book.epub"
    output_dir = f"output/{epub_file.split('/')[-1].replace('.epub', '')}-chapters"
    epub_to_markdown(epub_file, output_dir)

    # Convert images to LaTeX
    for img in os.listdir(f"{output_dir}/images"):
        img_path = f"{output_dir}/images/{img}"
        latex_code = convert_image_to_latex(img_path)
        print(f"Image: {img_path}\nLatex: {latex_code}\n")
