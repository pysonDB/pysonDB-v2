import json

from pysondb.cli import main


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
            'age': 7,
            'place': 'UK'
        }
    }
}


def test_cli_purge(tmpdir):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))

    assert json.loads(f.read()) == TEST_DATA
    assert main(('purge', f.strpath)) == 0
    assert json.loads(f.read()) == {'version': 2, 'data': {}, 'keys': []}
