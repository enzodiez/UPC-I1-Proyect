import customtkinter as ctk
import matplotlib.pyplot as plt
import os

class Airport():
    def __init__(self, ic="", lat=0.0, lon=0.0, schengen=False):
        self.icaoCode = ic
        self.latitude = lat
        self.longitude = lon
        self.schengen = schengen

def IsSchengenAirport(ic):
    trueSchengen = ['LO', 'EB', 'LK', 'LC', 'EK', 'FO', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH', 'BI',
                    'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'GC', 'LE', 'ES', 'LS']
    ic2 = f"{ic[0]}{ic[1]}"
    if ic2 in trueSchengen:
            return True
    
    return False

def SetSchengen(airport: Airport): # Que airport sea un objeto Airport
    if IsSchengenAirport(airport.icaoCode):
        airport.schengen = True

def PrintAirport(airport: Airport): # Que airport sea un objeto Airport
    airport.icaoCode = print(f"El código ICAO del aeropuerto es: {airport.icaoCode}")
    airport.latitude = print(f"Latitud: {airport.latitude}")
    airport.longitude = print(f"Longitud: {airport.longitude}")
    airport.schengen = print(f"Pertenece a la zona Schengen: {airport.schengen}")

def PlotAirports(airports):
    sch, nSch = 0, 0
    for airport in airports:
        if IsSchengenAirport(f"{airport[0]}{airport[1]}"):
            sch += 1
        else:
            nSch += 1

    fig, ax = plt.subplots()

    # Barra Schengen
    ax.bar('Airports', sch, label='Schengen', color='steelblue')

    # Barra No Schengen
    ax.bar('Airports', nSch, bottom=sch, label='No Schengen', color='lightcoral')

    # Configuraciones visuales
    ax.set_ylabel('Count')
    ax.set_title('Schengen airports')
    ax.legend()
    
    plt.show()

def MapAirports(airports):
    # Sobreescribe todo el fichero para actualizarlo
    txt = []
    txt.append("""<kml xmlns="https://www.opengis.net/kml/2.2">
<Document>
    <Style id="Schengen">
        <IconStyle>
            <color>ff00ff00</color>
        </IconStyle>
    </Style>
    <Style id="Non Schengen">
        <IconStyle>
            <color>ff0000ff</color>
        </IconStyle>
    </Style
""")

    for i in range(1, len(airports)):
        ic, lat, lon  = airports[i].split()

        if IsSchengenAirport(ic):
            style = 'Schengen'
        else:
            style = 'Non Schengen'

        txt.append(f"""    <Placemark>
        <name>{ic}</name>
        <styleUrl>{style}</styleUrl>
        <Point>
            <coordinates>{lat},{lon}</coordinates>
        </Point>
    </Placemark>
""")
    
    txt.append("""</Document>
</kml>""")
    
    new_txt = ''.join(txt)
    
    file = open('Airports_Points.kml', 'w')
    file.write(new_txt)
    file.close()

    print("Abriendo mapa de aeropuertos en Google Earth...")
    os.startfile('Airports_Points.kml')