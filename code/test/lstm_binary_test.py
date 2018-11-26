#!/usr/bin/python3

PROJECT_ROOT = "./"  # Running from code directory

BINARY_TOKENIZER_FILE = PROJECT_ROOT + "saved_models/binary_tokenizer.pkl"
BINARY_CATEGORIES_FILE = PROJECT_ROOT + "saved_models/binary_categories.pkl"
BINARY_MODEL_JSON = PROJECT_ROOT + "saved_models/binary_LSTM.json"
BINARY_MODEL_H5 = PROJECT_ROOT + "saved_models/binary_LSTM.h5"
BINARY_CLASS_REPORT = PROJECT_ROOT + "saved_models/binary_class_report.json"
BINARY_METRICS_REPORT = PROJECT_ROOT + "saved_models/binary_metrics_report.json"

import sys
sys.path.append(PROJECT_ROOT)
import lstm_binary 
import pandas as pd
from sklearn.model_selection import train_test_split


def test_train(dataset):
    #
    # Train the model
    #

    # 
    # Get the merged csv from commmand line
    #
    # merged_csv = sys.argv[1]

    #train_model = lstm_binary.LSTMBinary()
    #train_model.train(X_train, Y_train)
    #train_model.save(TOKENIZER_FILE, MODEL_JSON, MODEL_H5)
    pass

def test_predict():
    #
    # Test
    #
    testmodel = lstm_binary.LSTMBinary()
    testmodel.load(BINARY_TOKENIZER_FILE, BINARY_MODEL_JSON, BINARY_MODEL_H5, BINARY_METRICS_REPORT)
    testmodel.show()

    urllist = ["www.google.com", "www.netflix.com", "plvklpgwivery.com"]
    urltypes = testmodel.predict(urllist)
    print("URL type:", urltypes)

if __name__ == '__main__':
    # dataset = sys.argv[1]
    # test_train(dataset)
    test_predict()
