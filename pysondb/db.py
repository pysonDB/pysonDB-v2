import json
import uuid
from pathlib import Path
from threading import Lock
from typing import Union


try:
    import ujson
    UJSON = True
except ImportError:
    UJSON = False

from pysondb.db_types import Condition
from pysondb.db_types import DBSchemaType
from pysondb.db_types import SingleDataType
from pysondb.db_types import RetrunWithIdType
from pysondb.errors import IdDoesNotExistError
from pysondb.errors import SchemaTypeError
from pysondb.errors import UnknownKeyError


class PysonDB:

    def __init__(self, filename: str, auto_update: bool = True) -> None:
        self.filename = filename
        self.auto_update = auto_update
        self._au_memory = {'version': 2, 'keys': [], 'data': {}}
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

    def add(self, data: object) -> str:
        if not isinstance(data, dict):
            raise TypeError(f'data must be of type dict and not {type(data)}')

        with self.lock:
            db_data = self._load_file()

            keys = db_data['keys']
            if not isinstance(keys, list):
                raise SchemaTypeError(
                    f"keys must of type 'list' and not {type(keys)}")
            if len(keys) == 0:
                db_data['keys'] = sorted(list(data.keys()))
            else:
                if not sorted(keys) == sorted(data.keys()):
                    raise UnknownKeyError(
                        f'Unrecognized / missing key(s) {set(keys) ^ set(data.keys())}'
                        '(Either the key(s) does not exists in the DB or is missing in the given data)'
                    )

            _id = self._gen_id()
            if not isinstance(db_data['data'], dict):
                raise SchemaTypeError(
                    'data key in the db must be of type "dict"')

            db_data['data'][_id] = data
            self._dump_file(db_data)
            return _id

    def add_many(self, data: object, json_response: bool = False) -> Union[SingleDataType, None]:

        if not data:
            return None

        if not isinstance(data, list):
            raise TypeError(
                f'data must be of type "list" and not {type(data)}')

        if not all(isinstance(i, dict) for i in data):
            raise TypeError(
                'all the new data in the data list must of type dict')

        with self.lock:
            new_data: SingleDataType = {}
            db_data = self._load_file()

            # verify all the keys in all the dicts in the list are valid
            keys = db_data['keys']
            if not keys:
                db_data['keys'] = sorted(list(data[0].keys()))
                keys = db_data['keys']
            if not isinstance(keys, list):
                raise SchemaTypeError(
                    f"keys must of type 'list' and not {type(keys)}")

            for d in data:
                if not sorted(keys) == sorted(d.keys()):
                    raise UnknownKeyError(
                        f'Unrecognized / missing key(s) {set(keys) ^ set(d.keys())}'
                        '(Either the key(s) does not exists in the DB or is missing in the given data)'
                    )

            if not isinstance(db_data['data'], dict):
                raise SchemaTypeError(
                    'data key in the db must be of type "dict"')

            for d in data:
                _id = self._gen_id()
                db_data['data'][_id] = d
                if json_response:
                    new_data[_id] = d
            self._dump_file(db_data)

        return new_data if json_response else None

    def get_all(self) -> RetrunWithIdType:
        with self.lock:
            data = self._load_file()['data']
            if isinstance(data, dict):
                return data
        return {}

    def get_by_id(self, id: str) -> SingleDataType:
        if not isinstance(id, str):
            raise TypeError(
                f'id must be of type "str" and not {type(id)}')

        with self.lock:
            data = self._load_file()['data']
            if isinstance(data, dict):
                if id in data:
                    return data[id]
                else:
                    raise IdDoesNotExistError(
                        f'{id!r} does not exists in the DB')
            else:
                raise SchemaTypeError(
                    '"data" key in the DB must be of type dict')

    def get_by_query(self, condition: Condition) -> RetrunWithIdType:
        if not callable(condition):
            raise TypeError(
                f'"condition" must be of type callable and not {type(condition)!r}')

        with self.lock:
            new_data: RetrunWithIdType = {}
            data = self._load_file()['data']
            if isinstance(data, dict):
                for id, values in data.items():
                    if isinstance(values, dict):
                        if condition(values):
                            new_data[id] = values

            return new_data
