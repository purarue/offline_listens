from pathlib import Path
from typing import Iterator

import autotui.shortcuts

from .listens import Listen


def parse_file(file: Path) -> list[Listen]:
    return autotui.shortcuts.load_from(Listen, file)


def iter_dir(dir: Path) -> Iterator[Listen]:
    for file in dir.iterdir():
        if file.suffix == ".json" or file.suffix == ".yaml":
            yield from parse_file(file)
