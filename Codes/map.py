import folium as fo
from folium.plugins import MarkerCluster

import mysql.connector as sql
import geopandas as gpd
from shapely import Polygon, Point
from shapely.geometry import shape

# Connexion à la database
mydb = sql.connect(
  host="localhost",
  user="root",
  password="",
  database="velibs"
)

# On instancie notre cursor où on va éxecuter nos requêtes
mycursor = mydb.cursor()

def creation_map_markers():
  # On initialise la zone de la map qui englobe l'Île de France
  zone_map = fo.Map(location=[48.856614, 2.352222], zoom_start=12)
  
  geodata = gpd.read_file("NevesSousa_SAE204\JSON\quartier_paris.geojson")

  # On crée un dico qui va contenir les cluster et un polygon qui leur est associé
  dict_cluster_polygon = {}
  
  for _, r in geodata.iterrows():
    # On trace les quartiers
    sim_geo = gpd.GeoSeries(r["geometry"])
    geo_j = sim_geo.to_json()
    geo_j = fo.GeoJson(data=geo_j, style_function=lambda x: {"fillColor": "orange"})
    geo_j.add_to(zone_map)
    # On ajoute les clusters avec les polygons qui leur correspond à un dico
    coords = [[y,x] for x,y in r["geometry"].exterior.coords]
    dict_cluster_polygon[MarkerCluster()] = Polygon(coords)

  # On fait la requête sql qui va récuperer les données et on les stocks dans une variable
  mycursor.execute("SELECT * FROM station_status SS\
                    INNER JOIN station_information SI ON SS.stationcode = SI.stationcode;")
  rows = mycursor.fetchall()
  
  # On crée un dico qui va stocker les markers et leur point associé crée avec les mêmes coordonnées
  dict_marker_point = {}  
   
  # On parcours les données et on les exploitent
  #     - row[12] = latitude, row[11] = longitude
  #     - row[0] = stationcode
  #     - row[1] = is_installed
  #     - row[2] = numdocksavailable
  #     - row[3] = numbikesavailable
  #     - row[4] = mechanical
  #     - row[5] = ebike
  #     - row[6] = nom_arrondissement_communes
  #     - row[9] = name
  #     - row[10] = capacity
  for row in rows:
    # A chaque boucle on fait une petite vérification pour changer les valeurs numériques ici "is_installed" pour que ce soit plus agréable au visuel
    if row[1] == '1':
      is_installed = 'OUI'
    else:
      is_installed = 'NON'
    # On change la couleur du marker en fonction des vélos disponibles
    if row[3] >= 20 :
      color = 'green'
    elif 10 <= row[3] < 20:
      color = 'orange'
    elif 1 <= row[3] < 10:
      color = 'red'
    elif row[3] == 0 :
      color = 'black'
    dict_marker_point[fo.Marker([row[12], row[11]], icon=fo.Icon(color=color, icon="bicycle", prefix="fa"),
                        tooltip = (f"Code de station : {row[0]}<h4>{row[9]}</h4><h5>{row[6]}</h5>Capacité : {row[10]}<br>Est installé : {is_installed}"),
                        popup = fo.Popup(f"Docks disponibles : {row[2]}<br>Vélos disponibles : {row[3]}<br><br>Vélos mécaniques : {row[4]}<br>Vélos éléctriques : {row[5]}", max_height = 100, max_width= 270))] = Point([row[12], row[11]])
  
  # Pour chaque cluster on va verifier si un marker est dedans grâce au polygones et points que nous avions stocké          
  for cluster, polygon in dict_cluster_polygon.items():
    # A chaque itération de la boucle qui parcours les clusters ont fait une copie du dico des points pour la parcourir,
    # ça va nous permettre de supprimer les points qui ont déja été palcé et par la suite placer ceux qui n'ont pas été placé
    copy_dict_marker_point = dict_marker_point.copy()
    for marker, point in copy_dict_marker_point.items():
      if polygon.contains(point):
        cluster.add_child(marker)
        dict_marker_point.pop(marker)
    cluster.add_to(zone_map)
    
  # Pour les stations qui ne sont pas dans les quartiers on les ajoutes dans un cluster global
  cluster_hors_quartier = MarkerCluster().add_to(zone_map)
  for derniers_markers in dict_marker_point.keys():
    derniers_markers.add_to(cluster_hors_quartier)
      
  # On renvoie le fichier html mit a jour
  return zone_map.save('NevesSousa_SAE204/Codes/static/map.html')