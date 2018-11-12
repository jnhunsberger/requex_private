#!/usr/bin/python3

REFPATH = "./"
PROJECT_ROOT = "/Users/nscsekhar/Desktop/nscsekhar/Desktop/Surya/Personal/MIDS/W210/Project/team_cyber/"
TOKENIZER_FILE = PROJECT_ROOT + "code/saved_models/tokenizer"
CATEGORIES_FILE = PROJECT_ROOT + "code/saved_models/multiclass_categories"
MODEL_JSON = PROJECT_ROOT + "code/saved_models/multiclass_LSTM.json"
MODEL_H5 = PROJECT_ROOT + "code/saved_models/multiclass_LSTM.h5"
dga_csv = PROJECT_ROOT + "data/2018_0923/dga-feed-high.csv"
cisco_csv = PROJECT_ROOT + "data/2018_0923/top-1m.csv"
SUFFIXES = [' DGA', ' (', ' -']

import sys
sys.path.append(REFPATH)
import lstm_multiclass 
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle

#
# Prepare dataset (move to a different source)
#
""" Extract the DGA categories from the description string """
def strip_cat(input_str_row, lstrip_str="Domain used by ", rtrunc_str=SUFFIXES, verbose=False):
    if verbose:
        print('-'*50, '\nInput:    ', input_str_row['dga'])
    str1 = input_str_row['dga'].replace(lstrip_str, '')
    if verbose:
        print('Lstrip:   ', str1)
    str2 = str1
    for i in rtrunc_str:
        idx = str2.find(i)
        if idx != -1:
            str2 = str2[0:idx]
            if verbose:
                print('Trimmed:  ', str2)
            break
    return str2

def update_categories(input_row):
    if input_row['dga'] in MERGED_CAT_LIST:
        return MERGED_CAT_STR
    else:
        return input_row['dga']


def prepDataset(dga_file, cisco_file):
    dga_df = pd.read_csv(dga_file, header=None, skiprows=15)
    cisco_df = pd.read_csv(cisco_file, header=None)

    dga_df_slim =   dga_df.drop(columns=range(2,dga_df.shape[1]), inplace=False)
    dga_df_slim.columns = ['domain', 'dga']
    dga_df_slim['dga'] = dga_df_slim.apply(lambda row: strip_cat(row, verbose=False), axis=1)
    # dga_df_slim['dga'] = dga_df_slim.apply(update_categories, axis=1)

    cisco_df_slim = cisco_df.drop(columns=[0], inplace=False)
    cisco_df_slim.columns = ['domain']
    cisco_df_slim['dga'] = 'nonDGA'

    unified_df = pd.concat([cisco_df_slim, dga_df_slim], ignore_index=True)
    unified_df['catIndex'], labels = pd.factorize(unified_df['dga'], sort=True)

    print(labels)

    with open(CATEGORIES_FILE, 'wb') as handle:
        pickle.dump(labels, handle, protocol=pickle.HIGHEST_PROTOCOL)

    X = unified_df['domain']
    Y = unified_df['catIndex']

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2,random_state=23)

    return X_train, X_test, Y_train, Y_test

#
# Get the train and test data
#
# X_train, X_test, Y_train, Y_test = prepDataset(dga_csv, cisco_csv)

#
# Train the model
#
# train_model = lstm_multiclass.LSTMMulti()
# train_model.train(X_train, Y_train)
# train_model.save(TOKENIZER_FILE, CATEGORIES_FILE, MODEL_JSON, MODEL_H5)

#
# Test
#
testmodel = lstm_multiclass.LSTMMulti()
testmodel.load(TOKENIZER_FILE, CATEGORIES_FILE, MODEL_JSON, MODEL_H5)

# urllist = ["www.google.com", "www.netflix.com", "plvklpgwivery.com"]
urllist = ["www.google.com"]
urltypes = testmodel.predict(urllist)
print("URL type:", urltypes[0])