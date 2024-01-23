import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import keras
import io
from numpy import argmax, expand_dims, float32
import keras.utils as image
from keras.models import load_model
from keras.applications.vgg16 import VGG16
from keras.layers import Dropout

from flask import Flask, request, jsonify
from flask_cors import CORS

# Import model
model = load_model("model_fc.h5")
pre_model = VGG16(include_top=False, weights='imagenet')

# Add Dropout to the fully connected layers of your model with a unique name
model.add(Dropout(0.5, name="custom_dropout"))  # You can adjust the dropout rate as needed


# Prediction function
def predict(x):
    img = image.load_img(x, target_size=(224, 224))
    img = image.img_to_array(img)
    img = img.astype(float32) / 255
    img = expand_dims(img, axis=0)
    bt_prediction = pre_model.predict(img)
    pred = model.predict(bt_prediction)
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

            # Check for overfitting (you can adjust the threshold as needed)
            confidence_percentage = 0.62
            max_confidence = max(prediction[0])



            if max_confidence < confidence_percentage:
                warning_message = f"Warning: High confidence ({max_confidence:.2f}) in the prediction. May indicate overfitting."
                return jsonify({"prediction": "Unknown", "warning": warning_message})

            class_name = ['Airplane', 'Bicycle', 'Bus', 'Car', 'Helicopter', 'Motorcycle', 'Ship', 'Tractor', 'Train',
                          'Truck']
            pred = class_name[argmax(prediction)]
            data = {"prediction": pred}
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
