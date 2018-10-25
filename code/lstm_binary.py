#!/usr/bin/python3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.preprocessing import sequence
from keras.preprocessing import text

from tensorflow.python.client import device_lib

class LSTMBinary:

    def __init__(self):
        
        self.max_features = 1000                                # length of vocabulary
        self.batch_size = 128                                   # input batch size
        self.num_epochs = 5                                     # epochs to train
        self.encoder = text.Tokenizer(num_words=500, char_level=True)

        self.model = Sequential()

    def train(self, X_train):
        # encode string characters to integers
        self.encoder.fit_on_texts(X_train)                                    # build character indices
        X_train_tz = self.encoder.texts_to_sequences(X_train)

        # Model definition - this is the core model from Endgame
        self.model.add(Embedding(max_features, 128, input_length=75))
        self.model.add(LSTM(128))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))
        self.model.compile(loss='binary_crossentropy', optimizer='rmsprop')

        # Pad sequence where sequences are case insensitive characters encoded to
        # integers from 0 to number of valid characters
        X_train_pad=sequence.pad_sequences(X_train_tz, maxlen=75)

        # Train where Y_train is 0-1
        self.model.fit(X_train_pad, Y_train, batch_size=batch_size, epochs=num_epochs)

    def load(self):
        pass

    def predict(self, test_data):
        pass
