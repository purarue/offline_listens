from pathlib import Path
import click


@click.group()
def main() -> None:
    pass


default_listens_file = (
    Path.home() / ".local" / "share" / "offline_listens" / "listens.json"
)


@main.command(short_help="add a listen")
@click.option("-n", "--now", is_flag=True, help="if true, sets the listen time to now")
@click.argument(
    "LISTENS_FILE",
    required=True,
    type=click.Path(path_type=Path),
    default=default_listens_file,
    envvar="OFFLINE_LISTENS_FILE",
)
def listen(now: bool, listens_file: Path) -> None:
    from .listens import prompt, Listen

    from autotui.shortcuts import load_from, dump_to

    picked = prompt(now)
    items = load_from(Listen, listens_file, allow_empty=True)
    items.append(picked)
    dump_to(items, listens_file)


@main.command(short_help="dump listens")
def dump() -> None:
    import json

    from .listens import fetch_listens

    for listen in fetch_listens():
        click.echo(
            json.dumps(
                {
                    "artist": listen.artist,
                    "album": listen.album,
                    "track": listen.track,
                }
            )
        )


if __name__ == "__main__":
    main(prog_name="offline_listens")
