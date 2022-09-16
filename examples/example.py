# -*- coding: utf-8 -*-

import filefox

obj = {
    "name": "John",
    "age": 12,
}

filefox.write_json(obj, "json_data.json")
assert obj == filefox.read_json("json_data.json")

filefox.write_json(obj, "json_data.json.gz")
assert obj == filefox.read_json("json_data.json.gz")

filefox.write(obj, "json_data.json")
assert obj == filefox.read("json_data.json")

filefox.write(obj, "json_data.json.gz")
assert obj == filefox.read("json_data.json.gz")

filefox.write_json(
    obj, "json_data.json", file_kwargs={"mode": "w", "encoding": "utf8"}, indent=2
)
assert obj == filefox.read_json("json_data.json", file_kwargs={"encoding": "utf8"})
