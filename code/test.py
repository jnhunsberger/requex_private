#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
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
        description='TBD',
        prog='TBD'
        )

    parser.add_argument('config_file',
                        type=valid_filename,
                        metavar='CONFIG_FILE',
                        help="File path to requex configuration file. File must be in JSON format.")

    return vars(parser.parse_args())


def get_config(filename):
    '''get_config: reads the configuration JSON file and stores values in a dictionary for processing.

    PRE: assumes the file already exists

    return: dict of configuration settings
    '''

    with open(filename, "r") as f:
        config = json.load(f)

    return config


def main():
    args = parse_args()
    config = get_config(args['config_file'])
    print('configuration settings:')
    pprint(config)


if __name__ == '__main__':
    main()
