#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''rename.py - adds a datestemp to all files that do not already have
one in '../data/local/downloads/'.
'''

# Libraries
import os
import re
from datetime import datetime

# TODO: add support for exclude list to be read from a configuration file.


def run():
    # filenames to exclude from renaming
    exclude = ['.DS_Store', '__init__.py']

    # TODO: allow working directory to be set as a command line parameter.
    # change the working directory to the downloads folder
    os.chdir('../data/local/downloads/')

    # retreive the current date (UTC)
    now = datetime.utcnow()
    date = now.strftime('%Y-%m-%d')

    # update all file names to include current date
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        filename, extension = os.path.splitext(file)

        if filename in exclude:
            continue

        # check for a datestamp in the filename
        found_date = re.search(r'\d\d\d\d-\d\d-\d\d|$', filename).group()
        if found_date == '':
            # no datestamp, append one
            os.rename(file, filename+'-'+date+extension)


if __name__ == '__main__':
    run()
