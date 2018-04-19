#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import os
import json
import sys
import logging
import tempfile
import subprocess

__version__ = '0.1'

PY3 = sys.version_info >= (3,)

if PY3:
    xrange = range

def main():
    process = subprocess.Popen(['curl -s http://10.8.0.18/current'], shell=True, stdout=subprocess.PIPE)
    process.wait()
    outputData = process.stdout.read()
    output = outputData.decode("utf-8") 
    data = output.split(":")
    print ("F1: " + data[1] + "A / F2: " + data[2] + "A / F3: " + data[3] + "A")

if __name__ == '__main__':
    main()
