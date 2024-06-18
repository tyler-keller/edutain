import genanki
import yaml
import random
import os

def open_yaml_file(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    return data

def get_random_id():
    return int(''.join([str(random.randint(0, 9)) for _ in range(10)]))

def create_anki_deck(deck_name):
    deck = genanki.Deck(
            deck_id=get_random_id(),
            name=deck_name, 
        )
    return deck

def add_anki_notes(anki_deck, flashcards):
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

    for flashcard in flashcards:
        question = flashcard['question']
        answer = flashcard['answer']
        anki_deck.add_note(
            genanki.Note(
                model=qa_model,
                fields=[question, answer]
            )
        )
    
if __name__ == '__main__':
    dir = 'output/deep-learning-gemini'
    files = os.listdir(dir)
    for file in files:
        print(file)
        # data = open_yaml_file(f'{dir}/deep-learning-v1.yml')
        # deck_name = data['title']
        # chapters = data['chapters']
        # chapter_decks = []
        # for chapter in chapters:
        #     chapter_deck = create_anki_deck(f'{deck_name}' + '::' + f'Chapter-{chapter["chapter"]}')
        #     add_anki_notes(chapter_deck, chapter['questions'])
        #     chapter_decks.append(chapter_deck)
        # genanki.Package(chapter_decks).write_to_file('output/deep-learning-anki/deep-learning.apkg')

# f"{subdeck}::{str(index + 1).zfill(2)} {deck}"