from typing import Any
from typing import Dict
from typing import List
from typing import Union


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
