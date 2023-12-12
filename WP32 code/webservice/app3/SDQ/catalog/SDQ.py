from flask import Flask
from flask import jsonify,request
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import numpy as np
import rasterio as rio
from glob import glob
import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
from skimage.metrics import normalized_root_mse as nmse
import math
app = Flask(__name__)







@app.route('/wp3/SDQ', methods=['POST'])
def ndvi1():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        data1=data.get("ID1")
        data2=data.get("ID2")
        data_com=completeness(data1)
        data_clasf1=classification_veg(data1)
        data_clasf2=classification_basic(data1)
        data_clasf3=classification_all(data1)
        data_a=accuracy_l(data1,data2)
        data_r={"completeness":data_com,
                "accuracy":data_a,
                "class1":data_clasf1,
                "class2":data_clasf2,
                "class3":data_clasf3,
                }
        return (data_r)
    
    else:
        return "Content type is not supported."

def classification_basic(data1):
    url = "http://127.0.0.1:105/wp3/classification_basic"
    data={"ID":data1}
    response = requests.post(url, json=data)
    return response

def classification_all(data1):
    url = "http://127.0.0.1:105/wp3/classification_all"
    data={"ID":data1}
    response = requests.post(url, json=data)
    return response

def classification_veg(data1):
    url = "http://127.0.0.1:105/wp3/classification_veg"
    data={"ID":data1}
    response = requests.post(url, json=data)
    return response



def completeness(data1):
    url = "http://127.0.0.1:105/wp3/complete"
    data={"ID":"IMG_DATA/*B?*.jp2"}
    response = requests.post(url, json=data)
    return response


def accuracy_l(data1,data2):
    url = "http://127.0.0.1:105/wp3/accuracy"
    data={"ID1":data1,"ID2":data2 }
    response = requests.post(url, json=data)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)