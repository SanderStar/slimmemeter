# DSMR P1 uitlezen
# (c) 10-2012 - GJ - gratis te kopieren en te plakken
versie = "1.0"
import sys
import serial
import datetime
import uuid
import mysql.connector

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

##############################################################################
#Main program
##############################################################################
print ("DSMR P1 uitlezen",  versie)
print ("Control-C om te stoppen")
print ("Pas eventueel de waarde ser.port aan in het python script")

#Set COM port config
ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize=serial.SEVENBITS 
ser.parity=serial.PARITY_EVEN
ser.stopbits=serial.STOPBITS_ONE
ser.xonxoff=0
ser.rtscts=0
ser.timeout=20
ser.port="/dev/ttyUSB0"

# Open COM port
try:
    ser.open()
except:
    sys.exit ("Fout bij het openen van %s. Aaaaarch."  % ser.name)


# Initialize
# p1_teller is mijn tellertje voor van 0 tot 20 te tellen
p1_teller = 0

lines = []

while p1_teller < 27:
    p1_line = ''
    # Read 1 line van de seriele poort
    try:
        p1_raw = ser.readline()
    except:
        sys.exit ("Seriele poort %s kan niet gelezen worden. Aaaaaaaaarch." % ser.name )
    p1_str=str(p1_raw)
    p1_line=p1_str.strip()
    # als je alles wil zien moet je de volgende line uncommenten
    #print (p1_line)
    lines.append(p1_line)
    p1_teller = p1_teller +1

meting = Meting()

# Ontleed elke regel in het bestand
for i in range(len(lines)):
    if lines[i][0:9] == "1-0:1.8.1":
        meting.elektra_levering_laag = float(lines[i][10:20])
    elif lines[i][0:9] == "1-0:1.8.2":
        meting.elektra_levering_hoog = float(lines[i][10:20])
    elif lines[i][0:9] == "1-0:2.8.1":
        # Daltarief, teruggeleverd vermogen
        meting.elektra_teruglevering_laag = float(lines[i][10:20])
    elif lines[i][0:9] == "1-0:2.8.2":
        # Piek tarief, teruggeleverd vermogen
        meting.elektra_teruglevering_hoog = float(lines[i][10:20])
    elif lines[i][0:9] == "1-0:1.7.0":
        # Huidige stroomafname
        meting.elektra_levering_vermogen = float(lines[i][10:16])
    elif lines[i][0:9] == "1-0:2.7.0":
        # Huidig teruggeleverd vermogen
        meting.elektra_teruglevering_vermogen = float(lines[i][10:16])
    elif lines[i][0:10] == "0-1:24.2.1":
        # Gasmeter
        meting.gas_levering = float(lines[i][26:35])
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


# Close port and show status
try:
    ser.close()
except:
    sys.exit ("Oops %s. Programma afgebroken. Kon de seriele poort niet sluiten." % ser.name )

