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
import lstm_multiclass 

# declare constants
HOST = '0.0.0.0'
PORT = 8082

BINARY_TOKENIZER_FILE = PROJECT_ROOT + "saved_models/binary_tokenizer.pkl"
BINARY_CATEGORIES_FILE = PROJECT_ROOT + "saved_models/binary_categories.pkl"
BINARY_MODEL_JSON = PROJECT_ROOT + "saved_models/binary_LSTM.json"
BINARY_MODEL_H5 = PROJECT_ROOT + "saved_models/binary_LSTM.h5"
BINARY_MODEL_METRICS_REPORT = PROJECT_ROOT + "saved_models/binary_metrics_report"
BINARY_MODEL_CLASS_REPORT = PROJECT_ROOT + "saved_models/binary_class_report"

MULTI_TOKENIZER_FILE = PROJECT_ROOT + "saved_models/multiclass_tokenizer.pkl"
MULTI_CATEGORIES_FILE = PROJECT_ROOT + "saved_models/multiclass_categories.pkl"
MULTI_MODEL_JSON = PROJECT_ROOT + "saved_models/multiclass_LSTM.json"
MULTI_MODEL_H5 = PROJECT_ROOT + "saved_models/multiclass_LSTM.h5"

# initialize flask application
app = Flask(__name__)
api = Api(app)

binary_model = lstm_binary.LSTMBinary()
binary_model.load(BINARY_TOKENIZER_FILE, BINARY_MODEL_JSON, BINARY_MODEL_H5)

multi_model = lstm_multiclass.LSTMMulti()
multi_model.load(MULTI_TOKENIZER_FILE, MULTI_CATEGORIES_FILE, MULTI_MODEL_JSON, MULTI_MODEL_H5)

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

def get_binary(binary_query):
    prediction = binary_model.predict([binary_query])

    # Output either 'Negative' or 'Positive' along with the score
    if prediction == 1:
        pred_text = 'Benign'
    else:
        pred_text = 'Malicious'

    # create JSON object
    output = {'url': binary_query, 'type': pred_text}

    return output


def get_multi(multi_query):

    urltype, pred_prob = multi_model.predict([multi_query])

    # print("MULTICLASS Prediction: ", multi_query, " Type: ", urltype)

    # create JSON object
    output = {'url': multi_query, 'type': urltype[0], 'probability': pred_prob[0]}
    return output

@app.route("/")
def get():
    # global binary_response, multi_response
    
    # if binary_response is None:
    #     binary_response = {'url': ' ', 'type': ' '}
    # if multi_response is None:
    #     multi_response = {'url': ' ', 'type': ' '}

    binary_response = {'url': ' ', 'type': ' '}
    multi_response = {'url': ' ', 'type': ' '}

    binary_query = request.args.get("URL_Binary")
    if binary_query:
        binary_query = binary_query.lower()
        binary_response =  get_binary(binary_query)

    # multi_query = request.args.get("URL_Multi")
    # if multi_query:
    #     multi_query = multi_query.lower()
        multi_response = get_multi(binary_query)

    return render_template("cyber.html", binary_output=binary_response, multi_output=multi_response )

# class PredictUrl(Resource):
#     def get(self):
#         # use parser and find the user's query
#         args = parser.parse_args()
#         user_query = args['query']

#         print("User Query String: ", user_query)  

#         prediction = binary_model.predict([user_query])

#         # Output either 'Negative' or 'Positive' along with the score
#         if prediction == 0:
#             pred_text = 'Benign'
#         else:
#             pred_text = 'Malicious'

#         # create JSON object
#         output = {'url': user_query, 'type': pred_text}

#         return output


# Setup the Api resource routing here
# Route the URL to the resource
# api.add_resource(PredictUrl, '/')



if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT, 
            threaded=False)
