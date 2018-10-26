#!/usr/bin/python3

REFPATH = "../"
PROJECT_ROOT = "/Users/nscsekhar/Desktop/nscsekhar/Desktop/Surya/Personal/MIDS/W210/Project/team_cyber/"
TOKENIZER_FILE = PROJECT_ROOT + "code/saved_models/tokenizer"
MODEL_JSON = PROJECT_ROOT + "code/saved_models/binary_LSTM.json"
MODEL_H5 = PROJECT_ROOT + "code/saved_models/binary_LSTM.h5"
dga_csv = PROJECT_ROOT + "data/2018_0923/dga-feed-high.csv"
cisco_csv = PROJECT_ROOT + "data/2018_0923/top-1m.csv"

import sys
sys.path.append(REFPATH)
import lstm_binary 
import pandas as pd
from sklearn.model_selection import train_test_split

#
# Prepare dataset (move to a different source)
#
def prepDataset(dga_file, cisco_file):
    dga_df = pd.read_csv(dga_file, header=None, skiprows=15)
    cisco_df = pd.read_csv(cisco_file, header=None)

    dga_df_slim =   dga_df.drop(columns=range(1,dga_df.shape[1]), inplace=False)
    dga_df_slim.columns = ['domain']
    cisco_df_slim = cisco_df.drop(columns=[0], inplace=False)
    cisco_df_slim.columns = ['domain']
    dga_df_slim['dga'] = 1
    cisco_df_slim['dga'] = 0

    unified_df = pd.concat([cisco_df_slim, dga_df_slim], ignore_index=True)
    X = unified_df['domain']
    Y = unified_df['dga']
    
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2,random_state=23)

    return X_train, X_test, Y_train, Y_test

#
# Get the train and test data
#
X_train, X_test, Y_train, Y_test = prepDataset(dga_csv, cisco_csv)

#
# Train the model
#
#train_model = lstm_binary.LSTMBinary()
#train_model.train(X_train, Y_train)
#train_model.save(TOKENIZER_FILE, MODEL_JSON, MODEL_H5)

#
# Test
#
testmodel = lstm_binary.LSTMBinary()
testmodel.load(TOKENIZER_FILE, MODEL_JSON, MODEL_H5)

urllist = ["www.google.com", "www.netflix.com", "plvklpgwivery.com"]
urltypes = testmodel.predict(urllist)
print("URL type:", urltypes)