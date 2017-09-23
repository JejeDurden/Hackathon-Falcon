#!/usr/bin/env python
# -*- coding: utf-8 -*-

##------------------------------------------------------------##
'''
    File name: recast.py
    Author: Paul Duc-Vinh TRAN
    E-Mail : dvp.tran@gmail.com
    Date created: 11/09/2017
    Date last modified: 11/09/2017
    Python Version: 2.7
'''

##------------------------------------------------------------##
import recastai
    
    
def get_intent(text,lang="fr"):
    client = recastai.Client('f355b23fca612aba830c8754ee57c8c0', lang)
    response = client.request.analyse_text(text)
    return response

def action(response):
    if response.intent.slug == 'YOUR_EXPECTED_INTENT':
        #"""Do your code..."""
        return
    return