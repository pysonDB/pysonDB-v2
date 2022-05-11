import argparse
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    print('Still under construction')
    print(args)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
