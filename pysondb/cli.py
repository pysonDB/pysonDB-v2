import argparse
from typing import Optional
from typing import Sequence

from pysondb import db


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--info', action='store_true',
                        help='Get the pysondb version info and the JSON parser info')
    args = parser.parse_args(argv)

    if args.info:
        print('PysonDB - 2.0.0')
        if db.UJSON:
            print("using 'ujson' JSON parser")
        else:
            print('using builtin JSON parser')
        return 0

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
