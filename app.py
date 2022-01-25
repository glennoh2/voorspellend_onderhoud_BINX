# url_for en redirect linkt verschillende pagina"s aan elkaar
from flask import Flask, redirect, url_for, render_template, request
import pandas as pd
import numpy as np
from joblib import load
from datetime import datetime
app = Flask(__name__)

def_model = load("./def_model_123.pkl")
kolommen=["Aansturing Ventilator", "Fijnstofconcentratie PM10", "Fijnstofconcentratie PM2.5", "Filteroppervlak", "Klasse", "Totale Flow", "Voltooide Levensduur"]
#resultaat_voorspelling = float(0)

# Formule om het energieverbruik te meten volgens Camfil BV
# Energieverbruik = (flow*drukverschil*draaiuren fitler)/(eff.filter*1000)
# Flow -> [m^3/s]
# Drukverschil -> [Pa]
# Draaiuren -> [h]
# Eff. Filter -> [0, 1.0]
def bereken_energieverbruik(drukverschil, flow, levensduur, aanst_vent):
    flow_ms = flow/3600
    a = int(flow_ms*drukverschil*levensduur)
    aanst_vent_verh = aanst_vent/100
    b = int(aanst_vent_verh*1000)
    energieverbruik = int(float(a)/float(b))
    return energieverbruik

 # Routes om te navigeren door .html templates
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/onderzoek")
def onderzoek():

    return render_template("onderzoek.html")

@app.route("/pdm_filters")
def pdm_filters():

    return render_template("pdm_filters.html")

@app.route("/contact")
def contact():

    return render_template("contact.html")

@app.route("/voorspelling")
def voorspelling():

    return render_template("voorspelling.html")

@app.route("/voorspelling/resultaat", methods=["POST"])
def voorspelling_maken():
    if request.method == "POST":
        # Krijg de waardes die de gebruiker in "voorspelling.html" ingeeft
        aanst_vent = request.form["aanst_vent"]
        fijnst_pm10 = request.form["fijnst_pm10"]
        fijnst_pm2_5 = request.form["fijnst_pm2_5"]
        filt_opp = request.form["filt_opp"]
        klasse = request.form["klasse"]
        flow = request.form["flow"]
        levensduur = request.form["levensduur"]
        input_parameters = [float(aanst_vent), float(fijnst_pm10), float(fijnst_pm2_5), float(filt_opp), str(klasse), float(flow), float(levensduur)]
             
        # Zet de waardes is een pandas dataframe (zo kan het model een voorspelling maken)
        pd_input_parameters = pd.DataFrame([input_parameters], columns=kolommen)
        resultaat_voorsp = def_model.predict(pd_input_parameters)
        drukverschil= float(resultaat_voorsp)

        # Bereken het energieverbruik middels de gegeven parameters
        #energieverbruik = bereken_energieverbruik(60, 7, 5000, 0.70)
        energieverbruik = bereken_energieverbruik(float(drukverschil), float(flow), int(levensduur), float(aanst_vent))

        # Bereken de totale energiekosten aan de hand van de energieprijs
        energieprijs = request.form["energieprijs"]
        tot_energiekosten = energieverbruik*float(energieprijs) #aanpassen naar variabele input

        # Afronden van de resultaten
        drukverschil = round(drukverschil, 1)
        energieverbruik = int(energieverbruik)
        tot_energiekosten = round(tot_energiekosten, 2)
        
    else:
        drukverschil = None
        energieverbruik = None
        tot_energiekosten = None
    return render_template("voorspelling.html", result_drukverschil=drukverschil, result_energieverbruik=energieverbruik, result_energiekosten=tot_energiekosten)

@app.route("/aanst_vent")
def aanst_vent():

    return render_template("aanst_vent.html")

@app.route("/fijnstof")
def fijnstof():

    return render_template("fijnstof.html")

@app.route("/filt_opp")
def filt_opp():

    return render_template("filt_opp.html")

@app.route("/klasse")
def klasse():

    return render_template("klasse.html")

@app.route("/flow")
def flow():

    return render_template("flow.html")

@app.route("/levensduur")
def levensduur():
   
    return render_template("levensduur.html")

@app.route("/levensduur/bereken", methods=["POST"])
def levensduur_berekening():
    if request.method == "POST":
        # Krijg de waardes die de gebruiker in "levensduur.html" ingeeft
        datum_plaatsing_filter = request.form["datum_plaatsing_filter"]
        datum_huidig_filter = request.form["datum_huidig_filter"]

        date_format = "%Y-%m-%d"
        a = datetime.strptime(datum_plaatsing_filter, date_format)
        b = datetime.strptime(datum_huidig_filter, date_format)
        levensduur_ber = b - a        

        dagen = levensduur_ber.days
        seconden = levensduur_ber.seconds
        levensduur_ber = (dagen*24) + (seconden/3600)
        levensduur_ber = int(levensduur_ber)
    else:   
        levensduur_ber = None
    return render_template("levensduur.html", result_levensduur=levensduur_ber)

@app.route("/energieprijs")
def energieprijs():

    return render_template("energieprijs.html")

@app.route("/resultaten/<drukverschil>/<energieverbruik>/<tot_energiekosten>")
def resultaten(drukverschil, energieverbruik, tot_energiekosten):
    return render_template("resultaten.html", result_drukverschil=drukverschil, result_energieverbruik=energieverbruik, result_energiekosten=tot_energiekosten)

if __name__=="__main__":
    app.run(port=5000, debug = True)

