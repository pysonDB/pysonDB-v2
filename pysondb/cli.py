import argparse
import json
from typing import Optional
from typing import Sequence

from pysondb import db
from pysondb.utils import migrate


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--info', action='store_true',
                        help='Get the pysondb version info and the JSON parser info')

    sub = parser.add_subparsers(dest='sub')
    migrate_cmd = sub.add_parser('migrate')
    migrate_cmd.add_argument(
        'old', help='the path to the db with the old schema')
    migrate_cmd.add_argument(
        'new', help='the path to the file to put the db with the new schema')
    migrate_cmd.add_argument('--indent', type=int,
                             default=4, help='set the indent of the output DB')

    args = parser.parse_args(argv)
    if args.info:
        print('PysonDB - 2.0.0')
        if db.UJSON:
            print("using 'ujson' JSON parser")
        else:
            print('using builtin JSON parser')
        return 0

    if args.sub == 'migrate':
        with open(args.old) as f:
            new_data = migrate(json.load(f))
        with open(args.new, 'w') as f:
            json.dump(new_data, f, indent=args.indent)
        return 0

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
