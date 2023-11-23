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

mycursor.execute("SELECT name FROM station_information ORDER BY name")
stations_name = mycursor.fetchall()

mycursor.execute("SELECT stationcode FROM station_information ORDER BY stationcode")
stations_code = mycursor.fetchall()

mycursor.execute("SELECT DISTINCT nom_arrondissement_communes FROM station_status ORDER BY nom_arrondissement_communes")
stations_commune = mycursor.fetchall()

@app.route('/')
def display_page_principale():
    return render_template('index.html', len = len(stations_name), 
                           stations_name = stations_name, 
                           stations_code = stations_code,
                           stations_commune = stations_commune)
  
@app.route('/graphique1', methods = ['POST','GET'])
def graphique1():
    if request.method == 'POST':
        graphique1 = view_sur_periode_donne(request.form['date_debut'],request.form['date_fin'],request.form['station1'],
                               request.form['station2'],request.form['station3'],request.form['station4'])
        return redirect(url_for('display_page_principale', graphique1=graphique1))
    return render_template("index.html")

@app.route('/graphique2', methods = ['POST','GET'])
def graphique2():
    if request.method == 'POST':
        print(request.form['station'])
        graphique2 = view_sur_station(request.form['station'])
        return redirect(url_for('display_page_principale', graphique2=graphique2))
    return render_template("index.html")

@app.route('/graphique3')
def graphique3():
    print(request.form['commune'])
    graphique3 = view_sur_station(request.form['commune'])
    return redirect(url_for('display_page_principale', graphique3=graphique3))

if __name__ == '__main__':
    app.run()