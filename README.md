# youtube-views
Tool to increase YouTube views

## Requirements

This tool depends on python3 and uses some libraries. In order to install them, you can use pip:

```sh
$ pip3 install -r requirements.txt
```

## Usage
```sh
$ python3 youtube.py --help
usage: youtube.py [--visits VISITS] [--url URL] [--proxy PROXY] [-v] [-h]

Tool to increase YouTube views

Main Arguments:
  --visits VISITS  amount of visits per video, default: 1
  --url URL        YouTube video url
  --proxy PROXY    Uses a specified proxy server, e.g: 127.0.0.1:8118

Optional Arguments:
  -v, --verbose    show more output
  -h, --help       show this help message and exit
$
```

## Example
```sh
$ python3 youtube.py --visits 2 --url https://www.youtube.com/watch?v=HAQQUDbuudY --verbose
```
