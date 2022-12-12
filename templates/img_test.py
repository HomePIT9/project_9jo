from builtins import sorted
bb
import hashlib
import jwt
import gridfs
from operator import itemgetter
from datetime import datetime
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, make_response

app = Flask(__name__)

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.jftxkcu.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.homefit

# client = MongoClient('mongodb+srv://test:sparta@cluster0.qcokm6l.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
# db = client.dbsparta

SECRET_KEY = 'SPARTA'


@app.route("/upload", methods=['POST'])
def upload():
    ## file upload ##
    img = request.files['image']

    ## GridFs를 통해 파일을 분할하여 DB에 저장하게 된다
    fs = gridfs.GridFS(db)
    fs.put(img, filename='name')

    ## file find ##
    data = client.grid_file.fs.files.find_one({'filename': 'name'})

    ## file download ##
    my_id = data['_id']
    outputdata = fs.get(my_id).read()
    output = open('./images/' + 'back.jpeg', 'wb')
    output.write(outputdata)
    return jsonify({'msg': '저장에 성공했습니다.'})



if __name__ == '__main__':
    app.run('0.0.0.0', port=1000, debug=True)
