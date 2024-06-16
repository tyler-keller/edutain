import genanki
import yaml
import random
import pprint

def open_yaml_file(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    return data

def create_anki_deck(deck_name, deck_description):
    deck = genanki.Deck(
            model_id=(''.join([random.randint(0, 9) for _ in range(30)])), 
            name=deck_name, 
            description=deck_description
        )
    return deck

def create_anki_notes(anki_deck):
    anki_deck.add_note(
        genanki.Note(
            model=anki_deck.model(),
            fields=['What is the capital of France?', 'Paris']
        )
    )

if __name__ == '__main__':
    data = open_yaml_file('output/deep-learning-anki/deep-learning-v1.yml')
    # deck = create_anki_deck(data['title'], data['deck_description'])
    # for datum in data:
    #     print(datum)
    pretty_data = pprint.pformat(data, compact=True)
    print(pretty_data)
    # print(data.get('title', 'No title found'))
    # deck_name = data['deck_name']
    # deck_description = data['deck_description']
    # deck = create_anki_deck(deck_name, deck_description)
    # create_anki_notes(deck)
    # genanki.Package(deck).write_to_file('output/deep-learning-chapters-latex/deep-learning-chapters.apkg')