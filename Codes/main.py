import schedule
import time

from  insertion_update_donnees import *
from  creation_tables import *
from triggers import *
from map import *

def premiere_création():
    yes_or_no = input("Voulez vous créer toutes les fonctionnalités depuis le début (y/n): ")
    if yes_or_no == 'y':
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #                   Création des tables                       #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                
        try:  
            create_table('stations')
            create_table('status')
            create_table('history_change')
        except(NameError):
            print("Il y à une erreur sur le nom de la table")
        except:
            print("Il y à eu une erreur lors de la création d'une ou plusieurs tables")
        else:
            print('Création des tables : ✓')

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #                     Lecture des données                     #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

        # Gestion des exception qui va lever une erreur différente en fonction de la où 
        # l'erreur se trouve pour pouvoir indiquer où il y à eu l'erreur
        try:
            data_stations = lecture_json('stations')
            data_status = lecture_json('status')
        except:
            print('Une erreur est survenue lors de la lecture des données')
        else:
            print('Lecture des données : ✓')
            
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #                           Triggers                          #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        # On crée les triggers
        try:
            trigger_modifications()
            trigger_limit_valeur()
        except:
            print("Il y à eu une erreur lors de la création des triggers")
        else:
            print("Triggers : ✓")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #                   Insertion des données                     #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

        # On insert qu'une seule fois les données stations car elles sont statiques
        try:
            insertion_donnees(data_stations)
            insertion_donnees(data_status)
        except:
            print('Une erreur est survenue lors de la première insertion de données')
        else:
            print('Première insertion de données : ✓')

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #                      Création de la map                     #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
            
        # On crée une première carte
        try:
            creation_map_markers()
        except:
            print("Une erreur est survenue dans la création de la map")
        else:
            print("Map : ✓")
    else:
        print('Création structures première passé')
        

def job():
    print("Mis à jour des données en cours...")
    data_status = lecture_json('status')
    update_donnees(data_status)
    creation_map_markers()
    print("Données mises à jour")
    
if __name__ == '__main__' :
    
    # On exécute une fois cette fonction qui va exécuter l'essentiel pour la mise en place de tout
    premiere_création()
    
    # Toutes les 15 minutes on insert les données status car elles sont dynamiques
    schedule.every(10).seconds.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)