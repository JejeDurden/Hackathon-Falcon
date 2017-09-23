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
import operator

##------------------------------------------------------------##
#set env

#read files



#var

##------------------------------------------------------------##
#functions


def recommend_user(uid,user_factors,item_factors):
    return user_factors[uid,:].dot(item_factors.T)

def wrap_reco(dream_id,uid_to_idx,idx_to_mid,user_factors,item_factors,list_sku_exclude=[]):
    uid = uid_to_idx[dream_id]
    reco = recommend_user(uid,user_factors,item_factors)
    sku = idx_to_mid.values()
    dic = {key :value for (key,value) in zip(sku,reco)}
    dic = sorted(dic.items(), key=operator.itemgetter(1),reverse=True)
    dic = [x[0] for x in dic if x[0] not in list_sku_exclude]
    return dic        