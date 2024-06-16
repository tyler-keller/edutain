# import os
# import sqlite3
# import json
# import zipfile
# from hashlib import sha1
# from datetime import datetime

# class APKG:
#     def __init__(self, config):
#         self.config = config
#         self.dest = os.path.join(os.path.dirname(__file__), config['name'])
#         self.clean()
#         os.makedirs(self.dest)
#         self.db = sqlite3.connect(os.path.join(self.dest, 'collection.anki2'))
#         self.deck = {**config, 'id': int(datetime.now().timestamp())}
#         self.init_database()
#         self.media_files = []

#     def add_card(self, card):
#         self.insert_card(card)

#     def add_media(self, filename, data):
#         index = len(self.media_files)
#         self.media_files.append(filename)
#         with open(os.path.join(self.dest, str(index)), 'wb') as f:
#             f.write(data)

#     def save(self, destination):
#         media_dict = {str(idx): file for idx, file in enumerate(self.media_files)}
#         with open(os.path.join(self.dest, 'media'), 'w') as f:
#             json.dump(media_dict, f)

#         with zipfile.ZipFile(os.path.join(destination, f"{self.config['name']}.apkg"), 'w') as zf:
#             for root, _, files in os.walk(self.dest):
#                 for file in files:
#                     zf.write(os.path.join(root, file), arcname=file)

#         self.clean()

#     def clean(self):
#         if os.path.exists(self.dest):
#             for root, _, files in os.walk(self.dest):
#                 for file in files:
#                     os.remove(os.path.join(root, file))
#             os.rmdir(self.dest)

#     def init_database(self):
#         deck_id = self.deck['id']
#         model_id = deck_id + 1
#         fields = [{'name': field, 'ord': idx} for idx, field in enumerate(self.deck['card']['fields'])]

#         conf = {
#             "nextPos": 1,
#             "estTimes": True,
#             "activeDecks": [1],
#             "sortType": "noteFld",
#             "timeLim": 0,
#             "sortBackwards": False,
#             "addToCur": True,
#             "curDeck": 1,
#             "newBury": True,
#             "newSpread": 0,
#             "dueCounts": True,
#             "curModel": model_id,
#             "collapseTime": 1200
#         }

#         models = {
#             model_id: {
#                 "vers": [],
#                 "name": self.deck['name'],
#                 "tags": [],
#                 "did": deck_id,
#                 "usn": -1,
#                 "req": [[0, 'all', [0]]],
#                 "flds": fields,
#                 "sortf": 0,
#                 "latexPre": (
#                     '\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n'
#                     '\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n'
#                     '\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n'
#                 ),
#                 "tmpls": [{
#                     "afmt": self.deck['card']['template']['answer'],
#                     "name": self.deck['name'],
#                     "qfmt": self.deck['card']['template']['question'],
#                     "did": None,
#                     "ord": 0,
#                     "bafmt": '',
#                     "bqfmt": ''
#                 }],
#                 "latexPost": '\\end{document}',
#                 "type": 0,
#                 "id": model_id,
#                 "css": self.deck['card'].get('styleText', '.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n'),
#                 "mod": int(datetime.now().timestamp())
#             }
#         }

#         decks = {
#             deck_id: {
#                 "mid": model_id,
#                 "name": self.deck['name'],
#                 "extendRev": 50,
#                 "usn": -1,
#                 "collapsed": False,
#                 "newToday": [1362, 0],
#                 "timeToday": [1362, 0],
#                 "dyn": 0,
#                 "extendNew": 10,
#                 "conf": 1,
#                 "revToday": [1362, 0],
#                 "lrnToday": [1362, 0],
#                 "id": deck_id,
#                 "mod": int(datetime.now().timestamp()),
#                 "desc": ''
#             }
#         }

#         sql = f"""
#         BEGIN TRANSACTION;
#         CREATE TABLE IF NOT EXISTS col (
#             id integer PRIMARY KEY,
#             crt integer NOT NULL,
#             mod integer NOT NULL,
#             scm integer NOT NULL,
#             ver integer NOT NULL,
#             dty integer NOT NULL,
#             usn integer NOT NULL,
#             ls integer NOT NULL,
#             conf text NOT NULL,
#             models text NOT NULL,
#             decks text NOT NULL,
#             dconf text NOT NULL,
#             tags text NOT NULL
#         );
#         INSERT INTO col VALUES (
#             1, 1401912000, {int(datetime.now().timestamp())}, {int(datetime.now().timestamp())}, 11, 0, 0, 0,
#             '{json.dumps(conf)}', '{json.dumps(models)}', '{json.dumps(decks)}', '{{}}', '{{}}'
#         );
#         CREATE TABLE IF NOT EXISTS cards (
#             id integer PRIMARY KEY,
#             nid integer NOT NULL,
#             did integer NOT NULL,
#             ord integer NOT NULL,
#             mod integer NOT NULL,
#             usn integer NOT NULL,
#             type integer NOT NULL,
#             queue integer NOT NULL,
#             due integer NOT NULL,
#             ivl integer NOT NULL,
#             factor integer NOT NULL,
#             reps integer NOT NULL,
#             lapses integer NOT NULL,
#             left integer NOT NULL,
#             odue integer NOT NULL,
#             odid integer NOT NULL,
#             flags integer NOT NULL,
#             data text NOT NULL
#         );
#         CREATE TABLE IF NOT EXISTS notes (
#             id integer PRIMARY KEY,
#             guid text NOT NULL,
#             mid integer NOT NULL,
#             mod integer NOT NULL,
#             usn integer NOT NULL,
#             tags text NOT NULL,
#             flds text NOT NULL,
#             sfld integer NOT NULL,
#             csum integer NOT NULL,
#             flags integer NOT NULL,
#             data text NOT NULL
#         );
#         CREATE TABLE IF NOT EXISTS graves (
#             usn integer NOT NULL,
#             oid integer NOT NULL,
#             type integer NOT NULL
#         );
#         CREATE TABLE IF NOT EXISTS revlog (
#             id integer PRIMARY KEY,
#             cid integer NOT NULL,
#             usn integer NOT NULL,
#             ease integer NOT NULL,
#             ivl integer NOT NULL,
#             lastIvl integer NOT NULL,
#             factor integer NOT NULL,
#             time integer NOT NULL,
#             type integer NOT NULL
#         );
#         CREATE INDEX IF NOT EXISTS ix_revlog_usn ON revlog (usn);
#         CREATE INDEX IF NOT EXISTS ix_revlog_cid ON revlog (cid);
#         CREATE INDEX IF NOT EXISTS ix_notes_usn ON notes (usn);
#         CREATE INDEX IF NOT EXISTS ix_notes_csum ON notes (csum);
#         CREATE INDEX IF NOT EXISTS ix_cards_usn ON cards (usn);
#         CREATE INDEX IF NOT EXISTS ix_cards_sched ON cards (did, queue, due);
#         CREATE INDEX IF NOT EXISTS ix_cards_nid ON cards (nid);
#         COMMIT;
#         """
#         self.db.executescript(sql)

#     def insert_card(self, card):
#         create_time = card.get('timestamp', int(datetime.now().timestamp()))
#         card_id = create_time
#         note_id = card_id + 1
#         model_id = self.deck['id'] + 1
#         fields_content = '\u001F'.join(card['content'])
#         sort_field = card['content'][0]
        
#         sql_card = """
#         INSERT INTO cards (id, nid, did, ord, mod, usn, type, queue, due, ivl, factor, reps, lapses, left, odue, odid, flags, data)
#         VALUES (?, ?, ?, 0, ?, -1, 0, 0, 86400, 0, 0, 0, 0, 0, 0, 0, 0, '');
#         """
#         self.db.execute(sql_card, (card_id, note_id, self.deck['id'], create_time))

#         sql_note = """
#         INSERT INTO notes (id, guid, mid, mod, usn, tags, flds, sfld, csum, flags, data)
#         VALUES (?, ?, ?, ?, -1, '', ?, ?, ?, 0, '');
#         """
#         self.db.execute(sql_note, (
#             note_id, str(card_id), model_id, create_time, fields_content,
#             sort_field, int(sha1(sort_field.encode()).hexdigest()[:8], 16)
#         ))
#         self.db.commit()


# if __name__ == "__main__":
#     # Example Usage
#     config = {
#         'name': 'MyDeck',
#         'card': {
#             'fields': ['Question', 'Answer'],
#             'template': {
#                 'question': '{{Question}}',
#                 'answer': '{{Answer}}'
#             },
#             'styleText': '.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n'
#         }
#     }

#     apkg = APKG(config)
#     card = {
#         'content': ['What is the capital of France?', 'Paris']
#     }
#     apkg.add_card(card)
#     apkg.save('./test-anki/')

