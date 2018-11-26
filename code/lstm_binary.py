#!/usr/bin/python3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from keras.models import Sequential, model_from_json
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.preprocessing import sequence
from keras.preprocessing import text

import tensorflow as tf
from tensorflow.python.client import device_lib

import pickle
import json

class LSTMBinary:

    def __init__(self):
        
        self.max_features = 1000                                # length of vocabulary
        self.batch_size = 4096                                   # input batch size
        self.num_epochs = 5                                     # epochs to train
        self.encoder = text.Tokenizer(num_words=500, char_level=True)

        self.model = Sequential()

        #
        # Model metrics
        #
        self.f1score = 0.0
        self.accuracy = 0.0
        self.precision = 0.0
        self.recall = 0.0
        self.fp = 0.0
        self.fn = 0.0


    def train(self, X_train, Y_train):
        # encode string characters to integers
        self.encoder.fit_on_texts(X_train)                                    # build character indices
        X_train_tz = self.encoder.texts_to_sequences(X_train)

        # Model definition - this is the core model from Endgame
        self.model.add(Embedding(self.max_features, 128, input_length=75))
        self.model.add(LSTM(128))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))
        self.model.compile(loss='binary_crossentropy', optimizer='rmsprop')

        # Pad sequence where sequences are case insensitive characters encoded to
        # integers from 0 to number of valid characters
        X_train_pad=sequence.pad_sequences(X_train_tz, maxlen=75)
        # Train where Y_train is 0-1
        self.model.fit(X_train_pad, Y_train, batch_size=self.batch_size, epochs=self.num_epochs)

    def show(self):
        print("\nMODEL Parameters")
        print("\tMax Features: ", self.max_features)
        print("\tBatch size: ", self.batch_size)
        print("\tNum epochs: ", self.num_epochs)

        print("\nMODEL Metrics")
        print("\tF1 Score: ", self.f1score)
        print("\tAccuracy: ", self.accuracy)
        print("\tPrecision: ", self.precision)
        print("\tRecall: ", self.recall)
        print("\tFalse Positives: ", self.fp)
        print("\tFalse Negatives: ", self.fn)

    def validate(self, test_data, test_classes):
        '''
        Return pred_classes
        '''
        pass

    def save(self, tokenizer_file, model_json_file, model_h5_file):
        #
        # Save the tokenizer
        #
        with open(tokenizer_file, 'wb') as handle:
            pickle.dump(self.encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)

        #
        # Save the model and the weights
        #
        model_save = self.model.to_json()
        with open(model_json_file, 'w') as file:
            file.write(model_save)

        self.model.save_weights(model_h5_file)

        print('MODEL SAVED TO DISK!')
        pass

    def load(self, tokenizer_file, model_json, model_h5, model_report):
        #
        # Load the tokenizer
        #
        with open(tokenizer_file, 'rb') as handle:
            self.encoder = pickle.load(handle)
        
        #
        # Load the model and its weights
        #
        file = open(model_json, 'r')
        model_load = file.read()
        file.close()

        self.model = model_from_json(model_load)
        self.model.load_weights(model_h5)
        global graph
        graph = tf.get_default_graph()

        with open(model_report) as report:
            metrics = json.load(report)
            self.f1score = metrics["DGA"]["f1-score"]
            self.precision = metrics["DGA"]["precision"]
            self.recall = metrics["DGA"]["recall"]
            self.accuracy = metrics["accuracy"]
            self.fp = metrics["false positives"]
            self.fn = metrics["false negatives"]

        print('SAVED BINARY MODEL IS NOW LOADED!')


    def predict(self, input):
        print(input)
        inputSeq = sequence.pad_sequences(self.encoder.texts_to_sequences(input), maxlen=75)
        with graph.as_default():
            output = self.model.predict_classes(inputSeq)
        return output


    def dump_reports(self, X_test, Y_test, Y_pred, bit_mask, format_m_report, format_c_report, verbose=False):
        '''input : input domain strings and true classes
        predictions: output classes from calling predict()
        bit_mask: single bit switches for multiple output dumps
                    0x01: prediction metrics
                    0x02: FP and FN predictions table
        format_m_report: 'json' format only, csv doesn't fit correctly here
        # list of atleast 1 of: 'csv' or 'json'
        format_c_report: ['json', 'csv']
        verbose: print messages at checkpoints
        '''

        '''PENDING RESOLUTION:
        - labels # class order mappings
        - name_nonDGA, name_DGA # class name mappings
        # file dump formats, (made as input arguments, for now)
        - format_m_report, format_c_report
        - name_m_report, name_c_report # file names, (currently set in app.py)
        '''

       # accuracy, precision, recall, f1, false positive, false negative
        pred_table = X_test.to_frame()
        pred_table.columns = ['domain']
        pred_table['trueClass'] = [labels[i] for i in Y_test]
        pred_table['predClass'] = [labels[i] for i in Y_pred]
        pred_table['predProb'] = [Y_pred_prob[idx][Y_pred[idx]] for idx in range(0, Y_pred.shape[0]) ]
        
        pred_table_FP = pred_table[(pred_table['trueClass'] == name_nonDGA) & (pred_table['predClass'] == name_DGA) ]
        pred_FP_frac = pred_table_FP.shape[0]/pred_table.shape[0]
        
        pred_table_FN = pred_table[(pred_table['trueClass'] == name_DGA) & (pred_table['predClass'] == name_nonDGA) ]
        pred_FN_frac = pred_table_FN.shape[0]/pred_table.shape[0]
        
        acc = accuracy_score(Y_test, Y_pred)
       
        if verbose:
            print("Metrics now calculated.")
            print("Starting file dump.")
            
        if bit_mask & 0x01:
            metrics_report = classification_report(Y_test, Y_pred, target_names=labels, output_dict=True)
            metrics_report['accuracy'] = acc
            metrics_report['false positives'] = pred_FP_frac
            metrics_report['false negatives'] = pred_FN_frac
            
            if format_m_report == 'json':
                fileName = name_m_report + '.' + format_m_report
                with open(fileName, 'w') as filePath:
                    json.dump(metrics_report, fp=filePath)
            
        # False Positives and False Negatives
        if bit_mask & 0x02:
            pred_table_FP.insert(0, 'type', 'FP')
            pred_table_FN.insert(0, 'type', 'FN')
            
            for extn in format_c_report:
                filePath = name_c_report + '.' + extn
                if extn == 'csv':
                    pred_table_FP.to_csv(filePath, mode='w', index=False, header=True)
                    pred_table_FN.to_csv(filePath, mode='a', index=False, header=False)
                elif extn == 'json':
                    pred_table_FP.append(pred_table_FN)
                    pred_table_FP.to_json(filePath, orient='table', index=False)
        
        if verbose:
            print("Finished file dump.")
