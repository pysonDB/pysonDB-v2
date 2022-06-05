![data](https://raw.githubusercontent.com/pysonDB/pysonDB/master/images/file2son.png?token=APXKHAH6EDEJ7RUG3QOD2OC7ZHQZG)






## A Revamped version of PysonDB. New Schema and super fast.
 
 [![PyPI version](https://badge.fury.io/py/pysondb.svg)](https://pypi.org/project/pysondb/)
[![Downloads](https://pepy.tech/badge/pysondb/month)](https://pepy.tech/project/pysondb)
 [![CodeFactor](https://www.codefactor.io/repository/github/pysondb/pysondb/badge)](https://www.codefactor.io/repository/github/pysondb/pysondb)
 [![Discord](https://img.shields.io/discord/781486602778050590)](https://discord.gg/SZyk2dCgwg)
 ![GitHub Repo stars](https://img.shields.io/github/stars/pysonDB/pysonDB?style=plastic)
[![Downloads](https://static.pepy.tech/personalized-badge/pysondb?period=total&units=international_system&left_color=green&right_color=blue&left_text=Total%20Downloads)](https://pepy.tech/project/pysondb)
 
 ***
 

```python
pip install pysondb-v2
```
## The new DB schema

```json 

{
    "version": 2,
    "keys" ["a", "b", "c"],
    "data": {
        "384753047545745": {
            "a": 1,
            "b": "something",
            "c": true
        }
    }
}

```

## Features

* Much better than __PysonDB-V1__
* __Lightweight__ JSON based database.
* Supports __CRUD__ commands.
* No Database drivers required.
* __Unique ID__ assigned for each JSON document added.
* Strict about __Schema__ of data added. 
* __Inbuilt CLI__ to delete,display,create JSON database.


```py linenums="1"
from pysondb import PysonDB
db = PysonDB('test.json')

db.add({
    'name': 'adwaith',
    'age': 4,
    'knows_python': True
})

print(db.get_all())
{'231541323453553701': {'name': 'adwaith', 'age': 4, 'knows_python': True}}

```

* See its simple..
