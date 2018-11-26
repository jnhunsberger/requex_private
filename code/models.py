#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Libraries
import os
import argparse
import sys
import time
import json
import re
import numpy as np
import pandas as pd
import statistics as stat
import lstm_binary
import lstm_multiclass
from pprint import pprint
from datetime import datetime
from shutil import copy2
from sklearn.model_selection import train_test_split
import pickle

# constants
models_path = '../data/local/models/'
data_path = '../data/local/staging/'

REFPATH = "./"
PROJECT_ROOT = "/Users/nscsekhar/Desktop/nscsekhar/Desktop/Surya/Personal/MIDS/W210/Project/team_cyber/"
MULTI_TOKENIZER_FILE = PROJECT_ROOT + "saved_models/multiclass_tokenizer.pkl"
MULTI_CATEGORIES_FILE = PROJECT_ROOT + "saved_models/multiclass_categories.pkl"
MULTI_MODEL_JSON = PROJECT_ROOT + "saved_models/multiclass_LSTM.json"
MULTI_MODEL_H5 = PROJECT_ROOT + "saved_models/multiclass_LSTM.h5"


def valid_filename(filename, path=''):
    '''valid_filename: determines if the given filename is a real file. Assumes that the file is in the current working directory for the program.

    returns: given file name
    '''
    if path == '':
        path = os.getcwd()+'/'

    if not os.path.isfile(path+filename):
        msg = "The given file '{}' does not exist at '{}'.".format(
            filename,
            path
            )
        raise argparse.ArgumentTypeError(msg)

    return filename


def parse_args():
    '''parse_args: parse command line arguments

    return: dictionary of arguments
    '''
    parser = argparse.ArgumentParser(
        description='Runs models either in train or inference mode.',
        prog='models',
        epilog='Models requires at least one of -t/--train or -i/--inference to operate correctly. Both may be provided for sequential analysis.')
    parser.add_argument('config_file',
                        type=valid_filename,
                        metavar='CONFIG_FILE',
                        help="File path to the requex configuration file. File must be in JSON format.")
    parser.add_argument('-t', '--train',
                        metavar='TRAINING_FILE',
                        nargs=1,
                        help="Runs models in training mode. Training will be run on the given file. The training file must be a prepared '.csv' file. The program will search for the file in the models, then staging, and finally downloads directories.")
    parser.add_argument('-i', '--inference',
                        metavar='INFERENCE_FILE',
                        nargs=1,
                        help="Runs models in inference mode. Inference will be run on the given file. The inference file must be a list of domains separated by carriage returns with no header. The program will search for the file in the models, then staging, and finally downloads directories.")
    parser.add_argument('-m', '--model', choices=['binary', 'multiclass'],
                        metavar='model_type',
                        required=True,
                        help="This required option indicates which type of model is being built or used. Using 'binary' selects a benign/malicious model. Using 'multiclass' will classify the malware family for each malicious classified entry.")

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
        # filename provided, verify the file exists
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


def get_file_date(filename):
    '''get_file_date: extracts file date from file name. File date must be in YYYY-MM-DD format.

    returns: datetime object of file date.
    '''
    date = re.search(r'\d\d\d\d-\d\d-\d\d|$', filename).group()
    year, month, day = date.split('-')
    return datetime(int(year), int(month), int(day))


def write_to_train_logfile(metrics, logpath, stdout=True):
    '''write_to_train_logfile: writes metadata in the metrics dict to a logfile
    '''
    # constants
    logfile = 'requex_training_log.csv'

    # write to logfile
    stamp = datetime.utcnow().strftime('%Y-%m-%d-%H:%M')

    # extract the filename
    # filename = os.path.basename(datafile)

    if stdout:
        # print("info:{:>10} rows: {:>10} malicious, {:>10} benign, a {:>3.3f} ratio".format(total_rows, malicious_rows, benign_rows, ratio))
        print('info: {}, {}, {}, {:>3.3f}s, {:>3.2f} MB, {} rows: {} malicious, {} benign, {:>3.3f} ratio, {}, {} categories, train rows: {}, test rows: {}, train time: {:>3.3f}s, inference time: {:>3.3f}s'.format(
             stamp, metrics['filename'], metrics['filedate'], metrics['time'], metrics['memory'], metrics['total_rows'], metrics['malicious_rows'], metrics['benign_rows'], metrics['ratio'], metrics['model'], metrics['categories'], metrics['train_rows'], metrics['test_rows'], metrics['train_time'], metrics['inference_time']))

    with open(logpath+logfile, 'at') as log:
        log.write('{}, {}, {}, {:>3.3f}, {:>3.2f}, {}, {}, {}, {:>3.3f}, {}, {}, {}, {}, {:>3.3f}, {:>3.3f}\n'.format(
             stamp, metrics['filename'], metrics['filedate'], metrics['time'], metrics['memory'], metrics['total_rows'], metrics['malicious_rows'], metrics['benign_rows'], metrics['ratio'], metrics['model'], metrics['categories'], metrics['train_rows'], metrics['test_rows'], metrics['train_time'], metrics['inference_time']))


def copy_models(src, dst):
    '''copy_models: copies the source file (src) to the dst directory. src must be a file and dst must be a directory. Exclusions is an optional parameter that allows for files with certain file names to be excluded from being moved.
    '''
    # check to see if a directory for the dst directory exists
    if not os.path.isdir(dst):
        # directory does not exist, create it
        os.mkdir(dst)

    # verify whether the source and destination are the same
    src_path, filename = os.path.split(src)
    if os.path.isfile(dst+filename):
        print("A file by the name '{}' already exists. File not copied. Processing will continue using the file already in the '{}' directory.".format(filename, dst))
    elif os.path.isfile(src):
        copy2(src, dst)
    else:
        print("The given file '{}' does not exist.".format(src))
        exit(1)


def get_training_data(filename, metrics, logpath):
    '''get_training_data: reads the csv file into a pandas dataframe

    return: pandas dataframe
    '''
    # constants
    MB = 1024*1024

    start_time = time.time()
    df = pd.read_csv(filename,
                     sep=',',
                     parse_dates=[0],
                     dtype={1: int, 2: str, 3: str},
                     engine='c')
    end_time = time.time()
    read_time = end_time - start_time

    # calculate the memory footprint of the dataframe
    memory = sys.getsizeof(df)/MB

    filedate = get_file_date(filename)
    total = df.shape[0]
    benign = df.loc[df['dga'] == 0].shape[0]
    malicious = df.loc[df['dga'] == 1].shape[0]
    ratio = malicious / benign

    # write to logfile
    # write_to_train_logfile(logpath, filename, filedate.strftime('%Y-%m-%d'), read_time, memory, total, malicious, '2',benign, ratio)
    metrics = {
        'filename': filename,
        'filedate': filedate.strftime('%Y-%m-%d'),
        'time': read_time,
        'memory': memory,
        'total_rows': total,
        'malicious_rows': malicious,
        'benign_rows': benign,
        'ratio': ratio,
        'categories': 0,
        'model': 'unknown',
        'train_rows': 0,
        'test_rows': 0,
        'train_time': 0,
        'inference_rows': 0,
        'inference_time': 0,
        'inference_time_mean': 0.0
    }

    return df, metrics


def prep_training_dataset_binary(df):
    '''prep_training_dataset_binary: creates X, Y datasets for training and testing.

    returns: pandas dataframe x4: X_train, X_test, Y_train, Y_test
    '''
    # create X, Y dataframes. X = 'domain' and the model will try to
    # predict Y the catengory index.
    X = df['domain']
    Y = df['dga']

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=23)

    return X_train, X_test, Y_train, Y_test


def prep_training_dataset_multiclass(df, categories_file):
    '''prep_training_dataset_multiclass: creates X, Y datasets for training and testing.

    returns: pandas dataframe x4: X_train, X_test, Y_train, Y_test and the number of uniques
    '''

    # factorize the malware column
    df['catIndex'], uniques = pd.factorize(df['malware'], sort=True)

    # display factorized values
    # print('malware uniques: total - {}\n{}'.format(len(uniques), uniques))
    # print('catIndex uniques: {}'.format(
    #       pd.unique(df['catIndex'].sort_values())))

    # record the categories to disk
    with open(categories_file, 'wb') as f:
        pickle.dump(uniques, f, protocol=pickle.HIGHEST_PROTOCOL)

    # create X, Y dataframes. X = 'domain' and the model will try to
    # predict Y the catengory index.
    X = df['domain']
    Y = df['catIndex']

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=23)

    return X_train, X_test, Y_train, Y_test, len(uniques)


def get_model_info(model_type, config):
    '''get_model_info: returns a dictionary with key value pairs of model file keys and model file names. The model file names are full path names anchored to the root_dir and placed in the models directory.

    type: a string indicating the type of model ['binary', ['multiclass']
    config: a dict filled with configuration parameters

    return: dict of model:filename pairs
    '''

    if model_type == 'binary':
        model = config['binary_model']
    elif model_type == 'multiclass':
        model = config['multiclass_model']
    else:
        # this branch shouldn't happen with the way parse_args() written
        msg = "error: unsupported model type '{}'.".format(model_type)
        raise argparse.ArgumentTypeError(msg)
        exit(1)

    root_dir = config['root_dir']
    models_dir = config['models_dir']

    model = {
        'model_json': root_dir+models_dir+model['model_json'],
        'model_H5': root_dir+models_dir+model['model_H5'],
        'model_tokenizer': root_dir+models_dir+model['model_tokenizer'],
        'model_categories': root_dir+models_dir+model['model_categories']
    }

    return model


def find_file(filename, config):
    '''find_file: looks for the  file in a few directories and moves it into the models_dir. Returns the full path to the training file.

    return: string of full file path in the models_dir or an empty string
    '''
    root_dir = config['root_dir']
    downloads_dir = config['downloads_dir']
    staging_dir = config['staging_dir']
    models_dir = config['models_dir']

    # look for file in models_dir
    # look for file in staging_dir
    # look for file in downloads_dir
    if os.path.isfile(root_dir+models_dir+filename):
        return root_dir+models_dir
    elif os.path.isfile(root_dir+staging_dir+filename):
        return root_dir+staging_dir
    elif os.path.isfile(root_dir+downloads_dir+filename):
        return root_dir+downloads_dir
    else:
        return ''
        # msg = "The given file '{}' does not exist at any of these locations '{}', '{}', '{}'.".format(
        #     filename,
        #     models_dir,
        #     staging_dir,
        #     downloads_dir
        #     )
        # print(msg)
        # exit(1)


def get_model_type(model_type):
    '''get_model_type: evaluates model_type to see if it is a valid option. If model_type is empty, function will attempt to pull the parameters from the command line. This function should mirror the choices in parse_args() for -m/--models.

    return: a string with the model_type; empty string if not correct.
    '''
    if model_type is '':
        args = parse_args()
        return args['model']
    elif model_type.lower() == 'binary':
        return 'binary'
    elif model_type.lower() == 'multiclass':
        return 'multiclass'
    else:
        return ''


def get_train_file(filename, config):
    '''get_train_file: evaluates the filename as well as command line arguments to get the training file name. Verifies that the training file exists.

    returns: string of a filename or empty string if not valid.
    '''
    root_dir = config['root_dir']
    models_dir = config['models_dir']

    if filename == '':
        # no filename provided, attempt to get it from the command line
        # parameters
        args = parse_args()
        train_file = args['train']
        if train_file is not None:
            # extract the filename from the parameter list
            train_file = train_file[0]
            location = find_file(train_file, config)
            if location == '':
                # file was not found
                return ''
            else:
                copy_models(location+train_file, root_dir+models_dir)
                return root_dir+models_dir+train_file
        else:
            # the command line parameter for train_file was also None
            return ''
    else:
        # filename was provided
        location = find_file(train_file, config)
        if location == '':
            # file was not found
            return ''
        else:
            copy_models(location+train_file, root_dir+models_dir)
            return root_dir+models_dir+train_file


def get_inference_file(filename, config):
    '''get_inference_file: evaluates the filename as well as command line arguments to get the inference file name. Verifies that the inference file exists.

    returns: string of a filename or empty string if not valid.
    '''
    root_dir = config['root_dir']
    models_dir = config['models_dir']

    if filename == '':
        # no filename provided, attempt to get it from the command line
        # parameters
        args = parse_args()
        inference_file = args['inference']
        if inference_file is not None:
            # extract the filename from the parameter list
            inference_file = inference_file[0]
            location = find_file(inference_file, config)
            if location == '':
                # file was not found
                return ''
            else:
                copy_models(location+inference_file, root_dir+models_dir)
                return root_dir+models_dir+inference_file
        else:
            # the command line parameter for inference_file was also None
            return ''
    else:
        # filename was provided
        location = find_file(inference_file, config)
        if location == '':
            # file was not found
            return ''
        else:
            copy_models(location+inference_file, root_dir+models_dir)
            return root_dir+models_dir+inference_file


def load_inference_data(filename):
    '''load_inference_data: reads data from the given filename. The file must be a text file with '\n' at the end of each entry, one entry per line.

    returns: list of data to be analyzed
    '''
    domains = []
    with open(filename, 'rt', newline='\n') as f:
        lines = f.readlines()

    for line in lines:
        domains.append(line.strip())

    return domains


def write_predictions(domains, predictions, model_type, config):
    '''write_predictions: takes a 1-D list of domains and predictions and writes them to the inference file output. File name will be 'predictions_YYYY-MM-DD.txt'.
    '''

    # create filename
    root_dir = config['root_dir']
    models_dir = config['models_dir']

    # get the current date and time:
    datestamp = time.strftime('%Y-%m-%d', time.gmtime())
    timestamp = time.strftime('%H:%M.%S', time.gmtime())

    output_file = root_dir+models_dir+model_type+'_predictions_'+datestamp+'.txt'

    # write the predictions to disk
    with open(output_file, 'wt') as f:
        f.write('creation_date: {} {}\n'.format(datestamp, timestamp))
        for i, p in enumerate(predictions):
            # print('i: {}, p: {}, domains: {}'.format(i, p, domains[i]))
            f.write('{}, {}\n'.format(domains[i], p))


def run(config_file=None, model_type='', train_file='', inference_file=''):
    # get configuration parameters
    config_file = get_config_filename(config_file)
    config = get_config(config_file)
    # print('configuration settings:')
    # pprint(config)

    # parse function/command line parameters
    model_type = get_model_type(model_type)
    train_file = get_train_file(train_file, config)
    inference_file = get_inference_file(inference_file, config)

    # assemble the path to the log directory
    root_dir = config['root_dir']
    models_dir = config['models_dir']
    logpath = root_dir+models_dir

    if model_type == '':
        print("error: an invalid model type was given. See the -h/--help command line options for valid model choices.")
        exit(1)

    if train_file == '' and inference_file == '':
        print("error: neither train or inference were given as arguments. Please run again, but with either -t/--train or -i/--inference options (or both) enabled.")
        exit(1)

    # get the model information from the configuration file
    model_info = get_model_info(model_type, config)
    metrics = {
        'filename': '',
        'filedate': '',
        'time': 0.0,
        'memory': 0.0,
        'total_rows': 0,
        'malicious_rows': 0,
        'benign_rows': 0,
        'ratio': 0.0,
        'categories': 0,
        'model': 'unknown',
        'train_rows': 0,
        'test_rows': 0,
        'train_time': 0,
        'inference_rows': 0,
        'inference_time': 0,
        'inference_time_mean': 0.0
    }

    if train_file != '':
        # a training file was provided

        # get training data from disk
        df, metrics = get_training_data(train_file, metrics, logpath)

        if model_type == 'binary':
            X_train, X_test, Y_train, Y_test = prep_training_dataset_binary(df)
            metrics['model'] = model_type
            metrics['categories'] = 2
            metrics['train_rows'] = X_train.shape[0]
            metrics['test_rows'] = X_test.shape[0]
            # pprint(metrics)
            print('info: {} – training started.'.format(time.strftime('%Y-%m-%d %H:%M.%S', time.gmtime())))
            train_model = lstm_binary.LSTMBinary()
            start_time = time.time()
            train_model.train(X_train, Y_train)
            end_time = time.time()
            train_time = end_time - start_time
            metrics['train_time'] = train_time
            print('info: {} – training ended. Train time {:>3.3f}s.'.format(time.strftime('%Y-%m-%d %H:%M.%S', time.gmtime()), train_time))
            write_to_train_logfile(metrics, logpath, True)

            train_model.save(model_info['model_tokenizer'],
                             model_info['model_json'],
                             model_info['model_H5'])

        elif model_type == 'multiclass':
            # create X and Y and split into train and test
            X_train, X_test, Y_train, Y_test, categories = prep_training_dataset_multiclass(
                df, model_info['model_categories'])
            metrics['model'] = model_type
            metrics['categories'] = categories
            metrics['train_rows'] = X_train.shape[0]
            metrics['test_rows'] = X_test.shape[0]

            print('info: {} – training started.'.format(time.strftime('%Y-%m-%d %H:%M.%S', time.gmtime())))
            start_time = time.time()
            train_model = lstm_multiclass.LSTMMulti()
            train_model.train(X_train, Y_train)
            end_time = time.time()
            train_time = end_time - start_time
            metrics['train_time'] = train_time
            print('info: {} – training ended. Train time {:>3.3f}s.'.format(time.strftime('%Y-%m-%d %H:%M.%S', time.gmtime()), train_time))
            write_to_train_logfile(metrics, logpath, True)

            train_model.save(model_info['model_tokenizer'],
                             model_info['model_categories'],
                             model_info['model_json'],
                             model_info['model_H5'])
        else:
            print("error: unrecognized model type.")
            exit(1)
        # train the model (which model is set by models input)
        # train_model.train(X_train, Y_train)
        # train_model.save(TOKENIZER_FILE, MODEL_JSON, MODEL_H5)
        # save the model to disk

    if inference_file != '':
        # an inference file was provided
        print('inference file: {}'.format(inference_file))
        if model_type == 'binary':
            metrics['filename'] = inference_file
            metrics['filedate'] = time.strftime('%Y-%m-%d', time.gmtime())

            predict_model = lstm_binary.LSTMBinary()
            predict_model.load(model_info['model_tokenizer'],
                               model_info['model_json'],
                               model_info['model_H5'])
            domains = load_inference_data(inference_file)
            # print("Number of domains: ", len(domains))
            # print("Top 10:\n", domains[:10])

            # run predictions, record timings
            timestamp = time.strftime('%Y-%m-%d %H:%M.%S', time.gmtime())
            print('info: {} – inference started.'.format(timestamp))
            start_time = time.time()
            predictions = predict_model.predict(domains)
            end_time = time.time()
            prediction_time = end_time - start_time
            domain_count = len(domains)
            metrics['inference_rows'] = domain_count
            metrics['inference_time'] = prediction_time
            metrics['inference_time_mean'] = prediction_time / domain_count
            timestamp = time.strftime('%Y-%m-%d %H:%M.%S', time.gmtime())
            print('info: {} – inference ended. Inference time {:>3.3f}s.'.format(timestamp, prediction_time))

            # reshape the predictions
            predictions = np.reshape(predictions, [predictions.shape[0], ]).tolist()
            # print(predictions[:10])
            # print("domains: {}, predictions: {}".format(len(domains), len(predictions)))

            # write the predictions to file
            write_predictions(domains, predictions, model_type, config)

            # write_to_train_logfile(metrics, logpath, True)
        elif model_type == 'multiclass':
            metrics['filename'] = inference_file
            metrics['filedate'] = time.strftime('%Y-%m-%d', time.gmtime())

            predict_model = lstm_multiclass.LSTMMulti()
            predict_model.load(model_info['model_tokenizer'],
                               model_info['model_categories'],
                               model_info['model_json'],
                               model_info['model_H5'])
            domains = load_inference_data(inference_file)
            # print("Number of domains: ", len(domains))
            # print("Top 10:\n", domains[:10])

            # run predictions, record timings
            timestamp = time.strftime('%Y-%m-%d %H:%M.%S', time.gmtime())
            print('info: {} – inference started.'.format(timestamp))
            start_time = time.time()
            predictions, pred_prob = predict_model.predict(domains)
            end_time = time.time()
            prediction_time = end_time - start_time
            domain_count = len(domains)
            metrics['inference_rows'] = domain_count
            metrics['inference_time'] = prediction_time
            metrics['inference_time_mean'] = prediction_time / domain_count
            timestamp = time.strftime('%Y-%m-%d %H:%M.%S', time.gmtime())
            print('info: {} – inference ended. Inference time {:>3.3f}s.'.format(timestamp, prediction_time))

            # reshape the predictions
            # predictions = np.reshape(predictions, [predictions.shape[0], ]).tolist()
            # print(predictions[:10])
            # print("domains: {}, predictions: {}".format(len(domains), len(predictions)))

            # write the predictions to file
            write_predictions(domains, predictions, model_type, config)
        else:
            print("error: unrecognized model type.")
            exit(1)
        # get test data
        # load the model (based on models input)
        # testmodel = lstm_binary.LSTMBinary()
        # testmodel.load(BINARY_TOKENIZER_FILE, BINARY_MODEL_JSON, BINARY_MODEL_H5)
        # make predictions
        # urllist = ["www.google.com", "www.netflix.com", "plvklpgwivery.com"]
        # urltypes = testmodel.predict(urllist)
        # print("URL type:", urltypes)


if __name__ == '__main__':
    run()
