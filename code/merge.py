#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Libraries
import os
import sys
import re
import time
import argparse
import json
import pandas as pd
from datetime import datetime
from shutil import move


def get_file_type(filename, file_map):
    '''get_file_type: determines the type of file.

    returns: string: one of: 'bambanek_dga', 'umbrella'
    '''
    # current method is to use the first three letters of the file name
    basename = os.path.basename(filename)
    file_prefix = basename[:3]
    file_type = file_map.get(file_prefix)
    if file_type is not None:
        return file_type
    else:
        return 'unknown'


def get_file_list(directory):
    '''get_file_list: returns a list of the files at the given path.
    '''
    return [f for f in os.listdir(directory)
            if os.path.isfile(directory+f)]


def get_file_date(filename):
    '''get_file_date: extracts file date from file name. File date must be in YYYY-MM-DD format.

    returns: datetime object of file date.
    '''
    date = re.search(r'\d\d\d\d-\d\d-\d\d|$', filename).group()
    year, month, day = date.split('-')
    return datetime(int(year), int(month), int(day))


def write_to_logfile(datafile, filedate, time, memory, logpath, stdout=True):
    '''write_to_logfile: writes dataframe processing metadata to a logfile
    '''
    # constants
    logfile = 'requex_data_prep_log.log'

    # write to logfile
    stamp = datetime.utcnow().strftime('%Y-%m-%d-%H:%M')

    # extract the filename
    filename = os.path.basename(datafile)

    if stdout:
        print('{}, {:30}, {:<10}, {:>3.3f}s, {:>3.2f} MB'.format(
             stamp, filename, filedate, time, memory))

    with open(logpath+logfile, 'at') as log:
        log.write('{}, {}, {}, {:0.3f}, {:0.2f}\n'.format(
             stamp, filename, filedate, time, memory))


def move_staging(src, dst, exclusions=[]):
    '''move_staging: moves all files from src to dst. Must be directories. Exclusions is an optional parameter that allows for files with certain file names to be excluded from being moved.
    '''
    # filenames to exclude from renaming

    # check to see if a directory for the current date exists
    if not os.path.isdir(dst):
        # directory does not exist, create it
        os.mkdir(dst)

    # TODO: what if there are already files in that directory?

    # copy files from downloads directory into processing
    files = get_file_list(src)

    for file in files:
        filename = os.path.basename(file)
        if filename in exclusions:
            continue
        move(src+file, dst, copy_function='copy2')


def prep_bambanek_dga(datafile, logpath):
    '''prep_bambanek_dga: reads datafile in from disk

    Also, writes processing metadata to a logfile

    returns: dataframe of normalized data
    '''
    # constants
    MB = 1024*1024

    start_time = time.time()
    df = pd.read_csv(datafile,
                     sep=',',
                     header=16,
                     skip_blank_lines=True,
                     usecols=[0, 1, 2],
                     names=['domain', 'malware', 'date'],
                     dtype={0: str, 1: str},
                     parse_dates=[2],
                     engine='c')
    end_time = time.time()
    read_time = end_time - start_time

    # modify the malware column
    reg = re.compile(r'(^.*? )')
    prefix_len = len('Domain used by ')
    df['malware'] = df['malware'].str[prefix_len:]
    df['malware'] = df['malware'].str.extract(reg, expand=True)
    df['malware'] = df['malware'].str.lower()
    df['malware'] = df['malware'].str.strip()

    # add columns
    df['dga'] = 1
    filedate = get_file_date(datafile)
    df['date'] = filedate

    # calculate the memory footprint of the dataframe
    memory = sys.getsizeof(df)/MB

    # write to logfile
    write_to_logfile(datafile, filedate.strftime('%Y-%m-%d'), read_time, memory, logpath)

    return df


def prep_umbrella(datafile, logpath):
    '''prep_umbrella: reads datafile in from disk

    Also, writes processing metadata to a logfile

    returns: dataframe of normalized data
    '''
    # constants
    MB = 1024*1024

    start_time = time.time()
    df = pd.read_csv(datafile,
                     sep=',',
                     skip_blank_lines=True,
                     usecols=[1],
                     names=['domain'],
                     engine='c'
                     )
    end_time = time.time()
    read_time = end_time - start_time

    # add columns
    df['malware'] = 'NA'
    df['dga'] = 0
    filedate = get_file_date(datafile)
    df['date'] = filedate

    # calculate the memory footprint of the dataframe
    memory = sys.getsizeof(df)/MB

    # write to logfile
    write_to_logfile(datafile, filedate.strftime('%Y-%m-%d'), read_time, memory, logpath)

    return df


def merge_df(df_src, df_master, logpath):
    '''merge_df: append df_src into df_master

    Also, writes processing metadata to log file.

    returns: merged dataframe
    '''
    # constants
    MB = 1024*1024

    # merge dataframe into the master dataframe
    start_time = time.time()
    df_master = df_master.append(df_src, ignore_index=True)
    end_time = time.time()
    merge_time = end_time - start_time

    # calculate the memory footprint of the dataframe
    memory = sys.getsizeof(df_master)/MB

    # write to logfile
    write_to_logfile('', 'merge', merge_time, memory, logpath)

    return df_master


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
        description='Creates a merged Requex csv file that is ready for analysis or training. Moves any data files in the data downloads directory into a staging directory. The merged file is in the staging directory.',
        prog='marge'
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

    # constant
    MB = 1024 * 1024

    # use the downloads directory for all actions
    downloads_dir = config['root_dir']+config['downloads_dir']
    working_dir = config['root_dir']+config['staging_dir']

    date = datetime.utcnow().strftime('%Y-%m-%d')

    move_staging(downloads_dir, working_dir, config['excluded_files'])
    files = get_file_list(working_dir)

    df_master = pd.DataFrame()

    for file in files:
        type = get_file_type(file, config['file_map'])
        if type == 'bambanek':
            df = prep_bambanek_dga(working_dir+file, working_dir)
        elif type == 'umbrella':
            df = prep_umbrella(working_dir+file, working_dir)
        else:
            continue
        df_master = merge_df(df, df_master, working_dir)

    # deduplicate stats
    start_time = time.time()
    df_master = df_master.sort_values(
        by=['domain', 'date'],
        ascending=False
        ).drop_duplicates(['domain']).sort_index()
    end_time = time.time()
    dedup_time = end_time - start_time

    # calculate the memory footprint of the dataframe
    memory = sys.getsizeof(df_master)/MB

    write_to_logfile('', 'dedup', dedup_time, memory, working_dir)

    # Sort malware by number of domains in the dataset
    start_time = time.time()
    malware_counts = pd.DataFrame(
        df_master.groupby('malware')['domain'].nunique()
        )
    malware_counts = malware_counts.sort_values(by=['domain'], ascending=False)
    end_time = time.time()
    count_time = end_time - start_time

    # calculate the memory footprint of the dataframe
    memory = sys.getsizeof(malware_counts)/MB

    write_to_logfile('', 'count', count_time, memory, working_dir)

    # write merged dataset to a CSV file
    merged_filename = working_dir+'merged-'+date+'.csv'
    df_master.to_csv(path_or_buf=merged_filename,
                     sep=',',
                     header=True,
                     index=False
                     )

    print('malware counts:\n{}'.format(malware_counts))


if __name__ == '__main__':
    run()
