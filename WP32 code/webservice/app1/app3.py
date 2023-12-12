from flask import Flask
from flask import jsonify,request,Response
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import numpy as np
import rasterio as rio
import json

app = Flask(__name__)

import zlib
import io
def compress_nparr(nparr):
    """
    Returns the given numpy array as compressed bytestring,
    the uncompressed and the compressed byte size.
    """
    bytestream = io.BytesIO()
    np.save(bytestream, nparr)
    uncompressed = bytestream.getvalue()
    compressed = zlib.compress(uncompressed)
    return compressed, len(uncompressed), len(compressed)

def uncompress_nparr(bytestring):
    """
    """
    return io.BytesIO(zlib.decompress(bytestring))



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
        #print(data.get('l7'))
        #print(data.get('l3'))
        b3=np.array(data.get('band3'))
        b7=np.array(data.get('band7'))
        print(np.array(data.get('band1')).shape)
        print(np.array(data.get('band7')).shape)
        ndvi1 = es.normalized_diff(b7, b3)
        P= ndvi1.tolist()
        data={"ndvi":P}
        return (data)
    else:
        return "Content type is not supported."
    

@app.route('/wp3/ndvi2', methods=['POST'])
def ndvi13():
    content_type = request.headers.get('Content-Type')
    data = request.data
    #print(data.get('l7'))
    #print(data.get('l3'))
    
    data = uncompress_nparr(data)
    #data10 = data*10
    print("\n\nReceived array (compressed size = "+str(request.content_length)+"):\n"+str(data))
    resp, _, _ = compress_nparr(data)
    return Response(response=resp, status=200,
                    mimetype="application/octet_stream")
    

@app.route('/wp3/complete', methods=['POST'])
def complete():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        #print(data.get('l7'))
        #print(data.get('l3'))
        b3=np.array(data.get('band3'))
        b7=np.array(data.get('band7'))
        print(np.array(data.get('band1')).shape)
        print(np.array(data.get('band7')).shape)
        ndvi = es.normalized_diff(b7, b3)
        v1=np.array(ndvi[0])
        unique, frequency = np.unique(v1,return_counts = True)
        no_data=100*(np.count_nonzero(np.isnan(v1))/len(v1))
        data={"no_data":no_data}
        return (data)
    
    else:
        return "Content type is not supported." 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)