#!/usr/bin/env python
# -*- coding: utf-8 -*-

##------------------------------------------------------------##
#Imports

import numpy as np
import json
import pandas as pd

##------------------------------------------------------------##
#functions
def get_similar(sim,files_list, idx, N=10):
    row = sim[idx, :]
    out = []
    coef = []
    for x in np.argsort(-row)[:N]:
        out.append(files_list[x])
        coef.append(sim[idx, x])
    return out,coef

#compute
def compute(files_list,sim,sku_history,N=100):
    #compute visual sim
    index_history =[files_list.index(x) for x in sku_history]
    temp_df= pd.DataFrame()
    a_l,b_l=[],[]
    for element in index_history:
        a,b = get_similar(sim,files_list,element,N)
        a_l=a_l+a
        b_l=b_l+b
    temp_df['reco'] = a_l
    temp_df['score']= b_l

    #remove already seen items:
    temp_df = temp_df[~temp_df['reco'].isin([x for x in sku_history])]
    temp_df = temp_df.groupby('reco').mean().sort_values('score',ascending=False)
    #print(temp_df)
    return temp_df

def recommend(sku_,files_list,sim,sku_df,param=None):
    #visual reco
    sku_=sku_.split(",")
    output=compute(files_list,sim,sku_,14027).reset_index()
    output= list(output.reco)
    output_ = output[0:50]
    output_ = [{"sku_code": x, "name" : list(sku_df[sku_df["code_custom"]==x].sku_name)[0],"code_short":list(sku_df[sku_df["code_custom"]==x].sku_code)[0]} for x in output_]
    #output = [x.strip(".jpg") for x in output]
    if param:
        a=sku_df.set_index("code_custom").reindex(output)
        a=a.reset_index()
        out=list(a[a["custom_category"]==param]['code_custom'])[0:50]
        out = [{"sku_code": x, "name" : list(sku_df[sku_df["code_custom"]==x].sku_name)[0], "code_short":list(sku_df[sku_df["code_custom"]==x].sku_code)[0]} for x in out]
        #out = [x for x in output if x in out]
        return(json.dumps({"sku_list":out,"explanation" : "Model : Visual Recommendation, if Collaborative filtering chosen, it means that selected SKUs are not considered in C.F mode."}))
    else:
        return(json.dumps({"sku_list":output_,"explanation" : "Model : Visual Recommendation, if Collaborative filtering chosen, it means that selected SKUs are not considered in C.F mode."}))
    #return(str(output))
