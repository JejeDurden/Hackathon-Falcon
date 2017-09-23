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
from app import app
from flask import make_response,\
                    abort, jsonify, Blueprint, Flask, request,current_app


import pandas as pd
import json
from datetime import timedelta
from functools import update_wrapper
#import numpy as np

#import als_light as als
#import visual_reco as vr
#import sequence_prediction as sp
import text_to_speech as tts
import speech_to_text as stt
import recast as rc


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

##------------------------------------------------------------##


##------------------------------------------------------------##
def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Cache-Control'] = 'no-store, no-cache'
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


##------------------------------------------------------------##
#set env
main = Blueprint('main', __name__)

##------------------------------------------------------------##
#functions

def search(text):
    return text

    
##------------------------------------------------------------##
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"




@app.route("/api/stt", methods = ['GET', 'POST'])
@crossdomain(origin='*')
def carson_stt():
    if 'path' in request.args:
        if request.args['path']:
            path = request.args['path']#.replace("_","/")
            print(path)
            out = stt.speech_to_text(path)
            return(json.dumps({"response":out}))
        else:
            return(json.dumps({"response":"Je n'ai pas compris "}))
    return(json.dumps({"response":"Pas d'argument"}))
    
    
    
@app.route("/api/tts", methods = ['GET', 'POST'])
@crossdomain(origin='*')
def carson_tts():
    if 'text' in request.args:
        if request.args['text']:
            text = request.args['text']#.replace("_","/")
            print(text)
            out = tts.save_speech(text,path = "app/data/",filename="answer.mp3",lang="fr")
            return(json.dumps({"response":"Success"}))
        else:
            return(json.dumps({"response":"Je n'ai pas compris "}))
    return(json.dumps({"response":"Pas d'argument"}))

