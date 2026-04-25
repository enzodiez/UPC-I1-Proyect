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
            hora_str = airc.land_time.split(':')[0]
            hr = int(hora_str)
            if 0 <= hr < 24:
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

def MapFlights(aircrafts, filename):
    # Sobreescribe todo el fichero para actualizarlo
    file = open(filename, 'w')
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
    
    # Diccionario para almacenar las coordenadas de los aeropuertos de orígen no repetidos
    origen_coords = {}  # clave: código ICAO, valor: (lon, lat)

    # Creo un diccionario con todos los aeropuertos para poder hacer una búsqueda rápida
    # El VALOR es una tupla (parecido a una lista pero no se puede modificar)
    airport_dict = {}
    for airp in airports:
        airport_dict[airp.icaoCode] = (airp.longitude, airp.latitude)

    # obtengo las coordenadas de LEBL
    if 'LEBL' in airport_dict:
        lonLEBL, latLEBL = airport_dict['LEBL']
    else:
        # Si no se encuentra LEBL cierro archivo y salgo de la función
        file.write("</Document>\n</kml>")
        file.close()
        print("Error: No se encontró LEBL en Airports.txt")
        return
    
    # Guardo los códigos de los aeropuertos de origen en un set() que si hay elementos repetidos solo se queda con uno de ellos.
    # Así evito crear rutas repetidas
    origenes = set()
    for a in aircrafts:
        origenes.add(a.origin_airp)
    
    # Para cada código de los aeropuertos de origen busco sus coordenadas
    lonLatOrigin_airp = []  # lista de [longitud, latitud, código ICAO]
    for codigo in origenes:
        if codigo in airport_dict:
            lon, lat = airport_dict[codigo]
            lonLatOrigin_airp.append([lon, lat, codigo])
        else:
            print(f"Advertencia: No se encontraron coordenadas para {codigo}")
    
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
    os.startfile(filename)

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
        
        # Obtener coordenadas del origen
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

if __name__ == "__main__":
    print("="*60)
    print("TEST VERSIÓN 2 - FLIGHT MANAGEMENT")
    print("="*60)
    
    # ==========================================
    # 1. Test LoadArrivals
    # ==========================================
    print("\n📌 1. Probando LoadArrivals('arrivals.txt')")
    print("-" * 40)
    
    flights = LoadArrivals("arrivals.txt")
    
    if flights:
        print(f"   ✅ Vuelos cargados: {len(flights)}")
        print(f"   Primer vuelo: {flights[0].id} | {flights[0].origin_airp} | {flights[0].land_time} | {flights[0].company}")
        print(f"   Último vuelo: {flights[-1].id} | {flights[-1].origin_airp} | {flights[-1].land_time} | {flights[-1].company}")
    else:
        print("   ❌ Error: No se cargaron vuelos")
        exit()
    
    # ==========================================
    # 2. Test PlotArrivals
    # ==========================================
    print("\n📌 2. Probando PlotArrivals()")
    print("-" * 40)
    
    PlotArrivals(flights)
    print("   ✅ Gráfico de llegadas por hora (se cierra en 3 segundos)")
    plt.ion()
    plt.show(block=False)
    plt.pause(3)
    plt.close()
    
    # ==========================================
    # 3. Test PlotAirlines
    # ==========================================
    print("\n📌 3. Probando PlotAirlines()")
    print("-" * 40)
    
    PlotAirlines(flights)
    print("   ✅ Gráfico de vuelos por aerolínea (se cierra en 3 segundos)")
    plt.show(block=False)
    plt.pause(3)
    plt.close()
    
    # ==========================================
    # 4. Test PlotFlightsType
    # ==========================================
    print("\n📌 4. Probando PlotFlightsType()")
    print("-" * 40)
    
    PlotFlightsType(flights)
    print("   ✅ Gráfico Schengen vs No Schengen (se cierra en 3 segundos)")
    plt.show(block=False)
    plt.pause(3)
    plt.close()
    
    # ==========================================
    # 5. Test SaveFlights
    # ==========================================
    print("\n📌 5. Probando SaveFlights()")
    print("-" * 40)
    
    SaveFlights(flights, "ArrivalsToLEBL.txt")
    
    if os.path.exists("ArrivalsToLEBL.txt"):
        with open("ArrivalsToLEBL.txt", "r") as f:
            lines = f.readlines()
        print(f"   ✅ Archivo guardado: {len(lines)} líneas")
        print(f"   Primera línea: {lines[0].strip()}")
    else:
        print("   ❌ Error: No se creó el archivo")
    
    # ==========================================
    # 6. Test MapFlights
    # ==========================================
    print("\n📌 6. Probando MapFlights()")
    print("-" * 40)
    
    MapFlights(flights, 'LEBL_Arrivals.kml')
    input()
    
    if os.path.exists("LEBL_Arrivals.kml"):
        print("   ✅ Archivo KML creado: LEBL_Arrivals.kml")
    else:
        print("   ❌ Error: No se creó el archivo KML")
    
    # ==========================================
    # 7. Test LongDistanceArrivals
    # ==========================================
    print("\n📌 7. Probando LongDistanceArrivals()")
    print("-" * 40)
    
    long_flights = LongDistanceArrivals(flights)
    print(f"   ✅ Vuelos de larga distancia (>2000km): {len(long_flights)}")
    
    if long_flights:
        print("   Primeros 5 vuelos de larga distancia:")
        for f in long_flights[:5]:
            print(f"      - {f.id} desde {f.origin_airp}")
    
    MapFlights(long_flights, 'LEBL_Arrivals_MIN2000.kml')
    
    if os.path.exists("LEBL_Arrivals_MIN2000.kml"):
        print("   ✅ Archivo KML creado: LEBL_Arrivals_MIN2000.kml")
    else:
        print("   ❌ Error: No se creó el archivo KML")
    
    # ==========================================
    # RESULTADO FINAL
    # ==========================================
    print("\n" + "="*60)
    print("🎉 TEST VERSIÓN 2 COMPLETADO")
    print("="*60)
    print("\n✅ Si no has visto errores, todas las funciones funcionan correctamente.")
    print("✅ Archivos creados: ArrivalsToLEBL.txt, LEBL_Arrivals.kml, LEBL_Arrivals_MIN2000.kml")