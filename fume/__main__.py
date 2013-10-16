#!/usr/bin/env python
"""
Fume, a smoketest tool.

Usage:
    fume.py <script_name>

"""

import requests
from docopt import docopt
import sys
from fume import Script

def main():
    arguments = docopt(__doc__)
    filename = arguments["<script_name>"]
    script = Script.parse_script(filename)
    script.run()

if __name__ == "__main__":
    main()
