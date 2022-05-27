import argparse
import csv
import json
import sys
from typing import Optional
from typing import Sequence

from pysondb import db
from pysondb.utils import merge_n_db
from pysondb.utils import migrate
from pysondb.utils import print_db_as_table
from pysondb.utils import purge_db

try:
    import ujson as json  # type:ignore  # noqa: F811
except ImportError:
    import json


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--info', action='store_true',
                        help='Get the pysondb version info and the JSON parser info')

    sub = parser.add_subparsers(dest='sub')
    migrate_cmd = sub.add_parser('migrate', help='convert a v1 DB to v2')
    migrate_cmd.add_argument(
        'old', help='the path to the db with the old schema')
    migrate_cmd.add_argument(
        'new', help='the path to the file to put the db with the new schema')
    migrate_cmd.add_argument('--indent', type=int,
                             default=4, help='set the indent of the output DB')
    show = sub.add_parser('show', help='Pretty print a DB')
    show.add_argument('db', help='the path to the db to print as a table')
    merge = sub.add_parser(
        'merge', help='merge two or more DB with the same keys')
    merge.add_argument('filenames', nargs='*')
    merge.add_argument('--output', '-o', required=True,
                       help='The name of the output JSON file.')
    to_csv = sub.add_parser('tocsv', help='convert the DB to a csv file')
    to_csv.add_argument('db_file', help='The DB file to convert to CSV')
    to_csv.add_argument(
        '--output', '-o', help='The name fo the output csv file')
    purge = sub.add_parser('purge', help='purge / empty the whole DB')
    purge.add_argument('db_file', help='The DB file to purge')

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

    if args.sub == 'show':
        with open(args.db) as f:
            content, code = print_db_as_table(json.load(f))
            print(content)
            return code

    if args.sub == 'merge':
        dbs_data = []
        for _file in args.filenames:
            with open(_file, encoding='utf-8') as f:
                dbs_data.append(json.load(f))
        new_db, op_string, err_code = merge_n_db(*dbs_data)
        if op_string and err_code:
            print(op_string, file=sys.stderr)
            return err_code

        else:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(new_db, f)
                print('DB\'s merged successfully')
                return err_code

    if args.sub == 'tocsv':
        with open(args.db_file, encoding='utf-8') as f:
            with open(args.output, 'w', encoding='utf-8') as o:
                csv_write = csv.writer(o)
                db_data = json.load(f)
                if isinstance(db_data['keys'], list):
                    keys = ['id'] + sorted(db_data['keys'])
                    csv_write.writerow(keys)
                if isinstance(db_data['data'], dict):
                    for k, v in db_data['data'].items():
                        csv_write.writerow([k, *[v[i] for i in keys[1:]]])
        return 0

    if args.sub == 'purge':
        with open(args.db_file, mode='w', encoding='utf-8') as f:
            new_p_data = purge_db({})
            json.dump(new_p_data, f)
        return 0
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
