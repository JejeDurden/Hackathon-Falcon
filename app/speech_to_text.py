#!/usr/bin/env python
# -*- coding: utf-8 -*-

##------------------------------------------------------------##
'''
    File name: speech_to_text.py
    Author: Paul Duc-Vinh TRAN
    E-Mail : dvp.tran@gmail.com
    Date created: 11/09/2017
    Date last modified: 11/09/2017
    Python Version: 2.7
'''

##------------------------------------------------------------##
#Imports


import httplib, json, urllib

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

def speech_to_text(file_name):
    #In input the file name with or without file extension i.e : .wav are safe, in string format.
    #The file must be in current directory
    #Output a string.
    
    clientId = "paul"
    clientSecret = "0df92168a0af458495d99748dd1c81ad"
    ttsHost = "https://speech.platform.bing.com"

    params = urllib.urlencode({'grant_type': 'client_credentials', 'client_id': clientId, 'client_secret': clientSecret, 'scope': ttsHost})

    #print ("The body data: %s" %(params))

    headers = {"Content-type": "application/x-www-form-urlencoded"}

    AccessTokenHost = "oxford-speech.cloudapp.net"
    path = "/token/issueToken"

    # Connect to server to get the Oxford Access Token
    conn = httplib.HTTPSConnection(AccessTokenHost)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    #print(response.status, response.reason)

    data = response.read()
    conn.close()
    accesstoken = data.decode("UTF-8")
    #print ("Oxford Access Token: " + accesstoken)

    #decode the object from json
    ddata=json.loads(accesstoken)
    access_token = ddata['access_token']

    # Read the binary from wave file
    if '.wav' in file_name:
        f=file_name
    else:
        f=file_name+'.wav'
    
    try:
        f = open(f,'rb')
    except:
        print('File not found.')
        return None
    try:
        body = f.read();
    finally:
        f.close()

    headers = {"Content-type": "audio/wav; samplerate=8000",
    "Authorization": "Bearer " + access_token}

    #Connect to server to recognize the wave binary
    try:
        conn = httplib.HTTPSConnection("speech.platform.bing.com")
        conn.request("POST", "/recognize/query?scenarios=ulm&appid=D4D52672-91D7-4C74-8AD8-42B1D98141A5&locale=fr-fr&device.os=wp7&version=3.0&format=json&requestid=1d4b6030-9099-11e0-91e4-0800200c9a66&instanceid=1d4b6030-9099-11e0-91e4-0800200c9a66", body, headers)
        response = conn.getresponse()
        #print(response.status, response.reason)
        data = response.read()
        #print(data)
        conn.close()
        px = Payload(data)
        print(px.header["lexical"])
        return px.header["lexical"]
    except Exception,e:
        print(e)
        print('Could not deliver answer.')