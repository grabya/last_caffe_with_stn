import os
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

from flask import Flask
from flask import jsonify 

app = Flask(__name__)

caffe_root = './caffe-master/' 
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

mean_filename='./mean.binaryproto'
proto_data = open(mean_filename, "rb").read()
a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
mean  = caffe.io.blobproto_to_array(a)[0]

age_net_pretrained='./age_net.caffemodel'
age_net_model_file='./deploy_age.prototxt'
age_net = caffe.Classifier(age_net_model_file, age_net_pretrained,
                       mean=mean,
              host='0.0.0.0'         channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

gender_net_pretrained='./gender_net.caffemodel'
gender_net_model_file='./deploy_gender.prototxt'
gender_net = caffe.Classifier(gender_net_model_file, gender_net_pretrained,
                       mean=mean,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

age_list=['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)']
gender_list=['Male','Female']

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/analyze/<string:url>', methods=['GET'])
def analyze(url):
    input_image = caffe.io.load_image(example_image)
    prediction = age_net.predict([input_image]) 
    age = age_list[prediction[0].argmax()]
    print 'predicted age:', age
    prediction = gender_net.predict([input_image]) 
    gender = gender_list[prediction[0].argmax()]
    print 'predicted gender:', gender
    return jsonify({'age': age, 'gender': gender})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
