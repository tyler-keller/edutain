import ebooklib
from ebooklib import epub

# Load the EPUB file
books = ['deep-learning.epub', 'intelligence.epub', 'quantum-algs.epub', 'breakthrough.epub']
# for book in books:

print(f'Processing {books[1]}:')
book = epub.read_epub(f"input/{books[2]}")

# Get all the items in the EPUB file
items = book.get_items()

# Iterate over the items and find the chapter title
for item in items:
    chapter_titles = []

    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        item_content = item.get_body_content().decode("utf-8")
        # item_content = item_content.replace('\n', '')
        print(item_content)
        # Extract chapter titles from the HTML content
        # start_index = 0
        # while True:
        #     chapter_title_index = item_content.find('<section epub:type="bodymatter chapter" title="', start_index)

        #     if chapter_title_index == -1:
        #         break

        #     # Extract the chapter title
        #     start_quote_index = chapter_title_index + len('<section epub:type="bodymatter chapter" title="')
        #     end_quote_index = item_content.find('"', start_quote_index)
        #     chapter_title = item_content[start_quote_index:end_quote_index]

        #     chapter_titles.append(chapter_title)
        #     start_index = end_quote_index

    for chapter_title in chapter_titles:
        print(f'Chapter Title: {chapter_title}')
    
    print()