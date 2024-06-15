import re
import os
import sys
from ebooklib import epub
from markdownify import markdownify as md
from bs4 import BeautifulSoup
from PIL import Image
from pix2tex.cli import LatexOCR

def epub_to_markdown(epub_file, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    book = epub.read_epub(epub_file)
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
                        img['src'] = os.path.join('images', img_name)
                    else:
                        print(f"Image file not found for: {img_src}")
                except Exception as e:
                    print(f"Error extracting images: {e} {img_src}")

            markdown_content = md(str(soup))
            
            # Create output file name
            output_file = os.path.join(output_dir, f"{chapter_title}.md")
            
            # Write to the output file
            with open(output_file, "w") as file:
                file.write(markdown_content)

def convert_image_to_latex(image_path):
    img = Image.open(image_path)
    model = LatexOCR()
    return model(img)

def convert_markdown_images(markdown_file, latex_output_dir):
    # Ensure LaTeX output directory exists
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

    # Write the updated lines to the LaTeX output directory
    base_name = os.path.basename(markdown_file)
    latex_output_file = os.path.join(latex_output_dir, base_name)
    with open(latex_output_file, 'w') as file:
        file.writelines(lines)

if __name__ == "__main__":
    epub_file = sys.argv[1]

    if epub_file is None:
        print("Please provide the path to the EPUB file")
        sys.exit(1)
    elif epub_file == 'ALL':
        epub_files = [f"input/{f}" for f in os.listdir('input') if f.endswith('.epub')]
        for epub_file in epub_files:
            output_dir = f"output/{os.path.basename(epub_file).replace('.epub', '')}-chapters"
            epub_to_markdown(epub_file, output_dir)
            
            latex_output_dir = f"{output_dir}-latex"
            for md_file in os.listdir(output_dir):
                if 'chapter' in md_file.split('/')[-1]:
                    md_file_path = os.path.join(output_dir, md_file)
                    convert_markdown_images(md_file_path, latex_output_dir)
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
