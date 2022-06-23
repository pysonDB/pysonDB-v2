from typing import Any, Callable, Dict, List, Union

DB_SCHEMA = Dict[
    str, Union[
        int,
        List[str],
        Dict[
            str, Any
        ]
    ]
]

SIMPLE_TYPE_GROUP = Union[int, str, bool]

SINGLE_DATA_TYPE = Dict[
    str, Union[
        int,
        str,
        bool,
        List[SIMPLE_TYPE_GROUP]
    ]
]

QUERY_TYPE = Callable[[Dict[str, Any]], bool]
ID_GENERATOR_TYPE = Callable[[], str]
RETURN_WITH_ID_TYPE = Dict[
    str, Dict[
        str, SIMPLE_TYPE_GROUP
    ]
]
NEW_KEY_VALID_TYPES = Union[List, Dict, str, int, bool]
