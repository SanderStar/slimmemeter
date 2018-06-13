import datetime

print('Hello')

class Meting:
    datumtijd = None
    i = 0
    def __init__(self, a):
        self.i = a
        self.datumtijd = datetime.datetime.now()

x = Meting(10)
print(x.i, x.datumtijd)

# Open uitvoer bestand
with open("output.txt", "r") as ins:
    lines = []
    for line in ins:
        lines.append(line)

# Ontleed elke regel in het bestand
for i in range(len(lines)):
    if lines[i][0:9] == "1-0:1.8.1":
        print("daldag     ", int(float(lines[i][10:20])*1000), "kWh")
    elif lines[i][0:9] == "1-0:1.8.2":
        print("piekdag    ", int(float(lines[i][10:20])*1000), "kWh")
    elif lines[i][0:9] == "1-0:2.8.1":
        # Daltarief, teruggeleverd vermogen
	    print("dalterug   ", int(float(lines[i][10:20])*1000), "kWh")
    elif lines[i][0:9] == "1-0:2.8.2":
        # Piek tarief, teruggeleverd vermogen
        print("piekterug  ", int(float(lines[i][10:20])*1000), "kWh")
    elif lines[i][0:9] == "1-0:1.7.0":
        # Huidige stroomafname
        print("afgenomen vermogen      ", int(float(lines[i][10:16])*1000), " kW")
    elif lines[i][0:9] == "1-0:2.7.0":
        # Huidig teruggeleverd vermogen
        print("teruggeleverd vermogen  ", int(float(lines[i][10:16])*1000), " kW")
    elif lines[i][0:10] == "0-1:24.2.1":
        # Gasmeter
        print("gas                     ", int(float(lines[i][26:35])*1000), " m3")
    else:
        pass
