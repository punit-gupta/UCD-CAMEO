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







@app.route('/wp3/accuracy', methods=['POST'])
def ndvi1():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        data1=data.get("ID1")
        data2=data.get("ID2")
        datar=accuracy_l(data1,data2)
        return (datar)
    
    else:
        return "Content type is not supported."





def get_data(id):
    S_sentinel_bands = glob(id)
    #S_sentinel_bands = glob("jaipur_1/L1C_T43REK_A038140_20221011T053331/S2A_MSIL1C_20221011T052741_N0400_R105_T43REK_20221011T072632.SAFE/GRANULE/L1C_T43REK_A038140_20221011T053331/IMG_DATA/*B?*.jp2")
    S_sentinel_bands.sort()
    from rasterio.windows import Window
    f=rio.open(S_sentinel_bands[3], 'r')
    print(f.shape)
    f1=rio.open(S_sentinel_bands[7], 'r')
    print(f1.shape)
    k=[]
    k.append(f.read(1))
    k.append(f1.read(1))
    return k


def accuracy_l(s1,s2):
    arr_st1 = read_land(s1)
    arr_st2 = read_land(s2)
    print(str(len(arr_st1))+"-"+str(len(arr_st2)))
    print("Peak Signal-to-Noise Ratio (PSNR)")
    psnr="{"
    for i in range(0,len(arr_st1)-1):
        ps=cv2.PSNR(arr_st1[i],arr_st2[i])
        if(i==0):
            psnr+= "Band"+str(i)+":"+str(ps)
        else:
            psnr+= ",Band"+str(i)+":"+str(ps)
        print("Noise Data 1 -Data 2")
        print("Noise Band "+str(i)+": "+str(ps)+"%")
    psnr+= "}"
    print(psnr)

    print("Structural Similarity Index Measure (SSIM)") 
    ssi="{"
#    for i in range(0,len(arr_st1)-1): 
#        ss=  ssim(arr_st1[i],arr_st2[i])
#        ssi+= "\nBand"+str(i)+":"+str(ss)
#        print("SSIM Data 1 -Data 2")
#        print("SSIM Band "+str(i)+": "+str(ss)+"%")
    ssi+= "}"
    print(ssi)

    print("Root mean square error (RMSE)") 
    rms="{"
    for i in range(0,len(arr_st1)-1): 
        rs=math.sqrt(mse(arr_st1[i],arr_st2[i]))
        if(i==0):
            rms+= "Band"+str(i)+":"+str(rs)
        else:
            rms+= ",Band"+str(i)+":"+str(rs)
        print("RMSE Data 1 -Data 2")
        print("RMSE Band "+str(i)+": "+str(rs)+"%")
    rms+="}"
    print(rms)
    
    print("Mean square error (MSE)") 
    mse1="{"
    for i in range(0,len(arr_st1)-1):  
        ms=mse(arr_st1[i],arr_st2[i])
        if(i==0):
            mse1+="Band"+str(i)+":"+str(ms)
        else:
            mse1+=",Band"+str(i)+":"+str(ms)
        print("MSE Data 1 -Data 2")
        print("MSE Band "+str(i)+": "+str(ms)+"%")
    mse1+="}"
    print(mse1)

    print("Normalized  mean square error (NMSE)") 
    nmse1="{"
    for i in range(0,len(arr_st1)-1):  
        nm=nmse(arr_st1[i],arr_st2[i])
        if(i==0):
            nmse1+="Band"+str(i)+":"+str(nm)  
        else:
            nmse1+=",Band"+str(i)+":"+str(nm) 
        print("NMSE Data 1 -Data 2")
        print("NMSE Band "+str(i)+": "+str(nm)+"%")
    nmse1+="}"
    print(nmse1)
    data={"PSNR":psnr,
          "SSIM":ssi,
          "RMSE":rms,
          "NMSE":nmse1,
          "MSE":mse1}
    return data

def read_land(a):
    S_sentinel_bands = glob(a)
    S_sentinel_bands.sort()
    print(S_sentinel_bands)
    l = []
    for i in S_sentinel_bands:
        with rio.open(i, 'r') as f:
            l.append(f.read(1))
         
    return l

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)