#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''rename.py - adds a datestemp to all files that do not already have
one in '../data/local/downloads/'.
'''

# Libraries
import os
import errno
import argparse
import json
from pprint import pprint
import re
from datetime import datetime


def valid_filename(filename):
    '''valid_filename: determines if the given filename is a real file. Assumes that the file is in the current working directory for the program.

    returns: given file name
    '''
    if not os.path.isfile(filename):
        msg = "The given file '{}' does not exist at '{}'.".format(
            filename,
            os.getcwd()
            )
        raise argparse.ArgumentTypeError(msg)

    return filename


def parse_args():
    '''parse_args: parses command line arguments. Returns a dictionary of arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Renames each file in the downloads directory to include the current YYYY-MM-DD datestamp at the end of the filename. For example: mydata.csv is converted to mydata-2018-11-21.csv.',
        prog='rename'
        )

    parser.add_argument('config_file',
                        type=valid_filename,
                        metavar='CONFIG_FILE',
                        help="File path to requex configuration file. File must be in JSON format.")

    return vars(parser.parse_args())


def get_config_filename(filename=None):
    '''get_config_filename: returns a verified Requex configuration file name. This function handles the ambiguity around whether the module was called from a shell with command line arguments or if called from another program using the run() function. If filename is none, the function assumes that there are

    return: string; valid filename.
    '''
    if filename is None:
        # get command line arguments
        args = parse_args()
        filename = args['config_file']
    else:
        if not os.path.isfile(filename):
            print("The given file '{}' does not exist at '{}'.".format(
                filename,
                os.getcwd()
                ))
            exit(1)
    return filename


def get_config(filename):
    '''get_config: reads the configuration JSON file and stores values in a dictionary for processing.

    PRE: assumes the file already exists

    return: dict of configuration settings
    '''

    with open(filename, "r") as f:
        config = json.load(f)

    return config


def run(config_file=None):
    # get configuration parameters
    config_file = get_config_filename(config_file)
    config = get_config(config_file)
    # print('configuration settings:')
    # pprint(config)

    # filenames to exclude from renaming
    exclude = config['excluded_files']

    # use the downloads directory for all actions
    downloads_dir = config['root_dir']+config['downloads_dir']

    # retreive the current date (UTC)
    now = datetime.utcnow()
    date = now.strftime('%Y-%m-%d')

    # get a list of all files in the downloads directory
    files = [f for f in os.listdir(downloads_dir)
             if os.path.isfile(downloads_dir+f)]

    # update all file names that do not already have a datestemp to
    # include the current date.
    for file in files:
        filename, extension = os.path.splitext(file)

        if filename in exclude:
            continue

        # check for a datestamp in the filename
        found_date = re.search(r'\d\d\d\d-\d\d-\d\d|$', filename).group()
        if found_date == '':
            # no datestamp, append one
            os.rename(downloads_dir+file, downloads_dir+filename+'-'+date+extension)


if __name__ == '__main__':
    run()
