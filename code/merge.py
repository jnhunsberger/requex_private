#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Libraries
import os
import sys
import re
import time
import pandas as pd
from datetime import datetime
from shutil import move


def get_file_type(filename):
    '''get_file_type: determines the type of file.

    returns: string: one of: 'bambanek_dga', 'umbrella'
    '''
    # current method is to use the first three letters of the file name
    prefix = filename[:3]
    if prefix == 'dga':
        return 'bambanek_dga'
    elif prefix == 'top':
        return 'umbrella'
    else:
        return 'unknown'


def get_file_list(path='.'):
    '''get_file_list: returns a list of the files at the given path.
    '''
    return [f for f in os.listdir(path) if os.path.isfile(path+f)]


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


def move_staging(src, dst):
    '''move_staging: moves all files from src to dst. Must be directories.
    '''
    # filenames to exclude from renaming
    exclude = ['.DS_Store', '__init__.py']

    # check to see if a directory for the current date exists
    if not os.path.isdir(dst):
        # directory does not exist, create it
        os.mkdir(dst)

    # TODO: what if there are already files in that directory?

    # copy files from downloads directory into processing
    files = get_file_list(src)

    for file in files:
        filename = os.path.basename(file)
        if filename in exclude:
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


def run():
    # constant
    MB = 1024 * 1024
    # change current working directory to the data directory
    downloads_path = '../data/local/downloads/'
    working_path = '../data/local/staging/'
    date = datetime.utcnow().strftime('%Y-%m-%d')

    move_staging(downloads_path, working_path)
    files = get_file_list(working_path)

    df_master = pd.DataFrame()

    for file in files:
        type = get_file_type(file)
        if type == 'bambanek_dga':
            df = prep_bambanek_dga(working_path+file, working_path)
        elif type == 'umbrella':
            df = prep_umbrella(working_path+file, working_path)
        else:
            pass
        df_master = merge_df(df, df_master, working_path)

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

    write_to_logfile('', 'dedup', dedup_time, memory, working_path)

    # Sort malware by number of domains in the dataset
    start_time = time.time()
    malware_counts = pd.DataFrame(
        df_master.groupby('malware')['domain'].nunique()
        )
    print('malware_counts headers: {}'.format(malware_counts.columns.values))
    malware_counts = malware_counts.sort_values(by=['domain'], ascending=False)
    end_time = time.time()
    count_time = end_time - start_time

    # calculate the memory footprint of the dataframe
    memory = sys.getsizeof(malware_counts)/MB

    write_to_logfile('', 'count', count_time, memory, working_path)

    # write merged dataset to a CSV file
    merged_filename = working_path+'merged-'+date+'.csv'
    df_master.to_csv(path_or_buf=merged_filename,
                     sep=',',
                     header=True,
                     index=False
                     )

    print('malware counts:\n{}'.format(malware_counts))


if __name__ == '__main__':
    run()
