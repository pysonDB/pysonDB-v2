import json

from pysondb.cli import main

TEST_DATA_1 = {
    'version': 2,
    'keys': ['test'],
    'data': {
        '211194894507061604': {
            'test': '3'
        },
        '107314111299174914': {
            'test': '4'
        }
    }
}


TEST_DATA_2 = {
    'version': 2,
    'keys': ['test'],
    'data': {
        '211194894507061605': {
            'test': '3'
        },
        '107314111299174916': {
            'test': '4'
        }
    }
}


TEST_DATA_ERR_KEYS = {
    'version': 2,
    'keys': ['age'],
    'data': {
        '211194894507061605': {
            'age': '3'
        },
        '107314111299174916': {
            'age': '4'
        }
    }
}

FINAL_DATA = {
    'version': 2,
    'keys': ['test'],
    'data': {
        '211194894507061604': {
            'test': '3'
        },
        '107314111299174914': {
            'test': '4'
        },
        '211194894507061605': {
            'test': '3'
        },
        '107314111299174916': {
            'test': '4'
        }
    }
}


def test_cli_merge(tmpdir, capsys):
    f1 = tmpdir.join('test1.json')
    f2 = tmpdir.join('test2.json')
    f3 = tmpdir.join('new_test.json')

    f1.write(json.dumps(TEST_DATA_1))
    f2.write(json.dumps(TEST_DATA_2))

    assert main(('merge', f1.strpath, f2.strpath, '-o', f3.strpath)) == 0
    cap, _ = capsys.readouterr()
    assert cap == "DB\'s merged successfully\n"
    assert json.loads(f3.read()) == FINAL_DATA


def test_cli_merge_key_mismatch(tmpdir, capsys):
    f1 = tmpdir.join('test1.json')
    f2 = tmpdir.join('test2.json')

    f1.write(json.dumps(TEST_DATA_1))
    f2.write(json.dumps(TEST_DATA_ERR_KEYS))

    assert main(('merge', f1.strpath, f2.strpath, '-o', 'test')) == 1
    cap, err = capsys.readouterr()
    assert err == "All the DB\'s must have the same keys\n"
    assert cap == ''
