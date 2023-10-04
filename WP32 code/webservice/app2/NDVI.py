from flask import Flask
from flask import jsonify,request
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import numpy as np
import rasterio as rio
from glob import glob

app = Flask(__name__)



@app.route("/im_size", methods=["POST"])
def process_image():
    band3 = request.files['band3']
    band7 = request.files['band7']
    rio.save
    band3.save('b31.jp2')
    band7.save('b71.jp2')
    b3=rio.open('b31.jp2', 'r')
    b7=rio.open('b71.jp2', 'r')
    ndvi1 = es.normalized_diff(b7, b3)
    
    return jsonify({'msg': 'success'})




@app.route('/wp3/ndvi', methods=['POST'])
def ndvi1():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        #print(data.get('l7'))
        #print(data.get('l3'))
        b3=np.array(data.get('band3'))
        b7=np.array(data.get('band7'))
        print(np.array(data.get('band1')).shape)
        print(np.array(data.get('band7')).shape)

        ndvi1 = es.normalized_diff(b7, b3)
        ndv1= ndvi1.tolist()
        data={"ndvi":ndvi}
        return (ndvi)
    
    else:
        return "Content type is not supported."

    
@app.route('/wp3/ndvi1', methods=['POST'])
def ndvi12():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        id=str(data.get('ID'))
        print(id)
        k=get_data(id)
        b3=k[0]
        b7=k[1]
        print(b3.shape)
        print(b7.shape)
        ndvi1 = es.normalized_diff(b7, b3)
        print(ndvi1)
        P= ndvi1.tolist()
        data={"ndvi":P}
        print(ndvi1.shape)
        return (data)
    else:
        return "Content type is not supported."


def get_data(id):
    S_sentinel_bands = glob(id)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)