import json
from copy import deepcopy
from typing import Any
from typing import Dict

import pytest

from pysondb.db import PysonDB
from pysondb.errors import IdDoesNotExistError


TEST_DATA = {
    'version': 2,
    'keys': [
        'age',
        'name',
        'place'
    ],
    'data': {
        '219520953066905460': {
            'name': 'ad0',
            'age': 0,
            'place': 'US'
        },
        '110180374400879352': {
            'name': 'ad1',
            'age': 1,
            'place': 'US'
        },
        '224980674034561069': {
            'name': 'ad2',
            'age': 74574654,
            'place': 'UK'
        },
        '228563587602913112': {
            'name': 'ad3',
            'age': 3,
            'place': 'UK'
        },
        '167833310760833974': {
            'name': 'ad4',
            'age': 4,
            'place': 'IN'
        }
    }
}


def test_delete_by_id(tmpdir):
    final_data: Dict[str, Any] = deepcopy(TEST_DATA)
    del final_data['data']['110180374400879352']

    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)

    db.delete_by_id('110180374400879352')
    assert json.loads(f.read()) == final_data


def test_delete_by_id_id_not_found_error(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    db = PysonDB(f.strpath)

    with pytest.raises(IdDoesNotExistError):
        db.delete_by_id('2345')
