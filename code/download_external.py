#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''download.py - Downloads RequeX data sources to ../data/local/downloads/

'''

# Libraries
import os
import requests


def run():
    # HTTP SUCCESS STATUS CODE
    HTTP_SUCCESS = 200

    # TODO: allow sources to be read from a configuration file.

    # list of sources
    sources = [
        'http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip',
        'http://osint.bambenekconsulting.com/feeds/dga-feed-high.csv'
    ]

    # TODO: allow the write path to be specified as a command line parameter.

    # set the path of the data storage location
    # assumes the code is in team_cyber/code/
    data_write_path = '../data/local/downloads/'

    # check to see if a directory for the current date exists
    if not os.path.isdir(data_write_path):
        # directory does not exist, create it
        os.mkdir(data_write_path)

    # loop through each source location and write it to the date-stamped dir
    for source in sources:
        # extract the file name from the source path
        filename = os.path.basename(source)

        # download the file from the source
        r = requests.get(source)

        # verify that the request was successful
        if not r.status_code == HTTP_SUCCESS:
            print('HTTP error {} for {}'.format(r.status_code, source))
            exit(1)
        else:
            print('success: {}'.format(source))

        # write the file to the data directory with the current date
        with open(data_write_path+filename, 'wb') as f:
            f.write(r.content)

        r = None


if __name__ == '__main__':
    run()
