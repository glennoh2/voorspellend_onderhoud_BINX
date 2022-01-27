# url_for en redirect linkt verschillende pagina's aan elkaar
from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)

from joblib import load
import pandas as pd
def_model = load("./def_model.pkl")
kolommen=['Aansturing Ventilator', 'Fijnstofconcentratie PM10', 'Fijnstofconcentratie PM2.5', 'Filteroppervlak', 'Klasse', 'Totale Flow', 'Voltooide Levensduur']

@app.route("/") # Route om te navigeren
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr = user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"



@app.route("/voorspelling", methods=["POST", "GET"])
def voorspelling():
    if request.method == "POST":
        aanst_vent = request.form['aanst_vent']
        fijnst_pm10 = request.form['fijnst_pm10']
        fijnst_pm2_5 = request.form['fijnst_pm2_5']
        filt_opp = request.form['filt_opp']
        klasse = request.form['klasse']
        flow = request.form['flow']
        levensduur = request.form['levensduur']
        
        #lijst_parameters = [aanst_vent, fijnst_pm10, fijnst_pm2_5, filt_opp, klasse, flow, levensduur]
        lijst_parameters = [100, 17, 10, 59, "F7", 20000, 5000]
        
        
        input_parameters = lijst_parameters
        pd_input_parameters = pd.DataFrame([input_parameters], columns=kolommen)
        resultaat_voorsp = def_model.predict(pd_input_parameters)
        #result = int(resultaat_voorsp.Label[0])
        resultaat= resultaat_voorsp
    
    
        return redirect(url_for("resultaat", result=resultaat))
        
    else:
        return render_template("voorspelling.html")

@app.route("/<result>")
def resultaat(result):

    return f"<h1>{result}</h1>"

if __name__=='__main__':
    app.run(port=5000, debug = True)

