import os
import pickle
from reverseProxy import proxyRequest
from flask import Flask, render_template, request, send_file
from classifier import get_prediction

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

MODE = os.getenv('FLASK_ENV')
DEV_SERVER_URL = 'http://localhost:3000/'

app = Flask(__name__)

# Ignore static folder in development mode.
if MODE == "development":
    app = Flask(__name__, static_folder=None)

# Load the model from the pickle file
with open('../facial_keypoints.p', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
@app.route('/<path:path>')
def index(path=''):
    if MODE == 'development':
        return proxyRequest(DEV_SERVER_URL, path)
    else:
        return render_template("index.html") 

@app.route('/predict', methods=['POST'])
def predict():
    if (request.files['image']): 
        file = request.files['image']

        return get_prediction(file, model)
    else:
        print('No file uploaded!')
        return 'No file uploaded!', 400
