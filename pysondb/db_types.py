from typing import Any, Callable, Dict, List, Union

DBSchemaType = Dict[
    str, Union[
        int,
        List[str],
        Dict[
            str, Any
        ]
    ]
]

SimpleTypeGroup = Union[int, str, bool]

SingleDataType = Dict[
    str, Union[
        int,
        str,
        bool,
        List[SimpleTypeGroup]
    ]
]

QueryType = Callable[[Dict[str, Any]], bool]
IdGeneratorType = Callable[[], str]
ReturnWithIdType = Dict[
    str, Dict[
        str, SimpleTypeGroup
    ]
]
NewKeyValidTypes = Union[List, Dict, str, int, bool]
