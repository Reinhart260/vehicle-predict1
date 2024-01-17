import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


import keras
import io
from numpy import argmax, expand_dims, float32
import keras.utils as image

from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.applications.vgg16 import VGG16

         # use it without `open()`
# Import model
model = keras.models.load_model("model_fc.h5")
pre_model = VGG16(include_top=False, weights='imagenet')

# Prediction function
def predict(x):
    img = image.load_img(x, target_size=(224,224))
    img = image.img_to_array(img)
    img = img.astype(float32) / 255
    img = expand_dims(img, axis=0)
    bt_prediction = pre_model.predict(img)
    pred= model.predict(bt_prediction)
    return pred

# Initialize Flask server with error handling
app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
            image_bytes = file.read()
            img = io.BytesIO(image_bytes)
            prediction = predict(img)
            class_name = ['Airplane', 'Bicycle', 'Bus', 'Car', 'Helicopter', 'Motorcycle', 'Ship', 'Tractor', 'Train', 'Truck']
            pred = class_name[argmax(prediction)]
            data = {"prediction": pred}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"





if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))