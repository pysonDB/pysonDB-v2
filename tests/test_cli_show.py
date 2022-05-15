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


SUCCESS_TEST_OUTPUT = \
    """+--------------------+-----+------+-------+
|         id         | age | name | place |
+--------------------+-----+------+-------+
| 219520953066905460 |  0  | ad0  |   US  |
| 110180374400879352 |  1  | ad1  |   US  |
| 224980674034561069 |  7  | ad2  |   UK  |
+--------------------+-----+------+-------+
"""


def test_cli_show(tmpdir, capsys):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))

    assert main(('show', f.strpath)) == 0
    cap, _ = capsys.readouterr()
    assert str(cap) == str(SUCCESS_TEST_OUTPUT)


def test_cli_show_no_prettytable_installed(tmpdir, mocker, capsys):
    f = tmpdir.join('test.json')
    f.write(json.dumps(TEST_DATA))
    mocker.patch('pysondb.utils.PRETTYTABLE', False)

    assert main(('show', f.strpath)) == 1
    cap, _ = capsys.readouterr()
    assert cap == 'install prettytable (pip3 install prettytable) to run the following command\n'


def test_cli_show_v1_db(tmpdir, mocker, capsys):
    f = tmpdir.join('test.json')
    f.write(json.dumps({'data': [{'name': 'ad', 'age': 1, 'id': 353634357}]}))
    assert main(('show', f.strpath)) == 1
    cap, _ = capsys.readouterr()
    assert cap == 'the DB must be a v2 DB, you can use the migrate command to the convert your DB\n'
