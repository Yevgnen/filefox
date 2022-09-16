# -*- coding: utf-8 -*-

# See and run examples/example.py

import filefox

expected = {
    "name": "John",
    "age": 12,
}

assert expected == filefox.read_json("json_data.json")
assert expected == filefox.read_json("json_data.json.gz")
assert expected == filefox.read("json_data.json")
assert expected == filefox.read("json_data.json.gz")
