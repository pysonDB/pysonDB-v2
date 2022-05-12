from pysondb.cli import main


def test_cli_info_ujson_exist(mocker, capsys):
    mocker.patch('pysondb.db.UJSON', True)

    assert main(('--info',)) == 0
    out, _ = capsys.readouterr()
    assert out == "PysonDB - 2.0.0\nusing 'ujson' JSON parser\n"


def test_cli_info_ujson_does_not_exist(mocker, capsys):
    mocker.patch('pysondb.db.UJSON', False)

    assert main(('--info',)) == 0
    out, _ = capsys.readouterr()
    assert out == 'PysonDB - 2.0.0\nusing builtin JSON parser\n'
