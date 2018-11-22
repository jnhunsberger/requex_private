#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''download.py - Downloads RequeX data sources to ../data/local/downloads/

'''

# Libraries
import os
import requests
import argparse
import json
from pprint import pprint


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
        description='Downloads datafiles from external (HTTP) sources and stores them in a local downloads directory.',
        prog='download_external'
        )

    parser.add_argument('config_file',
                        type=valid_filename,
                        metavar='CONFIG_FILE',
                        help="File path to the Requex configuration file. File must be in JSON format.")

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

    # HTTP SUCCESS STATUS CODE
    HTTP_SUCCESS = 200

    sources = config['external_data']
    print('Downloading the following sources:')
    pprint(sources)

    # set the path of the data storage location
    data_write_path = config['root_dir']+config['downloads_dir']

    # check to see if the download directory exists
    if not os.path.isdir(data_write_path):
        # directory does not exist, create it
        os.mkdir(data_write_path)

    # loop through each source location and write it to the downloads dir
    for source in sources:
        # extract the file name from the source path
        filename = os.path.basename(source)

        # download the file from the source
        r = requests.get(source)

        # verify that the request was successful
        if not r.status_code == HTTP_SUCCESS:
            print('failure: HTTP error {} for {}'.format(r.status_code, source))
            exit(1)
        else:
            print('success: {}'.format(source))

        # write the file to the data directory with the current date
        with open(data_write_path+filename, 'wb') as f:
            f.write(r.content)

        r = None

    print('Downloads complete!')


if __name__ == '__main__':
    run()
