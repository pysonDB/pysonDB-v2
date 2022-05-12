import json
from pathlib import Path

from pysondb.db import PysonDb
from pysondb.db_types import DBSchemaType


SAMPLE_DATA: DBSchemaType = {
    'version': 2,
    'keys': ['a', 'b', 'c'],
    'data': {
        '384753047545745': {
            'a': 1,
            'b': 'something',
            'c': True
        }
    }
}


def test_load(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(SAMPLE_DATA))

    db = PysonDb(f.strpath)
    assert db._load_file() == SAMPLE_DATA


def test_dump(tmpdir):
    f = tmpdir.join('test.py')

    db = PysonDb(f.strpath)
    db._dump_file(SAMPLE_DATA)
    assert f.read() == json.dumps(SAMPLE_DATA, indent=4)


def test_gen_file_file_exists(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(SAMPLE_DATA, indent=4))
    PysonDb(f)

    assert f.read() == json.dumps(SAMPLE_DATA, indent=4)


def test_gen_file_file_does_not_exist(tmp_path):
    filename = tmp_path / 'test.json'
    PysonDb(filename)

    assert Path(filename).is_file()
    assert filename.read_text() == json.dumps(
        {'version': 2, 'keys': [], 'data': {}}, indent=4)
