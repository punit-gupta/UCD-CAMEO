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






    
@app.route('/wp3/complete', methods=['POST'])
def complete():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        id=data.get("ID")
        k=get_data(id)
        b3=k[1]
        b7=k[0]
        print(b3.shape)
        print(b7.shape)
        ndvi1 = es.normalized_diff(b7, b3)
        v1=np.array(ndvi1[0])
        unique, frequency = np.unique(v1,return_counts = True)
        no_data=100*(np.count_nonzero(np.isnan(v1))/len(v1))
        data={"no_data":no_data}
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