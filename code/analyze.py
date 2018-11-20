#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Libraries
import numpy as np
import pandas as pd
import time
import argparse


def parse_args():
    '''parse_args: parses command line arguments. Returns a dictionary of arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Runs analysis on pre-processed requex data csvs.',
        prog='analyze',
        )

    parser.add_argument('filename',
                        help="file path and name for the file to be analyzed.")

    return vars(parser.parse_args())


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

    # start_time = time.time()
    # malware_counts = df.groupby('malware')['domain'].nunique().reset_index()
    # malware_counts = malware_counts.sort_values('domain', ascending=False)
    # end_time = time.time()
    # method2 = end_time - start_time
    # print('malware counts method 2: {:>3.2}s\n{}'.format(method2, malware_counts))


def run():
    args = parse_args()
    filename = args['filename']
    if filename == '':
        print("ERROR: no filename given.")
        exit()

    print('entered filename: {}'.format(filename))

    working_path = '../data/local/staging/'

    df = pd.read_csv(working_path+filename,
                     sep=',',
                     header=0,
                     dtype={'dga': int, 'domain': str, 'malware': str},
                     parse_dates=[0],
                     engine='c')

    # dedup_analysis(df)
    malware_counts(df)


if __name__ == '__main__':
    run()
