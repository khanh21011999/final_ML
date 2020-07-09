from flask import Flask, request, render_template
from keras.models import load_model
import tensorflow as tf
import numpy as np
import cv2

from PIL import Image



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('CNN2.html')

@app.route('/classify', methods=['POST'])
def predict():
    model = tf.keras.models.load_model('../trained-model.h5', compile=False)

    try:
        #Processing input
        IMG_SIZE = 30

        #Save image to input.jpg to read
        img = request.files['imageFile']
        img.save('input.jpg')
        img_array = cv2.imread("input.jpg")
        #img_array=img_array/255
        new_array = cv2.resize(img_array, (IMG_SIZE,IMG_SIZE))
        image = new_array.reshape(1, IMG_SIZE, IMG_SIZE, 3)
        
        predict = model.predict(image)
        predict_class = CATEGORIES[np.argmax(predict)]

        if (predict_class == 'Human'):
           message = 'Congrats, you are one of us! \n Click somewhere to proceed...'
        else:
           message = 'Nooo, you upload a photo of  ' + predict_class + '.I thought you are human,not ' + predict_class + ', Please use real image :)' 

        print(predict_class)

    except Exception as e:
        #Store error to pass to the web page
        message = "ErrorClass: {}, Argument: {} and Traceback details are: {}".format(e.__class__,e.args,e.__doc__)
        predict_class = "Error."
        print(message)

    return render_template('CNN2.html', message=message, predict_class=predict_class)