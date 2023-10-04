from flask import Flask
from flask import jsonify,request
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import numpy as np
import rasterio as rio
from glob import glob


app = Flask(__name__)


    
@app.route('/wp3/classification_basic', methods=['POST'])
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
        m,ndvi_landsat_class=basic_classification(ndvi)
        data=b_classification(ndvi,m)
        
        print(ndvi.shape)
        return (data)
    else:
        return "Content type is not supported."


@app.route('/wp3/classification_basic1', methods=['POST'])
def complete1():
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
        m,ndvi_landsat_class=basic_classification(ndvi)

        data=b_classification(ndvi,m)
        data={"classes":data,
               "image":ndvi_landsat_class.tolist()}
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


def b_classification(ndvi1,m):
    # Calculate forest and water masks based on the thresholds
    total_mask = ndvi1.size

    concrete_percentage     =(m[0]/total_mask) * 100
    green_percentage    	=(m[1]/ total_mask) * 100
    water_percentage        =(m[2] / total_mask) * 100

    print("sssss")
    print(f"Concrete Percentage:{concrete_percentage:.2f}%")
    print(f"Green Percentage: {green_percentage:.2f}%")
    print(f"Water Percentage: {water_percentage:.2f}%")
    print("sssss")

    data={"Concrete_Percentage":concrete_percentage,
          "Green_Percentage": green_percentage,
          "Water_Percentage":water_percentage,
          }
    return data


def basic_classification(ndvi1):
    # Create classes and apply to NDVI results
    #ndvi_class_bins = [-1, 0, 0.1, 0.25, 0.4, 1]
    ndvi_class_bins = [-1, 0, 0.2, 1]
    ndvi_landsat_class = np.digitize(ndvi1, ndvi_class_bins)

    # Apply the nodata mask to the newly classified NDVI data
    ndvi_landsat_class = np.ma.masked_where(
        np.ma.getmask(ndvi1), ndvi_landsat_class
    )
    print(np.unique(ndvi_landsat_class))
    # Get list of classes
    classes, m = np.unique(ndvi_landsat_class,return_counts=True)
    print(classes)
    print(m)
    classes = classes.tolist()
    # The mask returns a value of none in the classes. remove that
    classes = classes[0:3]
    print("eee")
    return m,ndvi_landsat_class


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)