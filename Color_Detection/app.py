from flask import Flask, render_template, request, json
import random
import os, io, re, cv2, base64
from PIL import Image
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/detect", methods=['POST', 'GET'])
def detect():
    data = json.loads(request.data)
    color = data.get('color')
    # Converting to Image
    image_data = re.sub('^data:image/.+;base64,', '', data.get('image'))
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))
    # Converting to Opencv Format
    cv_image = np.array(image)
    image_processed = color_detect(color, cv_image)
    # Converting Again to base64
    retval, buffer = cv2.imencode('.jpg', image_processed)
    image_64_encode = base64.b64encode(buffer)
    # Converting to URL
    image_return = "data:image/jpg;base64,"+image_64_encode.decode("utf-8") 
    return json.dumps({'status':'OK','color':color, 'image':image_return});


def color_detect(color, image):
    if color == 'Blue':
        lower_hue = np.array([109, 0, 0])
        upper_hue = np.array([122, 255, 255])
    if color == 'Purple':
        lower_hue = np.array([130, 0, 0])
        upper_hue = np.array([150, 255, 255])
    if color == 'Green':
        lower_hue = np.array([50, 0, 0])
        upper_hue = np.array([75, 255, 255])
    if color == 'Red':
        lower_hue = np.array([170, 0, 0])
        upper_hue = np.array([179, 255, 255])
    if color == 'Orange':
        lower_hue = np.array([1, 0, 0])
        upper_hue = np.array([20, 255, 255])
    if color == 'Yellow':
        lower_hue = np.array([21, 0, 0])
        upper_hue = np.array([45, 255, 255])
    if color == 'Brown':
        lower_hue = np.array([1, 0, 0])
        upper_hue = np.array([32, 83, 83])
    if color == 'Pink':
        lower_hue = np.array([142, 0, 0])
        upper_hue = np.array([165, 255, 255])
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_hue, upper_hue)
    result = cv2.bitwise_and(image, image, mask=mask)
    return result
    
    
if __name__ == "__main__":
    app.run(debug=True)