#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''download.py - Downloads RequeX data sources from the Requex GCP
archives to ../data/local/downloads/

'''

# Libraries
import os
import shlex
import re
import subprocess
import argparse
import pandas as pd     # for its handy date range functions
import dateutil         # for timezone support with pandas
from pprint import pprint
from datetime import datetime
from datetime import timedelta
from google.cloud import storage


def parse_args():
    '''parse_args: parses command line arguments. Returns a dictionary of arguements.
    '''
    parser = argparse.ArgumentParser(
        description='Downloads files from the Requex archive.',
        prog='download_archive',
        epilog='If more than one argument is given, the most specific is selected. For example if -t and -w are given, the program will be run with -t. The order of precedence is: today, yesterday, week, month, recent, date range(first/last).')

    parser.add_argument('-i', '--interactive', choices=['yes', 'no'],
                        default='yes',
                        help="Determines if the script is run in interactive mode. If omitted, the script runs interactively.")
    parser.add_argument('-t', '--today', action='store_true',
                        help="Downloads the data from today (if available).")
    parser.add_argument('-y', '--yesterday', action='store_true',
                        help='Downloads the data from yesterday.')
    parser.add_argument('-w', '--week', action='store_true',
                        help='Downloads the last 7 days of data.')
    parser.add_argument('-m', '--month', action='store_true',
                        help='Downloads the last 30 days of data.')
    parser.add_argument('-r', '--recent', action='store_true',
                        help='Downloads the most recent data. If run with no arguments, this is the default behavior of the program.')
    parser.add_argument('-f', '--first', metavar='YYYY-MM-DD',
                        help='The first date from which to pull archive data. Must be in the format: YYYY-MM-DD. If first is used, either -l or -m must be provided.')
    parser.add_argument('-l', '--last', metavar='YYYY-MM-DD',
                        help='The last date from which to pull archive data. Must be in the format: YYYY-MM-DD. If last is used, either -f or -m must be provided.')

    return vars(parser.parse_args())


def build_commands(args):
    '''build_commands: takes a dictionary of argument:value pairs and generates a list of GCP commands as a result
    '''
    commands = []
    dates = []
    format_str = '%Y-%m-%d'
    # get current UTC date
    now = datetime.utcnow()

    # parse the options and build a list of date tuples
    if args['today']:
        dates.append(tuple(now.strftime(format_str).split('-')))

    elif args['yesterday']:
        year, month, day = now.strftime(format_str).split('-')
        day = str(int(day)-1)
        dates.append((year, month, day))

    elif args['week']:
        # get the last seven days of dates
        dates = get_week_dates()

    elif args['month']:
        # get the last thirty days of dates
        dates = get_month_dates()

    elif args['recent']:
        # find the dates of the most recent uploads
        dates = find_recent()

    # order of these arguments matters!
    if args['first'] is not None:
        if args['last'] is not None:
            first = args['first']
            last = args['last']
            if evaluate_date(first) and evaluate_date(last):
                if compare_dates(first, last):
                    # get difference in dates
                    print('NOTICE: dates are valid.\nfirst: {} \nlast: {}'.format(first, last))
                    dates = get_date_range(first, last)
                else:
                    dates = []
                    print('ERROR: dates not valid. Must be in YYYY-MM-DD format; last must be at least 1 day ahead of first; and all dates must be greater or equal to January 1, 2000:\nfirst: {} \nlast: {}'.format(first, last))
            else:
                dates = []
                print('ERROR: dates not valid. Must be in YYYY-MM-DD format; last must be at least 1 day ahead of first; and all dates must be greater or equal to January 1, 2000:\nfirst: {} \nlast: {}'.format(first, last))
        else:
            dates = []
            print("ERROR: 'first' option given, but no 'last' given.")
    elif args['last'] is not None:
        dates = []
        print("ERROR: 'last' option given, but no 'first' given.")

    # loop through the constructed list of dates and build the GCP commands
    for d in dates:
        year, month, day = d
        commands.append(
            'gsutil ls -r gs://requex_archives_raw/**/'+year+'/'+month +
            '/'+day+'/**'
            )

    return commands


def evaluate_date(date):
    '''evaluate_date: takes a string and verifies that it is a legitimately formatted date. The valid format is YYYY-MM-DD with hyphens. Also, the date must be greater than January, 1, 2000.

    returns: bool, True=a valid date
    '''
    try:
        year, month, day = date.split('-')
        year = int(year)
        month = int(month)
        day = int(day)

        testdate = datetime(year, month, day)
        return testdate >= datetime(2000, 1, 1)

    except ValueError:
        return False


def compare_dates(first, last):
    '''compare_dates: compares the first date and the last date to make sure the last date is not the same as or before the first date. It is highly recommended to run evaluate_date() prior to using this function. This function does not check to see if the dates are valid.

    returns: bool, True=the end date is after the begin date
    '''
    # convert the strings into dates...
    year, month, day = first.split('-')
    first_date = datetime(int(year), int(month), int(day))

    year, month, day = last.split('-')
    last_date = datetime(int(year), int(month), int(day))

    return last_date > first_date


def get_date_range(first, last):
    '''get_date_range: returns a list of the dates starting with the first and ending with the last.

    returns: list of dates
    '''
    date_list = []

    # convert first and last to dates
    year, month, day = first.split('-')
    first_date = datetime(int(year), int(month), int(day))

    year, month, day = last.split('-')
    last_date = datetime(int(year), int(month), int(day))

    # calculate the difference in days; add 1 to get the last date
    days = (last_date - first_date).days + 1

    dates = pd.date_range(
        pd.Timestamp(first_date),
        periods=days,
        tz=dateutil.tz.tzutc()
        ).tolist()

    for d in dates:
        # create list of date tuples of (year, month, day)
        date_list.append(tuple(d.strftime('%Y-%m-%d').split('-')))

    return date_list


def get_week_dates():
    '''get_week_dates: returns a list of the dates for the last seven days. NOTE: does not include today.
    '''
    date_list = []

    start_date = datetime.today() - timedelta(days=7)

    dates = pd.date_range(
        pd.Timestamp(start_date),
        periods=7,
        tz=dateutil.tz.tzutc()
        ).tolist()

    for d in dates:
        # create list of date tuples of (year, month, day)
        date_list.append(tuple(d.strftime('%Y-%m-%d').split('-')))

    return date_list


def get_month_dates():
    '''get_month_dates: returns a list of the dates for the last 30 days.
    '''
    date_list = []

    start_date = datetime.today() - timedelta(days=30)

    dates = pd.date_range(
        pd.Timestamp(start_date),
        periods=30,
        tz=dateutil.tz.tzutc()
        ).tolist()

    for d in dates:
        # create list of date tuples of (year, month, day)
        date_list.append(tuple(d.strftime('%Y-%m-%d').split('-')))

    return date_list


def find_recent():
    '''find_recent: this function queries GCP for all the files in the archive and collects those that are the most up to date.

    returns: list of GCP file paths to the most recent files
    '''
    print("NOTICE: the recent option has not yet been implemented.")
    return []


def query_gcs(command, ext=None):
    '''query_gcs - queries the Requex Google Cloud Storage archive for
    a list of all files that match the given command and file extension.

    returns: a list of GCP files
    '''
    # use subprocess as gsutil has more capability than the python GCS API
    print('command: {}'.format(command))
    args = shlex.split(command)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    output, err = proc.communicate()
    proc_status = proc.wait()

    if output is not None:
        output = output.decode('utf-8').split('\n')
    if err is not None:
        err = err.decode('utf-8').split('\n')

    if ext is not None:
        files = [f for f in output if f[-len(ext):] == ext]
    else:
        # no file extension, show all files
        files = [f for f in output if len(f) > 0 and f[-1] not in ['/', ':']]

    for num, file in enumerate(files, start=1):
        print('{:>3}: {}'.format(num, file))

    print('command exit status: {}'.format(proc_status))

    return files


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))


def clean_filenames(files):
    '''clean_filenames: strips off the 'gs://requex_archives_raw/' prefix from the archive file listings.
    '''
    prefix = re.compile(r'^gs://requex_archives_raw/')
    return [prefix.sub('', f) for f in files]


def main():

    # set environment variable
    env_var = 'GOOGLE_APPLICATION_CREDENTIALS'

    # requex-svc file path for connecting to GCP storage bucket
    svc_path = "/Users/jnhunsberger/Documents/Personal/Academics/MIDS_Program/Classes/2018_W210_Capstone/team_cyber/code/requex-svc.json"

    # download destination path:
    # assumes the code is in team_cyber/code/
    data_write_path = '../data/local/downloads/'

    # set the local environment variable
    os.environ[env_var] = svc_path

    # get command line arguments
    args = parse_args()
    for arg, val in args.items():
        print("{:>12}: {}".format(arg, val))

    commands = build_commands(args)
    for num, command in enumerate(commands):
        print('{:>3}: {}'.format(num, command))

    # build file list
    files = []
    for command in commands:
        file_list = query_gcs(command)
        if file_list:
            files.append(file_list)

    # flatten the nested lists
    files = [f for nested in files for f in nested]

    if args['interactive'] == 'yes':
        if files:
            print()
            ans = input("Download all these files? [Y|[n]] ")
            if ans != 'Y':
                exit()
        else:
            exit()

    files = clean_filenames(files)

    pprint(files)
    for file in files:
        filename = os.path.basename(file)
        # print('file requested: {}'.format(file))
        # print('file downloaded: {}'.format(data_write_path+filename))
        # TODO: check to see if file already exists locally; if so, skip download
        download_blob('requex_archives_raw', file, data_write_path+filename)


if __name__ == '__main__':
    main()
