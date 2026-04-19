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

def SetSchengen(airport: Airport): # Que airport sea un objeto/instancia Airport
    if IsSchengenAirport(airport.icaoCode):
        airport.schengen = True

def PrintAirport(airport: Airport): # Que airport sea un objeto Airport
    print(f"El código ICAO del aeropuerto es: {airport.icaoCode}")
    print(f"Latitud: {airport.latitude}")
    print(f"Longitud: {airport.longitude}")
    print(f"Pertenece a la zona Schengen: {airport.schengen}")

'''def SaveSchengenAirports(airports, filename):
    with open(filename, 'r', encoding='utf-8') as file:
        schAirp = file.readlines()
    
    for airp in airports:
        if IsSchengenAirport(airp.icaoCode):
            found = False
            cnt = 0
            while not found and cnt < len(schAirp):
                ic, lat, lon = schAirp[cnt].split()
                if airp.icaoCode == ic:
                    found = True
                cnt += 1
            if not found:
                latitud = Convertir_a_gms(float(airp.latitude), 'N', 'S')
                longitud = Convertir_a_gms(float(airp.longitude), 'E', 'W')
                line = f'{airp.icaoCode} {latitud} {longitud}'
                schAirp.append(line)
    
    with open(filename, 'w', encoding='utf-8') as file:
        for linea in schAirp:
            file.write(f'{linea}\n')'''
def SaveSchengenAirports(airports, filename):
    # Leeo y limpio los saltos de línea con splitlines()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # splitlines() elimina los \n automáticamente
            schAirp = file.read().splitlines()
    except FileNotFoundError:
        schAirp = []
    
    for airp in airports:
        if IsSchengenAirport(airp.icaoCode):
            found = False
            cnt = 0
            
            while not found and cnt < len(schAirp):
                try:
                    partes = schAirp[cnt].split()
                    if partes: # Si la línea no está vacía
                        ic = partes[0]
                        if airp.icaoCode == ic:
                            found = True
                except IndexError:
                    pass
                cnt += 1
                
            if not found:
                latitud = Convertir_a_gms(float(airp.latitude), 'N', 'S')
                longitud = Convertir_a_gms(float(airp.longitude), 'E', 'W')
                line = f'{airp.icaoCode} {latitud} {longitud}'
                schAirp.append(line)
    
    # Reescribir el archivo actualizado
    with open(filename, 'w', encoding='utf-8') as file:
        for linea in schAirp:
            if linea.strip(): # Solo escribir si la línea tiene contenido, para evitar problemas
                file.write(f'{linea}\n')

def PlotAirports(airports, titulo='Schengen airports VS No Schengen airports'):
    sch, nSch = 0, 0
    for airport in airports:
        if IsSchengenAirport(f"{airport.icaoCode[0]}{airport.icaoCode[1]}"):
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
    ax.set_title(titulo)
    ax.legend()
    
    # fig.show() Lo he anulado para que no interfiera en su uso en la interfaz gráfica. Ya se muestra ahí.

    return fig

def MapAirports(airports):
    # Sobreescribe todo el fichero para actualizarlo
    txt = []
    txt.append("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
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
    </Style>
""")

    for i in range(len(airports)):
        ic = airports[i].icaoCode
        lat = airports[i].latitude
        lon = airports[i].longitude

        if IsSchengenAirport(ic):
            style = 'Schengen'
        else:
            style = 'Non Schengen'

        txt.append(f"""    <Placemark>
        <name>{ic}</name>
        <styleUrl>#{style}</styleUrl>
        <Point>
            <coordinates>{lon},{lat},0</coordinates>
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

def LoadAirports (filename):
    F = open(filename,'r')
    apdata = [] #apdata=airports data
    line = F.readline()
    # apdata.append(''.join(f"{line}"))
    line = F.readline()
    while line != '':
        name, lat, lon = (line.split())
        line = F.readline()
        n_s = lat[0] #norte o sur
        lat = float(lat[1:])
        w_e = lon[0] #oeste o este
        lon = float(lon[1:])
        sec_lat = lat%100 #segundos de la latitud
        lat = lat//100
        sec_lat = sec_lat/3600
        min_lat = lat%100 #minutos de la latitud
        lat = lat//100
        min_lat = min_lat/60
        lat = lat + sec_lat + min_lat
        if n_s == "S":
            lat = -lat
        sec_lon = lon%100 #segundos de la longitud
        lon = lon//100
        sec_lon = sec_lon/3600
        min_lon = lon%100 #minutos de la longitud
        lon = lon//100
        min_lon = min_lon/60
        lon = lon + sec_lon + min_lon
        if w_e == "W":
            lon = -lon
        airp = Airport(name, float(f"{lat:0.5f}"), float(f"{lon:0.5f}"))
        SetSchengen(airp)
        apdata.append(airp)
    F.close()
    return apdata

def Convertir_a_gms (value, positive, negative): #Defino esta función para pasar de grados a grados, minutos y segundos, con la N, S, W y E como en el documento airports.txt, por si hace falta en algún momento
    #positive es N o E, negative es S o W
    direction = positive if value >= 0 else negative
    value = abs(value)

    degrees = int(value)
    minutes = int((value - degrees) * 60)
    seconds = int((((value - degrees) * 60) - minutes) * 60)

    return f"{direction}{degrees:02d}{minutes:02d}{seconds:02d}"

def AddAirport (airports, airport):
    for airp in airports:
        if airp.icaoCode == airport.icaoCode:
            return False
    
    airports.append(airport)
    SaveSchengenAirports(airports, 'SchengenAirports.txt')
    return True

def RemoveAirport (airports, code):
    for i in range(len(airports)):
        if airports[i].icaoCode == code.upper():
            del airports[i]
            return True
    return False