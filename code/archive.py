#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''archive.py - uploads all files with approved file names from
'../data/local/downloads/' to Google Cloud Storage.

NOTE: if the files already exist in the archive, this script will overwrite
them. It is your responsibility to make sure you don't wipe out the archive.

'''

# Libraries
import os
import re
from datetime import datetime
from google.cloud import storage


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def create_dest_filename(file, date):
    '''create_dest_filename: takes the file name and assembles the correct
    file path in the archive for its storage location

    file: the full filename
    date: string of the date where the file is to be stored in
    YYYY-MM-DD format
    '''
    year, month, day = date.split('-')

    file_prefix = file[:3]
    if file_prefix == 'dga':
        return 'bambanek/'+year+'/'+month+'/'+day+'/'+file
    elif file_prefix == 'top':
        return 'umbrella/'+year+'/'+month+'/'+day+'/'+file
    else:
        return file


def get_file_list():
    return [f for f in os.listdir('.') if os.path.isfile(f)]


def run():
    # CONSTANTS
    # environment variable
    env_var = 'GOOGLE_APPLICATION_CREDENTIALS'

    # requex-svc file path for connecting to GCP storage bucket
    svc_path = "/Users/jnhunsberger/Documents/Personal/Academics/MIDS_Program/Classes/2018_W210_Capstone/team_cyber/code/requex-svc.json"

    # set the local environment variable
    os.environ[env_var] = svc_path

    # change the working directory to the downloads folder
    os.chdir('../data/local/downloads/')

    # filenames to exclude from renaming
    exclude = ['.DS_Store', '__init__.py']

    # approved file extensions
    approved = ['.csv', '.dat']

    # retreive the current date (UTC)
    # now = datetime.utcnow()
    # date = now.strftime('%Y-%m-%d')

    # MAIN
    # archive all file names that have a datestamp and approved extension
    files = get_file_list()

    for file in files:
        filename, extension = os.path.splitext(file)

        if filename in exclude:
            continue

        # only upload files with approved extensions and datestamps
        if extension in approved:
            # this makes sure a folder of files with different date stamps
            # get placed in the correct folder in the archive.
            found_date = re.search(r'\d\d\d\d-\d\d-\d\d|$', filename).group()
            if found_date != '':
                # file contains a date, archive it
                dest_file = create_dest_filename(file, found_date)
                upload_blob('requex_archives_raw', file, dest_file)


if __name__ == '__main__':
    run()
