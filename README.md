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

as a list of JSON objects, one per line like (without the surrounding `[]`):

```
{"artist": "Artist Name", "album": "Album Name", "track": "Track Name"}
{"artist": "Artist Name", "album": "Album Name", "track": "Track Name"}
{"artist": "Artist Name", "album": "Album Name", "track": "Track Name"}
```

...and then lets you pick one of those, and then saves it to a file.

If you don't select one of those, it'll just prompt you to manually enter each field

This is then combined into [HPI](https://github.com/purarue/HPI) listens in the `my.offline.listens` module

## Installation

Requires `python3.8+`

To install with pip, run:

```
pip install git+https://github.com/purarue/offline_listens
```

## Usage

```
Usage: offline_listens [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dump          dump listens
  listen        add a listen
  parse         parse an offline listens file
  update-cache  update cache file
```

By default this saves to `~/.local/share/offline_listens/listens.json`. You can override that by passing the filename to `listen`, or by setting the OFFLINE_LISTENS_FILE environment variable. That can be a `.json` or `.yaml` file, like:

```bash
export OFFLINE_LISTENS_FILE="${HOME}/Documents/listens.yaml"
```

To use this, you need to set the `OFFLINE_LISTENS_COMMANDS` environment variable to a list of commands (separated with `:`, like a `$PATH`) that generate JSON data in the format above.

When you run this for the first time, it runs that command and generates a cache at `~/.cache/offline-listens.json`, which is then used when you are asked to pick a song you just listened to. To update that cache, you can run `offline_listens update-cache`.

For my `OFFLINE_LISTENS_COMMANDS`, I use a single command, using my [listens](https://github.com/purarue/HPI-personal/blob/master/scripts/listens) script, with [a small wrapper](https://github.com/purarue/HPI-personal/blob/master/scripts/offline-listens-source) which removes the date/only returns unique songs

So my config just looks like:

```
export OFFLINE_LISTENS_COMMANDS='offline-listens-source'
```

If you don't have any sources, you could just create a script like this, which parses the offline listens file itself:

```bash
#!/usr/bin/env bash

python3 -m offline_listens parse | jq '.[] | del(.when)' -c | sort | uniq
```

To generate the correct JSON, I would recommend [`jq`](https://stedolan.github.io/jq/)

- To convert a list into a list of JSON objects, you can use `some-command-which-makes-json | jq '.[]'`
- To compress the JSON, you can use `some-command-which-makes-json | jq -c`

### Tests

```bash
git clone 'https://github.com/purarue/offline_listens'
cd ./offline_listens
pip install '.[testing]'
flake8 ./offline_listens
mypy ./offline_listens
```
