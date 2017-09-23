#!/usr/bin/env python
# -*- coding: utf-8 -*-

##------------------------------------------------------------##
'''
    File name: text_to_speech.py
    Author: Paul Duc-Vinh TRAN
    E-Mail : dvp.tran@gmail.com
    Date created: 11/09/2017
    Date last modified: 11/09/2017
    Python Version: 2.7
'''

##------------------------------------------------------------##

from gtts import gTTS
import os


def save_speech(text,path = "data/",filename="answer.mp3",lang="fr"):
    if not os.path.exists(path):
        os.makedirs(path)
    tts = gTTS(text=text, lang=lang)
    tts.save(path+filename)
    print("save at %s" %path+filename)
    return