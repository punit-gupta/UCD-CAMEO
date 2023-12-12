from flask import Flask
from flask import jsonify,request
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import numpy as np
import rasterio as rio
from glob import glob
import cv2
import urllib3
import json
import boto3
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
from skimage.metrics import normalized_root_mse as nmse
import math
from dell import *
from landsat import *
import landsat as sdq
app = Flask(__name__)








@app.route('/wp3/SDQ', methods=['POST'])
def ndvi1():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        id=data.get("ID")
        print("metadata")
        json1= metadata(id) #landsat
        strj=str(json1)
        #print(strj)
        json_object = json.loads(strj)
        print(json_object["data_id"])
        data_id=json_object["data_id"]
        print("data")
        json1= data(data_id)
        json_object1 = json.loads(json1)
        strs=json_object1["data_s3_link"]
        
        res = strs.split('y/')[1]
        #res
        print("download")
        s3 = boto3.client('s3',
                  endpoint_url="http://10.11.1.100:80",
                  use_ssl=False,
                  aws_access_key_id='ucd-wp3-usr',
                  aws_secret_access_key='U53r-uCdwp3',
                  region_name='us-east-1')
        
        files=res+'.zip'
        print (files)
        s3.download_file('repository',files,files)
        
        unzip(files)

        res="LC08_L2SP_206023_20230513_20230518_02_T1"
        comple = sdq.complete_l(res)
        veg_c  = sdq.veg_class_l(res)
        basic_c= sdq.basic_class_l(res)
        data_r="{}"+comple+veg_c+basic_c+"}"
        return (data_r)
    
    else:
        return "Content type is not supported."




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)