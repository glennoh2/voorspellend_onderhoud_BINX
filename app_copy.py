from flask import Flask,request, url_for, redirect, render_template, jsonify
from pycaret.regression import *
import pandas as pd
import pickle
import numpy as np
from joblib import load


app = Flask(__name__)

model = load("./def_model.joblib")
cols = ['Aansturing Ventilator', 'Fijnstofconcentratie PM10', 'Fijnstofconcentratie PM2.5', 'Filteroppervlak', 'Klasse', 'Totale Flow', 'Voltooide Levensduur']

@app.route('/')
def home():
    return render_template("home - Copy.html")

@app.route('/predict',methods=['POST'])
def predict():
    int_features = [x for x in request.form.values()]
    final = np.array(int_features)
    data_unseen = pd.DataFrame([final], columns = cols)
    prediction = predict_model(model, data=data_unseen, round = 0)
    prediction = int(prediction.Label[0])
    return render_template('home - Copy.html',pred='Het voorspelde drukverschil is {}'.format(prediction))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    data_unseen = pd.DataFrame([data])
    prediction = predict_model(model, data=data_unseen)
    output = prediction.Label[0]
    return jsonify(output)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
