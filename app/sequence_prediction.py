#!/usr/bin/env python
# -*- coding: utf-8 -*-

##------------------------------------------------------------##
'''
    File name: views.py
    Author: Paul Duc-Vinh TRAN
    E-Mail : dvp.tran@gmail.com
    Date created: 11/09/2017
    Date last modified: 11/09/2017
    Python Version: 2.7
'''

##------------------------------------------------------------##
#Imports

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation,Dropout,TimeDistributed
from keras.layers import LSTM,SimpleRNN,GRU,Input
from keras.optimizers import RMSprop
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from numpy import argmax
from keras.layers.core import Flatten, RepeatVector

##------------------------------------------------------------##





##------------------------------------------------------------##
#functions

def build_SeqGen_GRU_simple(VOCAB_SIZE,unit_nb,embedding_out=None):
    print("Build GRU Seq GENERATOR...")
    model_ = Sequential()
    if embedding_out:
        model_.add(Embedding(input_dim=VOCAB_SIZE,output_dim=embedding_out,trainable=True)) 
        model_.add(GRU(unit_nb,return_sequences=True))
    else:
        model_.add(GRU(unit_nb, input_shape=(None, VOCAB_SIZE), return_sequences=True))
    model_.add(GRU(unit_nb))
    model_.add(Dense(VOCAB_SIZE,activation="softmax"))
    model_.compile(loss="categorical_crossentropy", optimizer="rmsprop",metrics=["accuracy"])

    print ('Model input_shape (nb_samples, seq_length, input_dim): {0}'.format(model_.input_shape))
    print ('Model output_shape (nb_samples, seq_length, output_dim): {0}'.format(model_.output_shape))
    model_.summary()
    return model_

def load_model(model_path,model):
    model.load_weights(model_path)
    return model

def sequence_builder(sku_list,seq_len,char_indices):
    seq = [[char_indices[x] for x in sku_list]]
    seq = sequence.pad_sequences(seq, maxlen=seq_len, value=0,padding='post',truncating="pre")
    return seq

def predic(model, seq_input,VOCAB_SIZE,indices_char):
    pred = model.predict(seq_input).reshape((1,VOCAB_SIZE))
    pred = list(np.argmax(pred, axis=1))
    pred = [indices_char[x] for x in pred]
    return pred

def wrap_predict(model,sku_list,seq_len,VOCAB_SIZE,indices_char,char_indices,nb_predic=10):
    offset = len(sku_list)
    for i in range(0,nb_predic):
        seq = sequence_builder(sku_list,seq_len,char_indices)
        #pred = predic(model,seq,VOCAB_SIZE,indices_char)[0]
        preds = list(np.argsort(-model.predict_proba(seq)).reshape(VOCAB_SIZE,))
        preds = [indices_char[x] for x in preds if x!=0]
        for pred in preds:
            if pred not in sku_list:
                sku_list.append(pred)
                break
    #print(sku_list)
    return sku_list[offset:]
