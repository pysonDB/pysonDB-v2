import json  # noqa: F401
from threading import Lock  # noqa: F401


try:
    import ujson  # noqa: F401
    UJSON = True
except ImportError:
    UJSON = False
