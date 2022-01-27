# url_for en redirect linkt verschillende pagina's aan elkaar
from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)

# Navigatie voor de web applicatie
# Navigeer naar de home pagina (template)
@app.route("/")
@app.route("/home")
def home():
    return render_template("huis.html")

# Navigeer naar de login pagina (template)
@app.route("/login")
def login():
    return render_template("login.html")

# Navigeer naar de home pagina (template) via logout
@app.route("/logout")
def logout():
    return redirect(url_for("home"))

# Navigeer naar succesvol ingelogd (na drukken op submit-knop)
# GET methode zal de gebruikersnaam en het wachtwoord tonen in de html link
# POST methode zal dit niet doen (privacy)
@app.route("/submit", methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        user = request.form['gn']
        return f"Login succesvol (POST), Hello {user}"
    else:
        user = request.args.get('gn')
        return f"Login succesvol (GET), Hello {user}" 

if __name__=='__main__':
    app.run()