from flask import Flask
from flask import request, redirect
from flask import jsonify
from flask_cors import CORS, cross_origin

import cv2
from keras.models import load_model
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)


model=tf.keras.models.load_model('trained-model.h5',compile=False)

def prepare(image):
    IMG_SIZE=30
    new_array= cv2.resize(np.float32(image),(IMG_SIZE,IMG_SIZE))
    return new_array.reshape(1,IMG_SIZE,IMG_SIZE,3)

def detail(classid):
  switcher={
      0:'Speed limit (20km/h)',
      1:'Speed limit (30km/h)',
      2:'Speed limit (50km/h)',
      3:'Speed limit (60km/h)',
      4:'Speed limit (70km/h)',
      5:'Speed limit (80km/h)',
      6:'End of speed limit (80km/h)',
      7:'Speed limit (100km/h)',
      8:'Speed limit (120km/h)',
      9:'No passing',
      10:'No passing for vechiles over 3.5 metric tons',
      11:'Right-of-way at the next intersection',
      12:'Priority road',
      13:'Yield',
      14:'Stop',
      15:'No vechiles',
      16:'Vechiles over 3.5 metric tons prohibited',
      17:'No entry',
      18:'General caution',
      19:'Dangerous curve to the left',
      20:'Dangerous curve to the right',
      21:'Double curve',
      22:'Bumpy road',
      23:'Slippery road',
      24:'Road narrows on the right',
      25:'Road work',
      26:'Traffic signals',
      27:'Pedestrians',
      28:'Children crossing',
      29:'Bicycles crossing',
      30:'Beware of ice/snow',
      31:'Wild animals crossing',
      32:'End of all speed and passing limits',
      33:'Turn right ahead',
      34:'Turn left ahead',
      35:'Ahead only',
      36:'Go straight or right',
      37:'Go straight or left',
      38:'Keep right',
      39:'Keep left',
      40:'Roundabout mandatory',
      41:'End of no passing',
      42:'End of no passing by vechiles over 3.5 metric tons'
  }
  return switcher.get(classid,"Invalid")

@app.route("/predict", methods=['GET','POST'])

def predict():
    data =request.files["inpFile"]
    image = Image.open(request.files["inpFile"])
    image = np.array(image)
    predict=model.predict([prepare(image)])
    #pred_name = CATEGORIES[np.argmax(predict)]
    pred_name =  detail(np.argmax(predict))   
    response = {'finalResult' : pred_name}
    print(response) 
    return jsonify(response)
    
app.run()
