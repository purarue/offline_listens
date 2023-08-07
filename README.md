# offline_listens

An offline listening history.

This lets me keep track of music I listen to when offline, or when its not possible to sync with my scrobbler to listenbrainz/last.fm or on my computer with mpv

This is very generic -- it accepts one or more commands that generate JSON data in the format:

```
{
  "artist": "Artist Name",
  "album": "Album Name",
  "track": "Track Name",
}
```

as a list of JSON like:

```
{"artist": "Artist Name", "album": "Album Name", "track": "Track Name"}
{"artist": "Artist Name", "album": "Album Name", "track": "Track Name"}
{"artist": "Artist Name", "album": "Album Name", "track": "Track Name"}
```

and then lets you pick one of those, and then saves it to a file.

This is then combined into [HPI](https://github.com/seanbreckenridge/HPI) listens in the `my.offline.listens` module

## Installation

Requires `python3.8+`

To install with pip, run:

```
pip install git+https://github.com/seanbreckenridge/offline_listens
```

## Usage

```
Usage: offline_listens [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dump          dump listens
  listen        add a listen
  update-cache  update cache file
```

To use this, you need to set the `OFFLINE_LISTENS_COMMANDS` environment variable to a list of commands (separated with `:`, like a `$PATH`) that generate JSON data in the format above.

When you run this for the first time, it runs that command and generates a cache at `~/.cache/offline-listens.json`, which is then used when you are asked to pick a song you just listened to. To update that cache, you can run `offline_listens update-cache`.

For my `OFFLINE_LISTENS_COMMANDS`, I use a single command, using my [listens](https://github.com/seanbreckenridge/HPI-personal/blob/master/scripts/listens) script, with [a small wrapper](https://github.com/seanbreckenridge/HPI-personal/blob/master/scripts/offline-listens-source) which removes the date/only returns unique songs

So my config just looks like:

```
export OFFLINE_LISTENS_COMMANDS='offline-listens-source'
```

### Tests

```bash
git clone 'https://github.com/seanbreckenridge/offline_listens'
cd ./offline_listens
pip install '.[testing]'
flake8 ./offline_listens
mypy ./offline_listens
```
