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

To use this, you need to set the `OFFLINE_LISTENS_COMMANDS` environment variable to a list of commands (separated with `:`, like a `$PATH`) that generate JSON data in the format above.

```
offline_listens
```

### Tests

```bash
git clone 'https://github.com/seanbreckenridge/offline_listens'
cd ./offline_listens
pip install '.[testing]'
flake8 ./offline_listens
mypy ./offline_listens
```
