from flask import Flask
from flask import jsonify,request
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import numpy as np
import rasterio as rio
from glob import glob


app = Flask(__name__)


    
@app.route('/wp3/classification_veg', methods=['POST'])
def complete():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        id=str(data.get('ID'))
        print(id)
        k=get_data(id)
        b3=k[1]
        b7=k[0]
        print(b3.shape)
        print(b7.shape)
        ndvi = es.normalized_diff(b7, b3)
        m=veg_classification(ndvi)
        data=v_classification(ndvi,m)
        print(ndvi.shape)
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

def veg_classification(ndvi1):
    # Create classes and apply to NDVI results
    ndvi_class_bins = [-1, 0, 0.1, 0.25, 0.4, 1]
    ndvi_landsat_class = np.digitize(ndvi1, ndvi_class_bins)

    # Apply the nodata mask to the newly classified NDVI data
    ndvi_landsat_class = np.ma.masked_where(
        np.ma.getmask(ndvi1), ndvi_landsat_class
    )

    # Get list of classes
    classes,m  = np.unique(ndvi_landsat_class,return_counts=True)
    classes = classes.tolist()
    # The mask returns a value of none in the classes. remove that
    classes = classes[0:5]
    return m

def v_classification(ndvi1,m):
    # Calculate forest and water masks based on the thresholds
    total_mask = ndvi1.size

    c1=(m[0]/total_mask) * 100
    c2=(m[1]/ total_mask) * 100
    c3=(m[2] / total_mask) * 100
    c4=(m[3] / total_mask) * 100
    c5=(m[4] / total_mask) * 100

    print(f"No Vegetatio Percentage:{c1:.2f}%")
    print(f"Bare Area Percentage: {c2:.2f}%")
    print(f"Low Vegetation Percentage: {c3:.2f}%")
    print(f"Moderate Vegetation Percentage: {c4:.2f}%")
    print(f"High Vegetation Percentage: {c5:.2f}%")
    
    data={"No_veg":c1,
          "Bare_area":c2,
          "low_veg":c3,
          "Moderate Veg":c4,
          "high_veg":c5 }
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)