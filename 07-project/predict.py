import joblib

from flask import Flask
from flask import request
from flask import jsonify


model_file = 'model.bin'
dv_file = 'dv.bib'

model = joblib.load('model.bin')
dv = joblib.load('dv.bin')

app = Flask('carOwn')

@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()

    X = dv.transform([customer])
    y_pred = model.predict_proba(X)[0, 1]
    carOwn = y_pred >= 0.5

    result = {
        'carOwn_probability': float(y_pred),
        'carOwn': bool(carOwn)
    }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)