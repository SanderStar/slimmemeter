import datetime
import uuid
import mysql.connector
import sys


class Meting:
    # unieke id
    id = None
    # huidige datum + tijd 
    datum_tijd = None
    # kWh
    elektra_levering_laag = None
    elektra_levering_hoog = None
    elektra_teruglevering_laag = None
    elektra_teruglevering_hoog = None
    # kW
    elektra_levering_vermogen = None
    elektra_teruglevering_vermogen = None
    # m3
    gas_levering = None

    def __init__(self):
        self.datum_tijd = datetime.datetime.now()
        self.id = uuid.uuid4()


# Open uitvoer bestand tbv unit test
with open("output.txt", "r") as ins:
    lines = []
    for line in ins:
        lines.append(line)

meting = Meting()

# Ontleed elke regel in het bestand
for i in range(len(lines)):
    # TODO evt * 1000 eruit halen om echte waarden te bewaren
    if lines[i][0:9] == "1-0:1.8.1":
        meting.elektra_levering_laag = float(lines[i][10:20])
        print("daldag                  ", int(float(lines[i][10:20])*1000), "kWh")
    elif lines[i][0:9] == "1-0:1.8.2":
        meting.elektra_levering_hoog = float(lines[i][10:20])
        print("piekdag                 ", int(float(lines[i][10:20])*1000), "kWh")
    elif lines[i][0:9] == "1-0:2.8.1":
        # Daltarief, teruggeleverd vermogen
        meting.elektra_teruglevering_laag = float(lines[i][10:20])
        print("dalterug                ", int(float(lines[i][10:20])*1000), "kWh")
    elif lines[i][0:9] == "1-0:2.8.2":
        # Piek tarief, teruggeleverd vermogen
        meting.elektra_teruglevering_hoog = float(lines[i][10:20])
        print("piekterug               ", int(float(lines[i][10:20])*1000), "kWh")
    elif lines[i][0:9] == "1-0:1.7.0":
        # Huidige stroomafname
        meting.elektra_levering_vermogen = float(lines[i][10:16])
        print("afgenomen vermogen      ", int(float(lines[i][10:16])*1000), " kW")
    elif lines[i][0:9] == "1-0:2.7.0":
        # Huidig teruggeleverd vermogen
        meting.elektra_teruglevering_vermogen = float(lines[i][10:16])
        print("teruggeleverd vermogen  ", int(float(lines[i][10:16])*1000), " kW")
    elif lines[i][0:10] == "0-1:24.2.1":
        # Gasmeter
        meting.gas_levering = float(lines[i][26:35])
        print("gas                     ", int(float(lines[i][26:35])*1000), " m3")
    else:
        pass

db = mysql.connector.connect(host="192.168.2.5",
                     port="3307",
                     user="slimmemeter",
                     passwd="slimmemeter",
                     db="star")

cur = db.cursor()

# TODO nice exception handling
try:
    cur.execute("INSERT INTO meting VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",  
        ( None,
        meting.datum_tijd, 
        meting.elektra_levering_hoog, 
        meting.elektra_levering_laag,
        meting.elektra_teruglevering_hoog,
        meting.elektra_teruglevering_laag,
        meting.elektra_levering_vermogen,
        meting.elektra_teruglevering_vermogen,
        meting.gas_levering) )
    db.commit()
except:
   db.rollback()
   sys.exit("Inserting data in database fails")

# Use all the SQL you like
cur.execute("SELECT * FROM meting")

# print the rows
for row in cur.fetchall():
    print(row)

db.close()