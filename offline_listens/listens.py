import os
import sys
import json
from pathlib import Path
from datetime import datetime

from typing import List, NamedTuple, Iterator, Generator, Dict, Any, Optional


class Source(NamedTuple):
    artist: str
    album: str
    track: str


class Listen(NamedTuple):
    artist: str
    track: str
    album: Optional[str]
    when: datetime


def fetch_commands() -> List[str]:
    """
    Feteches the commands from the OFFLINE_LISTENS_COMMANDS environment variable.
    """

    items = os.environ.get("OFFLINE_LISTENS_COMMANDS", "")
    cmds = [cmd for cmd in items.split(":") if cmd.strip()]
    if not cmds:
        print(
            "Warning: no commands found in OFFLINE_LISTENS_COMMANDS environment variable",
            file=sys.stderr,
        )
    return cmds


def yield_listens(command: str) -> Generator[Source, None, None]:
    """
    Yields listens from a command.
    """
    import shlex
    import shutil
    import subprocess

    if not command:
        return

    if len(shlex.split(command)) == 1:
        lookup = shutil.which(command)
        if lookup is None:
            print(f"Command {command} not found in $PATH", file=sys.stderr)
            return
        else:
            command = lookup

    command_str: List[str] = ["sh", "-c", command]

    process = subprocess.Popen(
        command_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    assert process.stdout is not None
    for line in process.stdout:
        try:
            listen: Dict[str, Any] = json.loads(line)
        except json.JSONDecodeError:
            print(f"Failed to parse JSON: {line.decode('utf-8')}", file=sys.stderr)
            continue
        yield Source(
            artist=listen["artist"],
            album=listen.get("album", None),
            # fetch from track or title
            track=listen.get("track", listen.get("title", "")),
        )


def fetch_listens() -> Iterator[Source]:
    for command in fetch_commands():
        if not command:
            print("Passed an empty command", file=sys.stderr)
            continue
        for listen in yield_listens(command):
            yield listen


HOME_DIR = Path.home()
CACHE_FILE = HOME_DIR / ".cache" / "offline-listens.json"


def read_cache() -> Iterator[Source]:
    if not os.path.exists(CACHE_FILE):
        yield from update_cache()
    else:
        with open(CACHE_FILE) as f:
            for line in f:
                listen = json.loads(line)
                yield Source(
                    artist=listen["artist"],
                    album=listen["album"],
                    track=listen["track"],
                )


def update_cache() -> List[Source]:
    """
    Updates the cache file.
    """
    listens = list(fetch_listens())
    if not CACHE_FILE.parent.exists():
        CACHE_FILE.parent.mkdir(parents=True)
    with open(CACHE_FILE, "w") as f:
        for listen in listens:
            json.dump(listen._asdict(), f, separators=(",", ":"))
            f.write("\n")
    return listens


def prompt(now: bool) -> Listen:
    import click
    from autotui.pick import pick_namedtuple
    from autotui.namedtuple_prompt import prompt_namedtuple

    picked = pick_namedtuple(read_cache())
    if picked is None:
        click.echo("No listen picked", err=True)
        return prompt_namedtuple(Listen)
    else:
        data: Dict[str, Any] = {
            "artist": picked.artist,
            "album": picked.album,
            "track": picked.track,
        }
        if now:
            data["when"] = datetime.now()
        nt = prompt_namedtuple(Listen, attr_use_values=data)
        return Listen(
            artist=nt.artist.strip(),
            album=nt.album.strip() if nt.album and nt.album.strip() else None,
            track=nt.track.strip(),
            when=nt.when,
        )
