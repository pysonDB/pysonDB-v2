### the readme will be filled later

## the possible schema

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

in the latest update the key will be a str,
and it does not need to be converted to a string to be used in JS apps.

### migrating v2

all the methods name are PEP8 complaint.
eg: addMany -> add_many so on and so forth.
