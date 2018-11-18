#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''extract.py - extracts all files from archives in ../data/local/downloads/
and deletes the original archives.
'''

# Libraries
import zipfile
import os

# TODO: Add ability to set the working directory as a command line parameter
# TODO: Add support for other types of archives, beyond just .zip


def run():
    # change the working directory to the downloads folder
    os.chdir('../data/local/downloads/')

    # unzip any .zip files in data/local/
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for file in files:
        filename, extension = os.path.splitext(file)
        if extension == '.zip':
            # extract the zip file
            zip_file = zipfile.ZipFile(file, 'r')
            zip_file.extractall('./')
            os.remove(file)


if __name__ == '__main__':
    run()
