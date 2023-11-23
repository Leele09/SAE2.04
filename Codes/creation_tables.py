import mysql.connector as sql

# Connexion à la database
mydb = sql.connect(
  host="localhost",
  user="root",
  password="",
  database="velibs"
)

# On instancie notre cursor où on va éxecuter nos requêtes
mycursor = mydb.cursor()

def create_table(nom_table):
  if nom_table == 'stations':
    # ---------------------Création table station_information---------------------
    mycursor.execute("CREATE TABLE IF NOT EXISTS station_information ( \
      stationcode VARCHAR(100) PRIMARY KEY, \
      name VARCHAR(120), \
      capacity INT, \
      longitude FLOAT, \
      latitude FLOAT \
      )")
    
  elif nom_table == 'status':
    # -----------------------Création table station_status------------------------
    mycursor.execute("CREATE TABLE IF NOT EXISTS station_status ( \
      stationcode VARCHAR(100) PRIMARY KEY,\
      is_installed VARCHAR(3), \
      numdocksavailable INT, \
      numbikesavailable INT, \
      mechanical INT, \
      ebike INT, \
      nom_arrondissement_communes VARCHAR(100), \
      horodatage DATETIME \
      )")
  
  elif nom_table == 'history_change':
    # -----------------------Création table history_change------------------------
    mycursor.execute("CREATE TABLE IF NOT EXISTS history_change ( \
      user VARCHAR(30), \
      type_modif VARCHAR(50), \
      stationcode VARCHAR(100),\
      is_installed VARCHAR(3), \
      numdocksavailable INT, \
      numbikesavailable INT, \
      mechanical INT, \
      ebike INT, \
      nom_arrondissement_communes VARCHAR(100), \
      datemodif DATETIME \
      )")
  
  else:
    raise NameError