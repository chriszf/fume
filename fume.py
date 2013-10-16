#!/usr/bin/env python
"""
Fume, a smoketest tool.

Usage:
    fume.py
"""

import requests
import docopt
import sys
from fume import Script

def main():
    filename = "sample1.fume"
    script = Script.parse_script(filename)
    script.run()

if __name__ == "__main__":
    main()
