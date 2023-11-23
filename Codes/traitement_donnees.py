import pandas as pd

station = pd.read_json("JSON/velib-emplacement-des-stations.json")
disponibilite = pd.read_json("JSON/velib-disponibilite-en-temps-reel.json")

# station = pd.DataFrame(station)
# disponibilite = pd.DataFrame(disponibilite)
disponibilite = disponibilite[["name",
                                "capacity",
                                "is_renting",
                                "is_returning",
                                "duedate",
                                "coordonnees_geo",
                                "code_insee_commune"]]

print(disponibilite)