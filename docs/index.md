# PysonDB-V2



## Quick walk through of all the methods

```python
from pysondb import PysonDB


db = PysonDB('test.json')
```

```python
!cat test.json
```

    {
        "version": 2,
        "keys": [],
        "data": {}
    }

## add

```py linenums="1"

id = db.add({
    'name': 'adwaith',
    'age': 4,
    'knows_python': True
})
print(id)

```

    231541323453553701

```python
!cat test.json
```

    {
        "version": 2,
        "keys": [
            "age",
            "knows_python",
            "name"
        ],
        "data": {
            "231541323453553701": {
                "name": "adwaith",
                "age": 4,
                "knows_python": true
            }
        }
    }

## add_many

```py linenums="1"
added_values = db.add_many([
    {
        'name': 'fredy',
        'age': 19,
        'knows_python': True
    },
    {
        'name': 'kenny',
        'age': 19,
        'knows_python': False
    }
])
print(added_values)
```

    None

```py linenums="1"
added_values = db.add_many([
    {
        'name': 'mathew',
        'age': 22,
        'knows_python': False
    },
    {
        'name': 'abi',
        'age': 19,
        'knows_python': True
    }
], json_response=True)
print(added_values)
```

    {'330993934764646664': {'name': 'mathew', 'age': 22, 'knows_python': False}, '131457970736078364': {'name': 'abi', 'age': 19, 'knows_python': True}}

```python
!cat test.json
```

    {
        "version": 2,
        "keys": [
            "age",
            "knows_python",
            "name"
        ],
        "data": {
            "231541323453553701": {
                "name": "adwaith",
                "age": 4,
                "knows_python": true
            },
            "263597723557497291": {
                "name": "fredy",
                "age": 19,
                "knows_python": true
            },
            "299482429835276227": {
                "name": "kenny",
                "age": 19,
                "knows_python": false
            },
            "330993934764646664": {
                "name": "mathew",
                "age": 22,
                "knows_python": false
            },
            "131457970736078364": {
                "name": "abi",
                "age": 19,
                "knows_python": true
            }
        }
    }

## get_by_id

```py linenums="1"
print(db.get_by_id('263597723557497291'))
```

    {'name': 'fredy', 'age': 19, 'knows_python': True}

## get_by_query

```py linenums="1"
def age_divisible_by_2(data):
    if data['age'] % 2 == 0:
        return True

print(db.get_by_query(query=age_divisible_by_2))
```

    {'231541323453553701': {'name': 'adwaith', 'age': 4, 'knows_python': True}, '330993934764646664': {'name': 'mathew', 'age': 22, 'knows_python': False}}

## get_all

```py linenums="1"
print(db.get_all())

```
```

{
   "231541323453553701":{
      "name":"adwaith",
      "age":4,
      "knows_python":true
   },
   "263597723557497291":{
      "name":"fredy",
      "age":19,
      "knows_python":true
   },
   "299482429835276227":{
      "name":"kenny",
      "age":19,
      "knows_python":false
   },
   "330993934764646664":{
      "name":"mathew",
      "age":22,
      "knows_python":false
   },
   "131457970736078364":{
      "name":"abi",
      "age":19,
      "knows_python":true
   }
}
```

## update_by_id

```py linenums="1"
updated_data = db.update_by_id('231541323453553701', {
    'age': 18
})
print(updated_data)
```

    {'name': 'adwaith', 'age': 18, 'knows_python': True}

## update_by_query

```py linenums="1"
updated_ids = db.update_by_query(
    query=lambda x: x['name'] == 'abi',
    new_data={'knows_python': False}
)
print(updated_ids)
```

    ['131457970736078364']

```py linenums="1"
!cat test.json
```

    {
        "version": 2,
        "keys": [
            "age",
            "knows_python",
            "name"
        ],
        "data": {
            "231541323453553701": {
                "name": "adwaith",
                "age": 18,
                "knows_python": true
            },
            "263597723557497291": {
                "name": "fredy",
                "age": 19,
                "knows_python": true
            },
            "299482429835276227": {
                "name": "kenny",
                "age": 19,
                "knows_python": false
            },
            "330993934764646664": {
                "name": "mathew",
                "age": 22,
                "knows_python": false
            },
            "131457970736078364": {
                "name": "abi",
                "age": 19,
                "knows_python": false
            }
        }
    }

## delete_by_id

```py linenums="1"
db.delete_by_id('131457970736078364')  # delete abi
```

```py linenums="1"
!cat test.json
```

    {
        "version": 2,
        "keys": [
            "age",
            "knows_python",
            "name"
        ],
        "data": {
            "231541323453553701": {
                "name": "adwaith",
                "age": 18,
                "knows_python": true
            },
            "263597723557497291": {
                "name": "fredy",
                "age": 19,
                "knows_python": true
            },
            "299482429835276227": {
                "name": "kenny",
                "age": 19,
                "knows_python": false
            },
            "330993934764646664": {
                "name": "mathew",
                "age": 22,
                "knows_python": false
            }
        }
    }

## delete_by_query

```py linenums="1"
ids = db.delete_by_query(lambda x: x['knows_python'] is False)
print(ids)
```

    ['299482429835276227', '330993934764646664']

```py linenums="1"
!cat test.json
```

    {
        "version": 2,
        "keys": [
            "age",
            "knows_python",
            "name"
        ],
        "data": {
            "231541323453553701": {
                "name": "adwaith",
                "age": 18,
                "knows_python": true
            },
            "263597723557497291": {
                "name": "fredy",
                "age": 19,
                "knows_python": true
            }
        }
    }

## purge

```py linenums="1"
db.purge()
```

```py linenums="1"
!cat test.json
```

    {
        "version": 2,
        "keys": [],
        "data": {}
    }

For more docs click [here](https://github.com/pysonDB/pysonDB-v2/tree/master/docs)
