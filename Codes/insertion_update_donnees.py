import mysql.connector as sql
import pandas as pd

# Connexion à la database
mydb = sql.connect(
  host="localhost",
  user="root",
  password="",
  database="velibs"
)

# On instancie notre cursor où on va éxecuter nos requêtes
mycursor = mydb.cursor()

# Lecture du json
def lecture_json(json):
  if json == 'stations' :
    stations = pd.read_json("NevesSousa_SAE204/JSON/velib-emplacement-des-stations.json")
    return stations
  elif json == 'status' :
    status = pd.read_json("https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/exports/json?lang=fr&timezone=Europe%2FBerlin")
    status = status[['stationcode','is_installed','numdocksavailable','numbikesavailable','mechanical','ebike','nom_arrondissement_communes']]
    return status

# -------------------------------------------------------------------------------

def insertion_donnees(table):
  if table.columns[1] == 'name':
    requete_insert = "INSERT INTO station_information VALUES (%s, %s, %s, %s, %s)"
    for ligne in table.values :
      # On met les valeurs dans un tuple
      valeurs = (str(ligne[0]), ligne[1], ligne[2], ligne[3]['lon'], ligne[3]['lat'])
      # On combine et exécute la requête avec les valeurs
      mycursor.execute(requete_insert,valeurs)
  elif table.columns[1] == 'is_installed':
    requete_insert = "INSERT INTO station_status VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())"
    for ligne in table.values :
      # On met les valeurs dans un tuple
      valeurs = (str(ligne[0]), ligne[1], ligne[2], ligne[3], ligne[4], ligne[5], ligne[6])
      # On combine et exécute la requête avec les valeurs
      mycursor.execute(requete_insert,valeurs)
      
  mydb.commit()

# -------------------------------------------------------------------------------

def update_donnees(table):
  if table.columns[1] == 'name':
    for ligne in table.values :
      requete_insert = "UPDATE station_information SET name = %s, capacity = %s, longitude = %s, latitude = %s WHERE stationcode = "
      requete_insert += f'{str(ligne[0])}'
      # On met les valeurs dans un tuple
      valeurs = (ligne[1], ligne[2], ligne[3]['lon'], ligne[3]['lat'])
      # On combine et exécute la requête avec les valeurs
      mycursor.execute(requete_insert,valeurs)
  elif table.columns[1] == 'is_installed':
    for ligne in table.values :
      requete_insert = "UPDATE station_status SET is_installed = %s, numdocksavailable = %s, numbikesavailable = %s, mechanical = %s, ebike = %s, nom_arrondissement_communes = %s, horodatage = NOW() WHERE stationcode = "
      requete_insert += f'{str(ligne[0])}'
      # On met les valeurs dans un tuple
      valeurs = (ligne[1], ligne[2], ligne[3], ligne[4], ligne[5], ligne[6])
      # On combine et exécute la requête avec les valeurs
      mycursor.execute(requete_insert,valeurs)