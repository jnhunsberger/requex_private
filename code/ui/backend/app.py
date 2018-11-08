from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import pickle
import numpy as np
from flask import render_template
from flask import request


import sys
PROJECT_ROOT = "./"
#PROJECT_ROOT = "/app/"
sys.path.append(PROJECT_ROOT)
import lstm_binary 

# declare constants
HOST = '0.0.0.0'
PORT = 8082

TOKENIZER_FILE = PROJECT_ROOT + "saved_models/tokenizer"
MODEL_JSON = PROJECT_ROOT + "saved_models/binary_LSTM.json"
MODEL_H5 = PROJECT_ROOT + "saved_models/binary_LSTM.h5"

# initialize flask application
app = Flask(__name__)
api = Api(app)

testmodel = lstm_binary.LSTMBinary()
testmodel.load(TOKENIZER_FILE, MODEL_JSON, MODEL_H5)

'''
@app.route('/api/load', methods=['GET', 'POST'])
def load():
    testmodel.load(TOKENIZER_FILE, MODEL_JSON, MODEL_H5)

    return "Successfully loaded the model files"


@app.route('/api/predict', methods=['GET', 'POST'])
def predict(url):
    urltypes = testmodel.predict([url])
    return jsonify([{'url': url, 'type': urltype}])
'''

# argument parsing
parser = reqparse.RequestParser()
parser.add_argument('query')

@app.route("/")
def get():
    query = request.args.get("URL")
    if not query:
            user_query = "www.example.com"
    else:
            user_query = query.lower()

    prediction = testmodel.predict([user_query])

    # Output either 'Negative' or 'Positive' along with the score
    if prediction == 0:
        pred_text = 'Benign'
    else:
        pred_text = 'Malicious'

    # create JSON object
    output = {'url': user_query, 'type': pred_text}

    return render_template("cyber.html", output=output)

class PredictUrl(Resource):
    def get(self):
        # use parser and find the user's query
        args = parser.parse_args()
        user_query = args['query']

        print("User Query String: ", user_query)  

        prediction = testmodel.predict([user_query])

        # Output either 'Negative' or 'Positive' along with the score
        if prediction == 0:
            pred_text = 'Benign'
        else:
            pred_text = 'Malicious'

        # create JSON object
        output = {'url': user_query, 'type': pred_text}

        return output


# Setup the Api resource routing here
# Route the URL to the resource
# api.add_resource(PredictUrl, '/')



if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)
