import base64
import csv
import hashlib
import io
import os
from collections import namedtuple

from shell import ShellError

KINDS = ("dir", "file")
DEFAULT_OWNER = "root"
Node = namedtuple("Node", "kind data owner")


class Vfs:
    def __init__(self, name="vfs", data=b"", nodes=None):
        self.name = name
        self.sha256 = hashlib.sha256(data).hexdigest()
        self.nodes = {"/": Node("dir", b"", DEFAULT_OWNER), **(nodes or {})}


def parse_row(row):
    kind = row["type"]
    if kind not in KINDS:
        raise ValueError(f"unknown type {kind!r}")
    content = base64.b64decode(row["content"] or "", validate=True)
    return row["path"], Node(kind, content, row.get("owner") or DEFAULT_OWNER)


def load(path):
    try:
        with open(path, "rb") as file:
            data = file.read()
        rows = csv.DictReader(io.StringIO(data.decode("utf-8")))
        nodes = dict(parse_row(row) for row in rows)
    except (OSError, ValueError, KeyError, csv.Error) as err:
        raise ShellError(f"vfs: cannot load {path}: {err}")
    return Vfs(os.path.basename(path), data, nodes)
