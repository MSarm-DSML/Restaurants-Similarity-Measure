"""import pickle
import mlflow
import os
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/similarity_measure', methods=['POST'])
def similarity_measure():
    data = json.loads(request.get_json())
    model_path = os.path.join(os.getcwd(), 'mlruns', '0', '6ac907f3d62f4cda92b720e3b2088fbc', 'artifacts', 'models', 'doc2vec_model.pkl')
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    input_number = int(data['number'])
    result = model.dv.most_similar(input_number, topn=20)
    return {'result': result}
if __name__ == '__main__':
    app.run(debug=True) """

import pickle
import mlflow
import os
import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/similarity_measure', methods=['POST'])
def similarity_measure():
    data = json.loads(request.get_json())
    model_path = get_most_recent_model_path()
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    input_number = int(data['number'])
    result = model.dv.most_similar(input_number, topn=20)
    return {'result': result}

def get_most_recent_model_path():
    # Get the most recent run
    runs = mlflow.search_runs(order_by=["start_time desc"], max_results=1)
    if len(runs) == 0:
        raise FileNotFoundError("No MLflow runs found.")
    run_id = runs.iloc[0]["run_id"]

    # Construct the path to the most recent model
    model_path = os.path.join(os.getcwd(), 'mlruns','0', run_id, 'artifacts', 'models', 'doc2vec_model.pkl')
    return model_path

if __name__ == '__main__':
    app.run(debug=True)
