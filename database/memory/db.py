import json


class DictMemoryDb:
    db = {}

    def __init__(self):
        try:
            with open('db.json', 'r') as db_file:
                self.db = json.load(db_file)
        except IOError:
            self.db = {}
        
    def save(self):
        with open('db.json', 'w') as out:
            json.dump(self.db, out, indent=4)

        print('save before exit')


DictMemoryDb = DictMemoryDb()

import atexit
atexit.register(DictMemoryDb.save)