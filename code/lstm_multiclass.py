#!/usr/bin/python3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from keras.models import Sequential, model_from_json
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.preprocessing import sequence
from keras.preprocessing import text
from keras.utils import to_categorical

import tensorflow as tf
from tensorflow.python.client import device_lib

import pickle

class LSTMMulti:

    def __init__(self):
        
        self.max_features = 1000                                # length of vocabulary
        self.batch_size = 128                                   # input batch size
        self.num_epochs = 2                                     # epochs to train
        self.encoder = text.Tokenizer(num_words=500, char_level=True)

        self.model = Sequential()

    def train(self, X_train, Y_train):
        # encode string characters to integers
        self.encoder.fit_on_texts(X_train)                                    # build character indices
        X_train_tz = self.encoder.texts_to_sequences(X_train)

        self.categories = list(Y_train.unique())

        # Model definition - this is the core model from Endgame
        self.model.add(Embedding(self.max_features, 128, input_length=75))
        self.model.add(LSTM(128))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(len(self.categories)))
        self.model.add(Activation('softmax'))
        self.model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

        # Pad sequence where sequences are case insensitive characters encoded to
        # integers from 0 to number of valid characters
        X_train_pad=sequence.pad_sequences(X_train_tz, maxlen=75)
        Y_train_binarized = to_categorical(Y_train, num_classes=len(self.categories))

        self.model.fit(X_train_pad, Y_train_binarized, batch_size=self.batch_size, epochs=self.num_epochs)

    def save(self, tokenizer_file, categories_file, model_json_file, model_h5_file):
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

    def load(self, tokenizer_file, categories_file, model_json, model_h5):
        #
        # Load the tokenizer
        #
        with open(tokenizer_file, 'rb') as handle:
            self.encoder = pickle.load(handle)
        
        #
        # Load the category list
        #
        with open(categories_file, 'rb') as handle:
            self.categories = pickle.load(handle)

        #
        # Load the model and its weights
        #
        file = open(model_json, 'r')
        model_load = file.read()
        file.close()
        self.model = model_from_json(model_load)
        self.model.load_weights(model_h5)
        global lstm_multi_graph
        lstm_multi_graph = tf.get_default_graph()

        print('SAVED MULTICLASS MODEL IS NOW LOADED!')


    def predict(self, input):
        print(input)
        inputSeq = sequence.pad_sequences(self.encoder.texts_to_sequences(input), maxlen=75)
        with lstm_multi_graph.as_default():
            output = self.model.predict_classes(inputSeq)
        print(output)
        return self.categories[output]
