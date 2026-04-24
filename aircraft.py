from airport import IsSchengenAirport, LoadAirports, Airport, SetSchengen, PlotAirports
import os
import matplotlib.pyplot as plt
import math

class Aircraft():
    def __init__(self, id="", cmp="", origin_airp="", land_time=""):
        self.id = id
        self.company = cmp
        self.origin_airp = origin_airp
        self.land_time = land_time

def LoadArrivals(filename):
    try:
        arrivals = []
        file = open(filename, 'r')
        # Leo dos veces para saltarme el encabezado
        line = file.readline()
        line = file.readline()

        while line != "":
            line = line.split()
            if len(line) < 4: # Asegurar una correcta estructura
                continue
            aircraft_id = line[0]
            origin = line[1]
            arrival_time = line[2]
            company = line[3]

            plane = Aircraft(
                id=aircraft_id,
                cmp=company,
                origin_airp=origin,
                land_time=arrival_time
            )
            arrivals.append(plane)
            
            line = file.readline()
        
        file.close()

        return arrivals

    except FileNotFoundError:
            return []

def PlotArrivals(aircrafts):
    if not aircrafts:
        return "Error en los datos recibidos. No se encontró información."
    else:
        frq = [0]*24
        hours = range(0,24)
        for airc in aircrafts:
            hr = int(airc.land_time[0] + airc.land_time[1])
            frq[hr] += 1
    fig, ax = plt.subplots()
    ax.plot(hours, frq, color='skyblue', linewidth=2)
    ax.set_xlabel("Arrival times", fontsize=12)
    ax.set_ylabel("Number of flights", fontsize=12)
    ax.set_title('Frecuencia de aterrizajes', fontsize=14, fontweight='bold')
    fig.tight_layout()
    return fig

def SaveFlights(aircrafts, filename):
    if not aircrafts:
        return "ERROR", "Error en los datos recibidos. No se encontró información."
    else:
        file = open(filename, 'w')
        i = 0
        while i < len(aircrafts):
            a = aircrafts[i]
            txt = f"{a.id or '-'} {a.origin_airp or '-'} {a.land_time or '-'} {a.company or '-'}"
            file.write(txt+'\n')
            i += 1
        file.close()
        '''
        LO MISMO PERO MÁS REDUCIDO
        ---------------------------
        for aircraft in aircrafts:
        txt = f"{aircraft.id or '-'} {aircraft.origin_airp or '-'} {aircraft.land_time or '-'} {aircraft.company or '-'}"
        file.write(txt)
        '''
        return "INFO", "Registro de llegadas a LEBL hoy guardado correctamente."

def PlotAirlines(aircrafts):
    if not aircrafts:
        return "Error en los datos recibidos. No se encontró información."
    else:
        airline_flights = {}
        for airc in aircrafts:
            # Usar get para inicializar en 0 si no existe
            airline_flights[airc.company] = airline_flights.get(airc.company, 0) + 1
        
        # Del diccionario hago dos listas, una para cada eje del gráfico, con las claves y los valores
        claves = list(airline_flights.keys())
        valores = list(airline_flights.values())

        # Creo el gráfico de barras
        fig, ax = plt.subplots()
        bars = ax.bar(claves, valores, color='skyblue', edgecolor='black')

        # Personalizo el gráfico
        ax.set_xlabel('Aerolíneas', fontsize=12)
        ax.set_ylabel('Número de vuelos', fontsize=12)
        ax.set_title('Vuelos a LEBL por aerolínea', fontsize=14, fontweight='bold')

        # Roto etiquetas, por si hay muchas aerolíneas
        ax.tick_params(axis='x', rotation=45)

        # Mostrar valores sobre las barras
        for bar, valor in zip(bars, valores):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(valor), ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        # Ajusto el límite superior del eje Y para que quepa el texto
        ax.set_ylim(0, max(valores) + max(valores) * 0.1)

        fig.tight_layout()
        # fig.show() Lo he anulado para que no interfiera en su uso en la interfaz gráfica. Ya se muestra ahí.
        return fig

def PlotFlightsType(aircrafts):
    if not aircrafts:
        return "Error en los datos recibidos. No se encontró información."
    else:
        airports = []
        for airc in aircrafts:
            airp = Airport(ic=airc.origin_airp)
            SetSchengen(airp)
            airports.append(airp)
        
        fig = PlotAirports(airports, titulo='Arrivals from Schengen airports VS No Schengen airports')

        return fig

def MapFlights(aircrafts):
    # Sobreescribe todo el fichero para actualizarlo
    file = open('LEBL_Arrivals.kml', 'w')
    file.write("""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <Style id="Schengen">
        <LineStyle>
            <color>ff00ff00</color>
            <width>3</width>
            <colorMode>normal</colorMode>
        </LineStyle>
    </Style>
    <Style id="Non Schengen">
        <LineStyle>
            <color>ff0000ff</color>
            <width>3</width>
            <colorMode>normal</colorMode>
        </LineStyle>
    </Style>
""")
    
    airports = LoadAirports('Airports.txt')
    lonLEBL, latLEBL = 0, 0
    lonLatOrigin_airp = [] # Los elementos son listas de longitud=3 que contiene la longitud, la latitud y el código ICAO (en ese orden) de los aircrafts de la lista aircrafts

    for elem in airports:
        if elem.icaoCode == 'LEBL':
            lonLEBL, latLEBL = elem.longitude, elem.latitude
        else:
            for n in range(len(aircrafts)):
                if elem.icaoCode == aircrafts[n].origin_airp:
                    lonLatOrigin_airp.append([elem.longitude, elem.latitude, elem.icaoCode])
    
    for i in range(len(lonLatOrigin_airp)):
        name = f"Route {lonLatOrigin_airp[i][2]} - LEBL"

        if IsSchengenAirport(lonLatOrigin_airp[i][2]):
            style = 'Schengen'
        else:
            style = 'Non Schengen'

        file.write(f"""    <Placemark>
        <name>{name}</name>
        <styleUrl>#{style}</styleUrl>
        <LineString>
            <altitudeMode>clampToGround</altitudeMode>
            <extrude>1</extrude>
            <tessellate>1</tessellate>
            <coordinates>
                {lonLatOrigin_airp[i][0]},{lonLatOrigin_airp[i][1]}
                {lonLEBL},{latLEBL}
            </coordinates>
        </LineString>
    </Placemark>
""")
    
    file.write("""</Document>
</kml>""")
    
    file.close()

    print("Abriendo mapa de vuelos a LEBL hoy en Google Earth...")
    os.startfile('LEBL_Arrivals.kml')

def LongDistanceArrivals(aircrafts):
    airports = LoadAirports('Airports.txt')

    # Creo diccionario de aeropuertos para hacer una búsqueda más rápida y sencilla
    airport_coords = {}
    for airport in airports:
        airport_coords[airport.icaoCode] = (airport.latitude, airport.longitude)
    
    # Obtengo las coordenadas de LEBL, si no se encuentra no se podrá calcular la distancia
    if 'LEBL' not in airport_coords:
        print("Error: No se encontró LEBL en la base de datos")
        return []
    
    lat_lebl_deg = float(airport_coords['LEBL'][0])
    lon_lebl_deg = float(airport_coords['LEBL'][1])

    # Convierto a radianes
    lat_lebl_rad = math.radians(lat_lebl_deg)
    lon_lebl_rad = math.radians(lon_lebl_deg)

    long_distance_aircrafts = []
    
    for aircraft in aircrafts:
        origin_code = aircraft.origin_airp
        
        # Verificar que el aeropuerto de origen existe
        if origin_code not in airport_coords:
            print(f"Advertencia: No se encontraron coordenadas para {origin_code}")
            continue
        
        # Obtener las coordenadas del origen
        lat_origin_deg = float(airport_coords[origin_code][0])
        lon_origin_deg = float(airport_coords[origin_code][1])
        
        # Convertir a radianes
        lat_origin_rad = math.radians(lat_origin_deg)
        lon_origin_rad = math.radians(lon_origin_deg)
        
        # Calcular distancia usando Haversine
        distance = haversine_distance(lat_lebl_rad, lon_lebl_rad, 
                                      lat_origin_rad, lon_origin_rad)
        
        # Si la distancia es mayor a 2000 km la a la lista
        if distance > 2000:
            long_distance_aircrafts.append(aircraft)
    
    return long_distance_aircrafts

def haversine_distance(lat1_rad, lon1_rad, lat2_rad, lon2_rad):
    """
    Calcula la distancia Haversine entre dos puntos en la superficie terrestre.
    
    Args:
        lat1_rad, lon1_rad: Coordenadas del punto 1 en radianes
        lat2_rad, lon2_rad: Coordenadas del punto 2 en radianes
    
    Returns:
        Distancia en kilómetros
    """
    r = 6371  # Radio de la Tierra en km
    
    dlat = abs(lat1_rad - lat2_rad)
    dlon = abs(lon1_rad - lon2_rad)
    
    # Fórmula de Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = r * c
    
    return distance