import json
import uuid
from pathlib import Path
from threading import Lock


try:
    import ujson
    UJSON = True
except ImportError:
    UJSON = False

from pysondb.db_types import DBSchemaType


class PysonDb:

    def __init__(self, filename: str, thread_lock: bool = True) -> None:
        self.filename = filename
        self.thread_lock = thread_lock
        self.lock = Lock()

        self._gen_db_file()

    def _load_file(self) -> DBSchemaType:
        with open(self.filename, encoding='utf-8', mode='r') as f:
            if UJSON:
                return ujson.load(f)
            else:
                return json.load(f)

    def _dump_file(self, data: DBSchemaType) -> None:
        with open(self.filename, encoding='utf-8', mode='w') as f:
            if UJSON:
                ujson.dump(data, f, indent=4)
            else:
                json.dump(data, f, indent=4)
        return None

    def _gen_db_file(self) -> None:
        if not Path(self.filename).is_file():
            self.lock.acquire()
            self._dump_file(
                {'version': 2, 'keys': [], 'data': {}}
            )
            self.lock.release()

    def _gen_id(self) -> str:
        # generates a random 18 digit uuid
        return str(int(uuid.uuid4()))[:18]
