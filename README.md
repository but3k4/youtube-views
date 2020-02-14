# youtube-views

**NOTE:** If you want to use Tor, be aware that YouTube can flag your video and delete the views after a while.

---

Tool to increase YouTube views

## Requirements

This tool depends on python3 and uses some libraries. In order to install them, you can use pip:

```sh
$ sudo pip3 install -r requirements.txt
```

### Optional (Incomplete)

If you want, you can install tor and privoxy, once selenium does not work very well with socks proxy.

#### Install Tor and on Mac OS X

```sh
$ brew install tor
```

#### Install Tor on Debian

```sh
$ sudo apt-get update
$ sudo apt-get install tor
```

#### Install Tor on ArchLinux

```sh
$ sudo pacman -Sy tor
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
