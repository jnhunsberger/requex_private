#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''daily_archiver.py - Runs all the archiver scripts sequentially.

'''
import os
import argparse
import download_external
import extract
import rename
import archive


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
        description='Downloads the latest data from the Requex data sources, processes it, and stores it in the Requex archive.',
        prog='daily_archiver'
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

    print("------ Starting daily_archiver....")
    download_external.run(config_file)
    print("------ download_external finished.")
    print("------ extract started.")
    extract.run(config_file)
    print("------ extract finished.")
    print("------ rename started.")
    rename.run(config_file)
    print("------ rename finished.")
    print("------ archive started.")
    archive.run(config_file)
    print("------ archive finished.")

    print("Daily archiver complete.")


if __name__ == '__main__':
    run()
