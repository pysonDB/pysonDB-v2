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


TEST_OUTPUT = \
    """id,age,name,place
219520953066905460,0,ad0,US
110180374400879352,1,ad1,US
224980674034561069,7,ad2,UK
"""


def test_tocsv(tmpdir):
    f1 = tmpdir.join('test.json')
    f2 = tmpdir.join('test.csv')
    f1.write(json.dumps(TEST_DATA))

    assert main(('tocsv', f1.strpath, '-o', f2.strpath)) == 0
    assert f2.read().replace('\n', '') == TEST_OUTPUT.replace('\n', '')
