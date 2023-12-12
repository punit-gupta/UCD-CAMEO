
from flask import Flask
from flask import jsonify,request
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import numpy as np
import rasterio as rio
from glob import glob
import matplotlib.pyplot as plt
import requests
import urllib3
import json

def metadata(metadataid):
    urllib3.disable_warnings()
    from flask import jsonify
    url = "https://10.11.2.101:31010/cameo/metadata/"+metadataid
    data={
    "username": "ucd-wp3-user",
    "password": "U(dWp3u$3r24"
    }
    response = requests.get(url=url,verify=False, json=data)
    if response.status_code ==200:
        print(response.json())
    else:
        print(response.status_code)
    
    jsonResponse = json.dumps(response.json())
    return jsonResponse

def data(dataid):
    urllib3.disable_warnings()
    from flask import jsonify
    url = "https://10.11.2.101:31010/cameo/data/"+dataid
    data={
    "username": "ucd-wp3-user",
    "password": "U(dWp3u$3r24"
    }
    response = requests.get(url=url,verify=False, json=data)
    if response.status_code ==200:
        print(response.json())
    else:
        print(response.status_code)
    
    jsonResponse = json.dumps(response.json())
    return jsonResponse

def search(data):
    urllib3.disable_warnings()
    from flask import jsonify
    url = "https://10.11.2.101:31010/cameo/search"
    
    response = requests.get(url=url,verify=False, json=data)
    if response.status_code ==200:
        print(response.json())
    else:
        print(response.status_code)
    
    jsonResponse = json.dumps(response.json())
    return jsonResponse

def unzip(id):
    import  zipfile
    import os
    #files="S2A_MSIL1C_20230520T114351_N0509_R123_T29ULS_20230520T151921.zip"
    zip_ref = zipfile.ZipFile(id, 'r')
    zip_ref.extractall(os.path.dirname(id))
    zip_ref.close()
    print(os.path.abspath(files))