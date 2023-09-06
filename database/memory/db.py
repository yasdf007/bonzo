import json
import dataclasses

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)


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
            json.dump(self.db, out, indent=4, cls=EnhancedJSONEncoder)

        print('save before exit')


DictMemoryDB = DictMemoryDb()

import atexit
atexit.register(DictMemoryDB.save)