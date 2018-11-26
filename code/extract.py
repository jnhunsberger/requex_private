#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''extract.py - extracts all files from archives in ../data/local/downloads/
and deletes the original archives.
'''

# Libraries
import os
import argparse
import json
from pprint import pprint
import zipfile


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
        description='Extracts files from archive formats.',
        prog='extract'
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

    # use the downloads directory for all actions
    downloads_dir = config['root_dir']+config['downloads_dir']

    # get a list of all files in the downloads directory
    files = [f for f in os.listdir(downloads_dir)
             if os.path.isfile(downloads_dir+f)]

    # extract each supported archive file to the downloads dir
    for file in files:
        filename, extension = os.path.splitext(file)
        # TODO: Add support for other types of archives, beyond just .zip
        if extension == '.zip':
            # extract the zip file
            zip_file = zipfile.ZipFile(downloads_dir+file, 'r')
            zip_file.extractall(downloads_dir)
            os.remove(downloads_dir+file)


if __name__ == '__main__':
    run()
