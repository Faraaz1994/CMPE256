import numpy as np
from flask import Flask,request
from flask_cors import CORS, cross_origin
from model import trainModel
from sklearn import preprocessing
import matplotlib.pyplot as plt
import matplotlib.image as matimage
import matplotlib.cm as cm
import cv2
from string import ascii_lowercase,ascii_uppercase
import pprint
import heapq
import json
from flask import send_file
import time


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model = trainModel()

@app.route("/")
@cross_origin()
def helloWorld():
  return "Works!!"


@app.route("/predict", methods=['POST'])
@cross_origin()
def predict():
  image,filename = createBinaryMatrix(request.json['points'],request.json['width'],request.json['height'])
  #image = normalize(image)
  image = image.reshape(1,64,64,1)
  prediction_values = model.predict(image)[0]
  char_map = getcharmap()
  top5 = heapq.nlargest(3, range(len(prediction_values)), prediction_values.__getitem__)
  predictions = {}
  for index in top5:
    char = getchar(index,char_map)
    probability = str(prediction_values[index])
    print("Character : ",char," value : ",probability)
    predictions[char] = probability
  response = {}
  response['predictions'] = predictions
  response['filename'] = filename
  return json.dumps(response)


def getchar(cls,char_map):
  return str(char_map[cls])

def getcharmap():
  char_map = dict()
  for i in range(10):
    char_map[i] = i

  index = 10
  for c in ascii_uppercase:
    char_map[index] = c
    index += 1

  for c in ascii_lowercase:
    char_map[index] = c
    index += 1
  return char_map

def normalize(data):
  data -= data.mean()
  return data

def createBinaryMatrix(points,width,height):
  image = np.ones((width,height),dtype=int)
  for point in points:
    x = int(point['x'])
    y = int(point['y'])
    image[y][x] = 0
    setNeighbours(x,y,image)
  seconds = str(int(time.time()))
  filename = 'static/digit_pre'+seconds+'.png'
  plt.imsave('static/digit_raw.png', image, cmap=cm.gray) 
  image = cv2.resize(image.astype('float32'),(64,64))
  plt.imsave(filename, image, cmap=cm.gray)
  return (image,filename)

def setNeighbours(cx,cy,image):
  x = np.arange(0, 400)
  y = np.arange(0, 400)
  r = 25
  mask = (x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2 < r**2
  image[mask] = 0  

if __name__ == '__main__':
  app.run(debug=True,threaded=False)
  
  





#flask run --without-threads --host=0.0.0.0
'''
Character       Class
0                 0
9                 9
A                 10
Z                 35
a                 36
z                 61
'''