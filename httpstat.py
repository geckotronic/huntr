#!/usr/bin/env python
# coding: utf-8
# References:
# man curl
# https://curl.haxx.se/libcurl/c/curl_easy_getinfo.html
# https://curl.haxx.se/libcurl/c/easy_getinfo_options.html
# http://blog.kenweiner.com/2014/11/http-request-timings-with-curl.html

from __future__ import print_function

import os
import json
import sys
import logging
import tempfile
import subprocess


__version__ = '1.2.1'


PY3 = sys.version_info >= (3,)

if PY3:
    xrange = range


# Env class is copied from https://github.com/reorx/getenv/blob/master/getenv.py
class Env(object):
    prefix = 'HTTPSTAT'
    _instances = []

    def __init__(self, key):
        self.key = key.format(prefix=self.prefix)
        Env._instances.append(self)

    def get(self, default=None):
        return os.environ.get(self.key, default)


ENV_SHOW_BODY = Env('{prefix}_SHOW_BODY')
ENV_SHOW_IP = Env('{prefix}_SHOW_IP')
ENV_SHOW_SPEED = Env('{prefix}_SHOW_SPEED')
ENV_SAVE_BODY = Env('{prefix}_SAVE_BODY')
ENV_CURL_BIN = Env('{prefix}_CURL_BIN')
ENV_DEBUG = Env('{prefix}_DEBUG')


curl_format = """{
"time_namelookup": %{time_namelookup},
"time_connect": %{time_connect},
"time_appconnect": %{time_appconnect},
"time_pretransfer": %{time_pretransfer},
"time_redirect": %{time_redirect},
"time_starttransfer": %{time_starttransfer},
"time_total": %{time_total},
"speed_download": %{speed_download},
"speed_upload": %{speed_upload},
"remote_ip": "%{remote_ip}",
"remote_port": "%{remote_port}",
"local_ip": "%{local_ip}",
"local_port": "%{local_port}"
}"""

https_template = """
  DNS Lookup   TCP Connection   TLS Handshake   Server Processing   Content Transfer
[   {a0000}  |     {a0001}    |    {a0002}    |      {a0003}      |      {a0004}     ]
             |                |               |                   |                  |
    namelookup:{b0000}        |               |                   |                  |
                        connect:{b0001}       |                   |                  |
                                    pretransfer:{b0002}           |                  |
                                                      starttransfer:{b0003}          |
                                                                                 total:{b0004}
"""[1:]

http_template = """
  DNS Lookup   TCP Connection   Server Processing   Content Transfer
[   {a0000}  |     {a0001}    |      {a0003}      |      {a0004}     ]
             |                |                   |                  |
    namelookup:{b0000}        |                   |                  |
                        connect:{b0001}           |                  |
                                      starttransfer:{b0003}          |
                                                                 total:{b0004}
"""[1:]


# Color code is copied from https://github.com/reorx/python-terminal-color/blob/master/color_simple.py
ISATTY = sys.stdout.isatty()


def make_color(code):
    def color_func(s):
        if not ISATTY:
            return s
        tpl = '\x1b[{}m{}\x1b[0m'
        return tpl.format(code, s)
    return color_func


red = make_color(31)
green = make_color(32)
yellow = make_color(33)
blue = make_color(34)
magenta = make_color(35)
cyan = make_color(36)

bold = make_color(1)
underline = make_color(4)

grayscale = {(i - 232): make_color('38;5;' + str(i)) for i in xrange(232, 256)}


def quit(s, code=0):
    if s is not None:
        print(s)
    sys.exit(code)


def print_help():
    help = """
Usage: httpstat URL [CURL_OPTIONS]
       httpstat -h | --help
       httpstat --version

Arguments:
  URL     url to request, could be with or without `http(s)://` prefix

Options:
  CURL_OPTIONS  any curl supported options, except for -w -D -o -S -s,
                which are already used internally.
  -h --help     show this screen.
  --version     show version.

Environments:
  HTTPSTAT_SHOW_BODY    Set to `true` to show response body in the output,
                        note that body length is limited to 1023 bytes, will be
                        truncated if exceeds. Default is `false`.
  HTTPSTAT_SHOW_IP      By default httpstat shows remote and local IP/port address.
                        Set to `false` to disable this feature. Default is `true`.
  HTTPSTAT_SHOW_SPEED   Set to `true` to show download and upload speed.
                        Default is `false`.
  HTTPSTAT_SAVE_BODY    By default httpstat stores body in a tmp file,
                        set to `false` to disable this feature. Default is `true`
  HTTPSTAT_CURL_BIN     Indicate the curl bin path to use. Default is `curl`
                        from current shell $PATH.
  HTTPSTAT_DEBUG        Set to `true` to see debugging logs. Default is `false`
"""[1:-1]
    print(help)


def main():
    process = subprocess.Popen(['curl -s http://10.8.0.18/current'], shell=True, stdout=subprocess.PIPE)
    process.wait()
    outputData = process.stdout.read()
    output = outputData.decode("utf-8") 
    data = output.split(":")
    print ("F1: " + data[1] + "A / F2: " + data[2] + "A / F3: " + data[3] + "A")


if __name__ == '__main__':
    main()
