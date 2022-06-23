from typing import Any, Dict, List, Tuple, Union

from pysondb.db_types import DB_SCHEMA, SINGLE_DATA_TYPE

try:
    from prettytable import PrettyTable
    PRETTYTABLE = True
except ImportError:
    PRETTYTABLE = False


OLD_DATA_TYPE = Dict[str, List[Dict[str, Any]]]
NEW_DATA_TYPE = Dict[
    str,
    Union[
        int,
        str,
        List[str],
        Dict[
            str,
            Any
        ]
    ]
]


def migrate(old_db_data: OLD_DATA_TYPE) -> NEW_DATA_TYPE:
    new_data: NEW_DATA_TYPE = {'version': 2, 'keys': [], 'data': {}}

    if not old_db_data['data']:
        return new_data

    new_data['keys'] = list(old_db_data['data'][0].keys())
    if isinstance(new_data['keys'], list):
        new_data['keys'].remove('id')
    if isinstance(new_data['data'], dict):
        for d in old_db_data['data']:
            _id = str(d['id'])
            del d['id']
            new_data['data'][_id] = d

    return new_data


def print_db_as_table(data: NEW_DATA_TYPE) -> Tuple[str, int]:
    if not PRETTYTABLE:
        return 'install prettytable (pip3 install prettytable) to run the following command', 1
    if 'version' not in data:
        return 'the DB must be a v2 DB, you can use the migrate command to the convert your DB', 1

    if isinstance(data['keys'], list):
        keys = sorted(data['keys'])
        x = PrettyTable()
        x.field_names = ['id', *keys]
        if isinstance(data['data'], dict):
            for id, values in data['data'].items():
                x.add_row([id, *[values[i] for i in keys]])

            return x.get_string(), 0

    return '', 0


def merge_n_db(*dbs: DB_SCHEMA) -> Tuple[DB_SCHEMA, str, int]:
    keys: List[str] = []
    new_db: DB_SCHEMA = {}
    data: Dict[str, SINGLE_DATA_TYPE] = {}
    for db in dbs:
        if isinstance(db['keys'], list):
            if not keys:
                keys = db['keys']
            if db['keys'] != keys:
                return {}, 'All the DB\'s must have the same keys', 1

        if isinstance(db['data'], dict):
            data = {**data, **db['data']}

    new_db['version'] = 2
    new_db['keys'] = keys
    new_db['data'] = data
    return new_db, '', 0


def purge_db(_: Any) -> DB_SCHEMA:
    data: DB_SCHEMA = {'version': 2, 'keys': [], 'data': {}}
    return data
