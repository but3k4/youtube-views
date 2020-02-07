# youtube-views
Tool to increase YouTube views

## Requirements

This tool depends on python3 and uses some libraries. In order to install them, you can use pip:

```sh
$ pip3 install -r requirements.txt
```

## Usage
```sh
$ python3 bot.py --help
usage: bot.py [--visits VISITS] [--url URL] [--proxy PROXY] [--enable-tor]
              [-v] [-h]

Tool to increase YouTube views

Main Arguments:
  --visits VISITS  amount of visits per video, default: 1
  --url URL        YouTube video url
  --proxy PROXY    set the proxy server to be used. e.g: 127.0.0.1:8118
  --enable-tor     enable TOR support (You must have installed TOR at your
                   system)

Optional Arguments:
  -v, --verbose    show more output
  -h, --help       show this help message and exit
$
```

## Example
```sh
$ python3 bot.py --visits 2 --url https://www.youtube.com/watch?v=HAQQUDbuudY --verbose
```
