import json
import os
from typing import Any
import yaml


def path_of(*paths: str):
    return os.path.abspath(os.path.join(*paths))


def read_file(
    path: str,
    is_json: bool = False,
    is_yaml: bool = False,
):
    with open(path, mode='r', encoding='utf8') as f:
        if is_json:
            return json.load(f)
        elif is_yaml:
            return yaml.load(f, yaml.SafeLoader)
        else:
            return f.read()


def write_file(
    path: str,
    content: Any,
    is_json: bool = False,
    is_yaml: bool = False,
):
    with open(path, mode='w', encoding='utf8') as f:
        if is_json:
            json.dump(content, f, ensure_ascii=False)
        elif is_yaml:
            yaml.dump(content, f, yaml.SafeDumper, allow_unicode=True)
        else:
            f.write(content)
