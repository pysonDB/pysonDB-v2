from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Union


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

Condition = Callable[[Dict[str, Any]], bool]
RetrunWithIdType = Dict[
    str, Dict[
        str, SimpleTypeGroup
    ]
]
