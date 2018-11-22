#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''archive.py - uploads all files with approved file names from
'../data/local/downloads/' to Google Cloud Storage.

NOTE: if the files already exist in the archive, this script will overwrite
them. It is your responsibility to make sure you don't wipe out the archive.

'''

# Libraries
import os
import argparse
import json
from pprint import pprint
import re
from google.cloud import storage


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
        description='Archives data files to the Requex Google Cloud Storage archive.',
        prog='archive'
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


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('success: file {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def create_dest_filename(file, date, file_map):
    '''create_dest_filename: takes the file name, archive date, and a dictionary that contains a file map and assembles the correct
    file path in the archive for the file's storage location.

    file: the filename with extension, but without path
    date: string of the date where the file is to be stored in
    YYYY-MM-DD format
    file_map: dictionary of first three letters of a filename and the map to the root directory in the archive into which to store the file.

    returns: string; a gcs-formatted filename.
    '''
    year, month, day = date.split('-')

    basename = os.path.basename(file)
    file_prefix = basename[:3]
    archive_dir = file_map.get(file_prefix)

    if archive_dir is not None:
        return archive_dir+'/'+year+'/'+month+'/'+day+'/'+basename
    else:
        return basename


def get_file_list(directory):
    return [f for f in os.listdir(directory)
            if os.path.isfile(directory+f)]


def run(config_file=None):
    # get configuration parameters
    config_file = get_config_filename(config_file)
    config = get_config(config_file)
    # print('configuration settings:')
    # pprint(config)

    # environment variable
    env_var = 'GOOGLE_APPLICATION_CREDENTIALS'

    # requex-svc file path for connecting to GCP storage bucket
    svc_path = config['root_dir']+config['google_auth_json']

    # set the local environment variable
    os.environ[env_var] = svc_path

    # use the downloads directory for all actions
    downloads_dir = config['root_dir']+config['downloads_dir']

    # filenames to exclude from renaming
    exclude = config['excluded_files']

    # approved file extensions
    approved = config['data_formats']

    # Google Cloud Storage archive name
    gcs_name = config['google_cloud_storage_archive']

    # get a list of all files in the downloads directory
    files = get_file_list(downloads_dir)

    # archive all file names that have a datestamp and approved extension
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
                dest_file = create_dest_filename(
                    downloads_dir+file,
                    found_date,
                    config['file_map']
                    )
                upload_blob(gcs_name, downloads_dir+file, dest_file)


if __name__ == '__main__':
    run()
