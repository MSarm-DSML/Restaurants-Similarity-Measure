#!/usr/bin/env python
# coding: utf-8

import mlflow, os, json
from flask import Flask, request as flask_request


app = Flask(__name__)

@app.route('/similarity_measure', methods=['POST'])
def similarity_measure():
    data = json.loads(flask_request.get_json())
    model = mlflow.sklearn.load_model(os.getcwd()+'\\mlruns\\0\\341f57115a0741dfadf5327ae9c994eb\\artifacts\\doc2vec_model_')
    input_number = int(data['number'])
    result = model.dv.most_similar(input_number, topn=20)
    return {'result': result}

if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True)
