# Importeren van joblib om het model in te laden
# Pandas importeren om een dataframe te creëren
from joblib import load
import pandas as pd

# request kan inputs van de gebruiker opvragen
# url_for en redirect linkt verschillende pagina's aan elkaar
# render_template kan html templates renderen in de web applicatie
from flask import Flask, request, url_for, redirect, render_template, jsonify

app = Flask(__name__)

# Navigatie voor de web applicatie
# Navigeer naar de home pagina (template)
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/voorspelling")
def voorspelling():
    return render_template("voorspelling.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/voorspelling', methods=['GET'])
def voorspellen():
    aanst_vent = request.form['aanst_vent']
    fijnst_pm10 = request.form['fijnst_pm10']
    fijnst_pm2_5 = request.form['fijnst_pm2_5']
    filt_opp = request.form['filt_opp']
    klasse = request.form['klasse']
    flow = request.form['flow']
    levensduur = request.form['levensduur']
    input_parameters = {'Aansturing Ventilator': [float(aanst_vent)],
                        'Fijnstofconcentratie PM10': [float(fijnst_pm10)],
                       'Fijnstofconcentratie PM2.5': [float(fijnst_pm2_5)],
                        'Filteroppervlak': [float(filt_opp)],
                        'Klasse': [str(klasse)],
                        'Totale Flow': [float(flow)],
                        'Voltooide Levensduur': [float(levensduur)]}

    
    input_parameters_pd = pd.DataFrame([[aanst_vent, fijnst_pm10, fijnst_pm2_5, filt_opp, klasse, flow, levensduur]], 
                                     columns=['Aansturing Ventilator', 'Fijnstofconcentratie PM10', 'Fijnstofconcentratie PM2.5',
                                              'Filteroppervlak', 'Klasse', 'Totale Flow', 'Voltooide Levensduur'])


    def_model = load("./def_model.joblib")

    #input_parameters_voorb = def_model.transform(input_parameters)
    #def_model_fit = def_model.fit_transform(input_parameters)
    

    #data_filter_test = pd.DataFrame(data=data_filter_test)
    #def_model_loaded = load("def_model.pkl")    # Model ophalen
    voorspelling = def_model.predict(input_parameters_pd)  # Voorspel het drukverschil
    #voorspelling = int(voorspelling.Label[0])
    #voorsp = def_model_fit.predict(input_parameters)
    
    voorsp = voorspelling
    return f"<h1>{voorsp}</h1>"


if __name__=='__main__':
    app.run(port=4000, debug = True)