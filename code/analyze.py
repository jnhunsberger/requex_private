#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Libraries
import os
import json
import argparse
import pandas as pd
import time
from shutil import copy2


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
        description='Runs analysis on a pre-processed Requex data csv.',
        prog='analyze',
        )
    parser.add_argument('config_file',
                        type=valid_filename,
                        metavar='CONFIG_FILE',
                        help="File path to requex configuration file. File must be in JSON format.")
    parser.add_argument('filename',
                        metavar='FILE',
                        help="The file name for the file to be analyzed. The file must be in the staging directory.")

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


def get_file_list(directory):
    '''get_file_list: returns a list of the files at the given path.
    '''
    return [f for f in os.listdir(directory)
            if os.path.isfile(directory+f)]


def copy_analysis(src, dst):
    '''move_staging: copies the source file (src) to the dst directory. src must be a file and dst must be a directory. Exclusions is an optional parameter that allows for files with certain file names to be excluded from being moved.
    '''
    # check to see if a directory for the dst directory exists
    if not os.path.isdir(dst):
        # directory does not exist, create it
        os.mkdir(dst)

    # copy src file into destination directory
    if os.path.isfile(src):
        copy2(src, dst)
    else:
        print("The given file '{}' does not exist.".format(src))
        exit(1)


def factorize(df):
    # print('PRE-FACTORIZE ---------------------')
    # print(df.describe(include='all'))
    df['catIndex'], uniques = pd.factorize(df['malware'], sort=True)
    print('uniques: \n{}'.format(uniques))
    print('POST-FACTORIZE ---------------------')
    print(df.describe(include='all'))
    print('catIndex uniques: {}'.format(pd.unique(df['catIndex'].sort_values())))
    print('malware uniques: {}'.format(pd.unique(df['malware'].sort_values())))
    df_malicious = df.dropna(subset=['malware'])
    print('HEAD -------------------------------')
    print(df_malicious.head(n=50))
    print('TAIL -------------------------------')
    print(df_malicious.tail(n=50))


def dedup_analysis(df):
    print('PRE-DEDUPLICATION --------------------------')
    print(df.head(n=50))
    print(df.describe(include='all'))
    df = df.sort_values(by=['domain', 'date'],
                        ascending=False
                        ).drop_duplicates(['domain']).sort_index()
    print('POST-DEDUPLICATION -------------------------')
    print(df.head(n=50))
    print(df.describe(include='all'))


def malware_counts(df):
    start_time = time.time()
    malware_counts = pd.DataFrame(
        df.groupby('malware')['domain'].nunique()
        )
    malware_counts = malware_counts.sort_values(by=['domain'], ascending=False)
    end_time = time.time()
    method1 = end_time - start_time
    print('malware counts method 1: {:>3.2}s\n{}'.format(method1, malware_counts))


def run(config_file=None):
    # get configuration parameters
    config_file = get_config_filename(config_file)
    config = get_config(config_file)
    # print('configuration settings:')
    # pprint(config)

    # get the analysis directory
    analysis_dir = config['root_dir']+config['analysis_dir']
    staging_dir = config['root_dir']+config['staging_dir']

    # get the file to be analyzed
    args = parse_args()
    filename = args['filename']

    copy_analysis(staging_dir+filename, analysis_dir)

    print("File to be analyzed: '{}'".format(analysis_dir+filename))

    df = pd.read_csv(analysis_dir+filename,
                     sep=',',
                     header=0,
                     dtype={'dga': int, 'domain': str, 'malware': str},
                     parse_dates=[0],
                     engine='c')

    # dedup_analysis(df)
    malware_counts(df)
    # factorize(df)


if __name__ == '__main__':
    run()
