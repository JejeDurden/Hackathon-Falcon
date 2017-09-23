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
import numpy as np

import als_light as als
import visual_reco as vr
import sequence_prediction as sp


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
#read csv
sku_df = pd.read_csv("data/sku_info/keep_info.csv",sep="|",index_col=0,encoding="utf-8")
sku_names = map(lambda x : str(x),list(set(sku_df.sku_name)))
#list files/images
files_list = list(sku_df["code_custom"])

#var
material_list = list(set(sku_df.aesthetic_sub_line))
material_list = sorted([str(x) for x in material_list])
colour_list = list(set(sku_df.color))
colour_list = sorted([str(x) for x in colour_list])
category_list = list(set(sku_df.custom_category))
category_list = sorted([str(x) for x in category_list])


#matrix
sim = np.fromfile('data/saved_model/distance_matrix_complete.dat', dtype=float) #distance_matrix_complete_InceptionV3.dat
sim = sim.reshape((len(files_list), len(files_list)))

item_factors = np.load('data/saved_model/item_factors.npy')
user_factors = np.load('data/saved_model/user_factors.npy')


#load dictionnaries
with open('data/saved_model/idx_to_mid.json') as json_data:
    idx_to_mid = json.load(json_data)
# need to cast idx_to_mid keys as int
keylist = idx_to_mid.keys()
keylist = map( lambda x : int(x),keylist)
keylist.sort()
idx_to_mid = {key : idx_to_mid[str(key)] for key in keylist }
del keylist
with open('data/saved_model/uid_to_idx.json') as json_data:
    uid_to_idx = json.load(json_data)    

with open('data/LSTM_data/char_indices.json') as json_data:
    char_indices = json.load(json_data)
with open('data/LSTM_data/indices_char.json') as json_data:
    indices_char = json.load(json_data) 
# need to cast indices_char keys as int
keylist = indices_char.keys()
keylist = map( lambda x : int(x),keylist)
keylist.sort()
indices_char = {key : indices_char[str(key)] for key in keylist }    
   

#params for gru
seq_len = 50
unit_nb = 100
embedding_out = 128
VOCAB_SIZE = len(indices_char)+1
#load model
last_checkpoint="data/LSTM_data/checkpoint_100_epoch_162.hdf5"
model = sp.build_SeqGen_GRU_simple(VOCAB_SIZE,unit_nb,embedding_out=128)
model = sp.load_model(last_checkpoint,model)


##------------------------------------------------------------##


def search(text):
    out = sku_df[sku_df["sku_name"]==text]
    out = list(out["code_custom"])
    if len(out)>0:
        output = [{"sku_code": x, "name" : list(sku_df[sku_df["code_custom"]==x].sku_name)[0]} for x in out]
        return(json.dumps({"sku_list":output}))
    else:
        return(json.dumps({"sku_list":output}))


    
##------------------------------------------------------------##
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route("/api/search", methods = ['GET', 'POST'])
@crossdomain(origin='*')
def get_search():
    if 'input' in request.args:
        if request.args['input']:
            return search(request.args['input'])
        else:
            return(json.dumps({"sku_list":[]}))
    return(json.dumps({"sku_list":[]}))


@app.route("/api/rec_seq", methods = ['GET', 'POST'])
@crossdomain(origin='*')
def pred_sequence():
    if 'sku_history' in request.args:
        if request.args['sku_history']:
            sku_list = request.args['sku_history'].split(",")
            out = sp.wrap_predict(model,sku_list,seq_len,VOCAB_SIZE,indices_char,char_indices,nb_predic=10)
            out = [{"sku_code": x, "name" : list(sku_df[sku_df["sku_code"]==x].sku_name)[0], "code_short" : list(sku_df[sku_df["sku_code"]==x].code_custom)[0]} for x in out]
            return(json.dumps({"sku_list":out}))
        else:
            return(json.dumps({"sku_list":[]})) 
    
    
    
@app.route("/api/rec_als", methods = ['GET', 'POST'])
@crossdomain(origin='*')
def get_reco_user():
    if 'dream_id' in request.args:
        if request.args['dream_id'] :
            if "sku_history" in request.args:
                to_exclude = request.args['sku_history'].split(",")
                to_exclude = list(set(to_exclude))
            else:
                to_exclude = []
            sku_list = als.wrap_reco(request.args['dream_id'],uid_to_idx,idx_to_mid,user_factors,item_factors,list_sku_exclude=to_exclude)[0:51]
            output = [{"sku_code": x, "sku_name" : list(sku_df[sku_df["sku_code"]==x].sku_name)[0], "sku_url" : list(sku_df[sku_df["sku_code"]==x].code_custom)[0]} for x in sku_list]
            return(json.dumps({"sku_list":output}))
        else:
            return(json.dumps({"sku_list":[]}))
    else:
        return(json.dumps({"sku_list":[]}))    



@app.route("/api/get", methods = ['GET', 'POST'])
@crossdomain(origin='*')
def get_reco():
    if 'sku_history' in request.args:
        if request.args['sku_history']:
            return vr.recommend(request.args['sku_history'],files_list,sim,sku_df,request.args["param"])
            #return als_recommend(request.args['sku_history'],sku_df,idx_to_mid,coef=0.2,param=request.args["param"],correct_error=True)
        else:
            return(json.dumps({"sku_list":[]}))
    if 'context' in request.args:
        rand=np.random.choice(range(0,len(files_list)),150)
        image_names = [files_list[x] for x in rand]
        image_names = [{"sku_code": x, "name" : list(sku_df[sku_df["code_custom"]==x].sku_name)[0]} for x in image_names]
        #image_names = [x.strip(".jpg") for x in image_names]
        return (json.dumps({"sku_list":image_names[0:75],"material_list":material_list,"colour_list":colour_list,"category_list":category_list,"name_list":sku_names})) #garder juste category_list
    if 'context_' in request.args:
        return (json.dumps({"category_list":category_list})) #garder juste category_list
    else:
        return "WHAAAAAAAAAAT?"



@app.route("/api/filter", methods = ['GET', 'POST'])
@crossdomain(origin='*')
def filter_catalog():
    df = sku_df
    if "colour" in request.args:
        colour=request.args['colour']
        if colour:
            df=df[df["color"]==colour]
    else:
        color=None
    if "material" in request.args:
        material = request.args['material']
        if material:
            df = df[df["aesthetic_sub_line"]==material]
    else:
        material=None
    if "category" in request.args:
        category = request.args['category']
        if category:
            df = df[df["custom_category"]==category]
    else:
        category = None
    image_names = list(df["code_custom"])
    #rand=np.random.choice(range(0,len(image_names)),150)
    #image_names = [image_names[x] for x in rand]
    if len(image_names)>75:
        rand=np.random.choice(range(0,len(image_names)),75)
        image_names = [image_names[x] for x in rand]
    else:
        image_names=image_names[0:75]
    image_names = [{"sku_code": x, "name" : list(sku_df[sku_df["code_custom"]==x].sku_name)[0]} for x in image_names]
    return(json.dumps({"sku_list":image_names}))
    