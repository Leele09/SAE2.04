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

def trigger_modifications():
    liste_EVENT = ['DELETE', 'UPDATE', 'INSERT']
    action = 'BEFORE'
    OLD_or_NEW = 'OLD'
    for event in liste_EVENT:
        if event == 'INSERT':
            action = 'AFTER'
            OLD_or_NEW = 'NEW'
        mycursor.execute(f"CREATE TRIGGER HistModif_{event}_station_status {action} {event} ON station_status\
                            FOR EACH ROW\
                            BEGIN\
                                INSERT INTO history_change VALUES(user(),'{event}',{OLD_or_NEW}.stationcode , {OLD_or_NEW}.is_installed, {OLD_or_NEW}.numdocksavailable, {OLD_or_NEW}.numbikesavailable, {OLD_or_NEW}.mechanical, {OLD_or_NEW}.ebike, {OLD_or_NEW}.nom_arrondissement_communes, NOW());\
                            END")
            
def trigger_limit_valeur():
    liste_EVENT = ['UPDATE', 'INSERT']
    for event in liste_EVENT:
        mycursor.execute(f"CREATE TRIGGER LimitValeur_{event}_station_status BEFORE {event} ON station_status\
                            FOR EACH ROW\
                            BEGIN\
                                IF NEW.is_installed = 'OUI' THEN\
                                    SET NEW.is_installed = 1;\
                                ELSEIF NEW.is_installed = 'NON' THEN\
                                    SET NEW.is_installed = 0;\
                                END IF;\
                            END")