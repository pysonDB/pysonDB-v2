from typing import Any
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
