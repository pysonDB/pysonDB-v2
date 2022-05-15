from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

try:
    from prettytable import PrettyTable
    PRETTYTABLE = True
except ImportError:
    PRETTYTABLE = False


OldDataType = Dict[str, List[Dict[str, Any]]]
NewDataType = Dict[
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


def migrate(old_db_data: OldDataType) -> NewDataType:
    new_data: NewDataType = {'version': 2, 'keys': [], 'data': {}}

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


def print_db_as_table(data: NewDataType) -> Tuple[str, int]:
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
