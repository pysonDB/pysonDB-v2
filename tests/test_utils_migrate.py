import json

from pysondb.utils import migrate


def test_migrate():
    with open('tests/test_utils_migrate/old_db.json') as f:
        old = json.load(f)

    with open('tests/test_utils_migrate/new_data.json') as f:
        new = json.load(f)

    assert migrate(old) == new


def test_migrate_empty_data():
    assert migrate({'data': []}) == {'version': 2, 'keys': [], 'data': {}}
