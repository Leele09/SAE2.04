from flask import Flask, render_template, request, redirect, url_for
import mysql.connector as sql
from analyses import *

# Connexion à la database
mydb = sql.connect(
  host="localhost",
  user="root",
  password="",
  database="velibs"
)

# On instancie notre cursor où on va éxecuter nos requêtes
mycursor = mydb.cursor()

app = Flask(__name__)

def type_de_requete(name):
    if name == 'name':
        mycursor.execute("SELECT name FROM station_information ORDER BY name")
        stations_name = mycursor.fetchall()
        return stations_name
    elif name == 'code':
        mycursor.execute("SELECT stationcode FROM station_information ORDER BY stationcode")
        stations_code = mycursor.fetchall()
        return stations_code
    elif name == 'commune':
        mycursor.execute("SELECT DISTINCT nom_arrondissement_communes FROM station_status ORDER BY nom_arrondissement_communes")
        stations_commune = mycursor.fetchall()
        return stations_commune

@app.route('/')
def display_page_principale():
    view_types_de_velos()
    return render_template('index.html', len = len(type_de_requete('name')), 
                           len2 = len(type_de_requete('commune')),
                           stations_name = type_de_requete('name'), 
                           stations_code = type_de_requete('code'),
                           stations_commune = type_de_requete('commune'))
  
@app.route('/graphique1', methods = ['POST','GET'])
def graphique1():
    if request.method == 'POST':
        view_sur_periode_donne(request.form['date_debut'],request.form['date_fin'],request.form['station1'],
                               request.form['station2'],request.form['station3'],request.form['station4'])
        return redirect(url_for('display_page_principale'))
    return render_template("index.html")

@app.route('/graphique2', methods = ['POST','GET'])
def graphique2():
    if request.method == 'POST':
        view_sur_station(request.form['station'])
        return redirect(url_for('display_page_principale'))
    return render_template("index.html")

@app.route('/graphique3', methods = ['POST','GET'])
def graphique3():
    if request.method == 'POST':
        view_sur_commune(request.form['commune'])
        return redirect(url_for('display_page_principale'))
    return render_template("index.html")

if __name__ == '__main__':
    app.run()