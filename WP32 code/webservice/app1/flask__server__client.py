################################################################################
### server.py
################################################################################

#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
Dummy server, interacts with the client receiving, altering and returning
compressed numpy arrays.

Setup/run:
 1. pip install Flask --user
 2. export FLASK_APP=server.py; flask run
"""

import io
import zlib

from flask import Flask, request, Response
import numpy as np


# ## CONFIG

SERVER_HOST= "localhost"
SERVER_PORT = 12345
API_PATH = "/api/test"

# ## HELPERS

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
    return np.load(io.BytesIO(zlib.decompress(bytestring)))



# ## MAIN SERVER DESCRIPTOR/ROUTINE

# Initialize the Flask application
app = Flask(__name__)

# route http posts to this method
@app.route(API_PATH, methods=['POST'])
def test1234():
    """
    Expects a compressed, binary np array. Decompresses it, multiplies it by 10
    and returns it compressed.
    """
    r = request
    #
    data = uncompress_nparr(r.data)
    #
    data10 = data*10
    print("\n\nReceived array (compressed size = "+\
          str(r.content_length)+"):\n"+str(data))
    resp, _, _ = compress_nparr(data10)
    return Response(response=resp, status=200,
                    mimetype="application/octet_stream")


# start flask app
app.run(host=SERVER_HOST, port=SERVER_PORT)



################################################################################
### client.py
################################################################################


#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
Dummy client, interacts with the server sending and receiving
compressed numpy arrays.

Run:
python client.py
"""


from __future__ import print_function
import io
import numpy as np
import zlib
import requests


# ## CONFIG

SERVER_HOST= "localhost"
SERVER_PORT = 12345
API_PATH = "/api/test"


# ## HELPERS

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
    return np.load(io.BytesIO(zlib.decompress(bytestring)))


# ## MAIN CLIENT ROUTINE

url = "http://"+SERVER_HOST+":"+str(SERVER_PORT)+API_PATH
while True:
    raw_input("\n\npress return...")
    arr = np.random.rand(3,3)
    compressed, u_sz, c_sz = compress_nparr(arr)
    #
    print("\nsending array to", url)
    print("size in bits (orig, compressed):", u_sz, c_sz)
    print(arr)
    #
    resp = requests.post(url, data=compressed,
                         headers={'Content-Type': 'application/octet-stream'})
    #
    print("\nresponse:")
    data = uncompress_nparr(resp.content)
    print(data)
