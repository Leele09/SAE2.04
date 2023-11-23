import matplotlib.pyplot as plt
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

def view_sur_periode_donne(debut, fin, station1, station2, station3, station4):
    # Cette commande permet de reset le plot
    plt.clf()
    # On va stocker le résultat de cette requete sql dans une variable
    mycursor.execute(f"CREATE OR REPLACE VIEW view_periode\
                        AS\
                        SELECT HC.stationcode, numdocksavailable, numbikesavailable, mechanical, ebike, name, datemodif\
                        FROM history_change HC\
                        INNER JOIN station_information SI ON SI.stationcode = HC.stationcode\
                        WHERE datemodif BETWEEN '{debut}' AND '{fin}'\
                        AND name = '{station1}' OR name = '{station2}' OR name = '{station3}' OR name = '{station4}';")
    mycursor.execute(f"SELECT * FROM view_periode")
    data = mycursor.fetchall()
    
    # Ici on crée x = [] qui va contenir les dates renvoyés par la requete
    # et dictionnaire_valeurs = {} qui va contenir toutes les infos des quatres stations
    dictionnaire_valeurs = {}
    for i in range(1,5):
        dictionnaire_valeurs[f"x{i}"] = []
        for j in range(1,5):
            dictionnaire_valeurs[f"station{i}_y{j}"] = []
        
    # On stocke chaque donnée dans le dictionnaire en les triant    
    for i in data:
        if i[5] == station1:
            dictionnaire_valeurs["x1"].append(i[6])
            dictionnaire_valeurs["station1_y1"].append(i[4])
            dictionnaire_valeurs["station1_y2"].append(i[3])
            dictionnaire_valeurs["station1_y3"].append(i[2])
            dictionnaire_valeurs["station1_y4"].append(i[1])
        elif i[5] == station2:
            dictionnaire_valeurs["x2"].append(i[6])
            dictionnaire_valeurs["station2_y1"].append(i[4])
            dictionnaire_valeurs["station2_y2"].append(i[3])
            dictionnaire_valeurs["station2_y3"].append(i[2])
            dictionnaire_valeurs["station2_y4"].append(i[1])
        elif i[5] == station3:
            dictionnaire_valeurs["x3"].append(i[6])
            dictionnaire_valeurs["station3_y1"].append(i[4])
            dictionnaire_valeurs["station3_y2"].append(i[3])
            dictionnaire_valeurs["station3_y3"].append(i[2])
            dictionnaire_valeurs["station3_y4"].append(i[1])
        elif i[5] == station4:
            dictionnaire_valeurs["x4"].append(i[6])
            dictionnaire_valeurs["station4_y1"].append(i[4])
            dictionnaire_valeurs["station4_y2"].append(i[3])
            dictionnaire_valeurs["station4_y3"].append(i[2])
            dictionnaire_valeurs["station4_y4"].append(i[1])
      
    # On désigne des subplots  
    fig, axs = plt.subplots(2, 2)
       
    liste_lables = ["E-bike","Mécanique","Vélos disponnibles","Docks disponnibles"]
    # On rentre chaque donné pour chaque graphique 
    for i in range(1,5):
        axs[0, 0].plot(dictionnaire_valeurs["x1"], dictionnaire_valeurs[f"station1_y{i}"], label = liste_lables[i-1])
        axs[0, 1].plot(dictionnaire_valeurs["x2"], dictionnaire_valeurs[f"station2_y{i}"])
        axs[1, 0].plot(dictionnaire_valeurs["x3"], dictionnaire_valeurs[f"station3_y{i}"])
        axs[1, 1].plot(dictionnaire_valeurs["x4"], dictionnaire_valeurs[f"station4_y{i}"])
    
    # On définie les titres
    axs[0, 0].title.set_text(station1)
    axs[0, 1].title.set_text(station2)
    axs[1, 0].title.set_text(station3)
    axs[1, 1].title.set_text(station4)
    
    # Cette commande permet de mettre le label de l'axe des x en diagonale pour que ce soit plus lisible
    fig.autofmt_xdate()
    fig.legend(loc='upper center', ncol=4)
    
    fig.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
       
    return fig.savefig('NevesSousa_SAE204/Codes/static/view_sur_periode_donnee.png', dpi=300, format='png', bbox_inches='tight')
    
def view_sur_commune(commune):
    # Cette commande permet de reset le plot
    plt.clf()
    mycursor.execute(f"CREATE OR REPLACE VIEW view_commune\
                        AS\
                        SELECT SUM(numdocksavailable), SUM(numbikesavailable), SUM(mechanical), SUM(ebike), DATE_FORMAT(datemodif, '%Y-%m-%d %H:%i')\
                        FROM history_change\
                        WHERE nom_arrondissement_communes = '{commune}' AND datemodif >= DATE_SUB(NOW(), INTERVAL 1 WEEK)\
                        GROUP BY datemodif;")
    mycursor.execute('SELECT * FROM view_commune;')
    # On stock les infos dans une variable
    data = mycursor.fetchall()
    # On crée le graphique
    x,y1,y2,y3,y4 = [],[],[],[],[]
    
    for i in data:
        x.append(i[4])
        y1.append(i[3])
        y2.append(i[2])
        y3.append(i[1])
        y4.append(i[0])

    plt.plot(x, y1, label="E-bike")
    plt.plot(x, y2, label="Mécanique")
    plt.plot(x, y3, label="Vélos disponnibles")
    plt.plot(x, y4, label="Docks disponnibles")
    plt.gcf().autofmt_xdate() 
    plt.title(commune)   
    
    return plt.savefig('NevesSousa_SAE204/Codes/static/view_sur_commune.png', dpi=300, format='png', bbox_inches='tight')
    
def view_sur_station(station):
    # Cette commande permet de reset le plot
    plt.clf()
    mycursor.execute(f"CREATE OR REPLACE VIEW view_station\
                        AS\
                        SELECT numdocksavailable, numbikesavailable, mechanical, ebike, datemodif\
                        FROM history_change\
                        WHERE stationcode = '{station}' AND datemodif >= DATE_SUB(NOW(), INTERVAL 24 HOUR);")
    mycursor.execute('SELECT * FROM view_station;')
    # On stock les infos dans une variable
    data = mycursor.fetchall()
    # On crée le graphique
    x,y1,y2,y3,y4 = [],[],[],[],[]
    for i in data:
        x.append(i[4])
        y1.append(i[3])
        y2.append(i[2])
        y3.append(i[1])
        y4.append(i[0])
    plt.plot(x, y1, label="E-bike")
    plt.plot(x, y2, label="Mécanique")
    plt.plot(x, y3, label="Vélos disponnibles")
    plt.plot(x, y4, label="Docks disponnibles")
    plt.title(f"Code station : {station}")
    plt.legend()
    
    return plt.savefig('NevesSousa_SAE204/Codes/static/view_sur_station.png', dpi=300, format='png', bbox_inches='tight')
    
def view_types_de_velos():
    # Cette commande permet de reset le plot
    plt.clf()
    # Requete qui va récuperer les infos
    mycursor.execute(f"CREATE OR REPLACE VIEW view_types_de_velos\
                        AS\
                        SELECT SUM(mechanical), SUM(ebike)\
                        FROM station_status")
    mycursor.execute("SELECT * FROM view_types_de_velos")
    # On stock les infos dans une variable
    data = mycursor.fetchall()
    # On crée le graphique
    plt.pie(data[0], labels=['Mécaniques','Eléctriques'], autopct='%1.1f%%', explode=(0.01,0.01))
    
    return plt.savefig('NevesSousa_SAE204/Codes/static/view_sur_types_de_velos.png', dpi=300, format='png', bbox_inches='tight')

view_sur_station(11114)
# view_types_de_velos()
# view_sur_commune('Paris')
# view_sur_periode_donne('2023-06-0cdsjbcjksdbcks','2023-06-02 10:03:30','Benjamin Godard - Victor Hugo','Ney - Porte de Clignancourt','Gare Rosny-Bois-Perrier','Redoute - Les Courtilles')