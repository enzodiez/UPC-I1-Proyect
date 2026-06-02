from airport import IsSchengenAirport, Airport, SetSchengen, PlotAirports, LoadAirports
import os
import matplotlib.pyplot as plt
import math

class Aircraft():
    # Representa un vuelo (llegada o salida) con identificador, compañía, origen y hora de aterrizaje.
    def __init__(self, id="", cmp="", origin_airp="", land_time="", destination_airp="", departure_time=""):
        self.id = id
        self.company = cmp
        self.origin_airp = origin_airp
        self.land_time = land_time
        self.destination_airp = destination_airp
        self.departure_time = departure_time

def normalize_time(time_str):
    """
    Función extra.
    Convierte una cadena de tiempo en formato 'h:mm', 'hh:mm', 'h:m' o 'hh:m' a 'hh:mm'.
    Ejemplos: '0:04' -> '00:04', '1:24' -> '01:24', '12:3' -> '12:03'
    """
    if not time_str:
        return ""
    parts = time_str.split(':')
    if len(parts) != 2:
        return time_str  # Formato inesperado, se devuelve igual.
    hour = parts[0].zfill(2)      # Rellena con cero a la izquierda hasta 2 dígitos.
    minute = parts[1].zfill(2)    # Rellena con cero a la izquierda hasta 2 dígitos.
    return f"{hour}:{minute}"

def LoadArrivals(filename):
    """
    Carga desde un archivo de texto una lista de objetos Aircraft (llegadas).
    Salta la cabecera, ignora líneas con formato incorrecto.
    Devuelve la lista de vuelos, o vacía si el archivo no existe.
    """
    try:
        arrivals = []
        with open(filename, 'r') as file:
            # Saltar la primera línea (cabecera)
            next(file, None)
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) < 4:
                    continue   # Ignorar líneas con formato incorrecto
                aircraft_id = parts[0]
                origin = parts[1]
                if len(origin) != 4:
                    continue
                else:
                    valid = True
                    for ch in origin:
                        if not ('a' <= ch <= 'z' or 'A' <= ch <= 'Z'):
                            valid = False
                            break
                    if not valid:
                        continue
                arrival_time = normalize_time(parts[2])
                company = parts[3]
                plane = Aircraft(
                    id=aircraft_id,
                    cmp=company,
                    origin_airp=origin,
                    land_time=arrival_time
                )
                arrivals.append(plane)
        return arrivals
    except FileNotFoundError:
        return []

def PlotArrivals(aircrafts):
    """
    Recibe una lista de Aircraft y muestra un gráfico de líneas con la frecuencia
    de llegadas por cada hora del día (0 a 23). Devuelve la figura de matplotlib.
    """
    if not aircrafts:
        return "Error en los datos recibidos. No se encontró información."
    else:
        frq = [0]*24
        hours = range(0,24)
        for airc in aircrafts:
            if airc.land_time != "":
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
    """
    Guarda la lista de Aircraft en un archivo de texto con el formato:
    id origen tiempo compañía. Si la lista está vacía, retorna un error.
    Devuelve una tupla (tipo_mensaje, texto).
    """
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
    """
    Gráfico de barras con el número de vuelos por aerolínea (código ICAO).
    Las barras tienen el número sobre ellas y las etiquetas rotadas 90°.
    Devuelve la figura de matplotlib.
    """
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
        fig, ax = plt.subplots(figsize=(16, 6))
        bars = ax.bar(claves, valores, color='skyblue', edgecolor='black')

        # Personalizo el gráfico
        ax.set_xlabel('Aerolíneas', fontsize=12)
        ax.set_ylabel('Número de vuelos', fontsize=12)
        ax.set_title('Vuelos a LEBL por aerolínea', fontsize=14, fontweight='bold')

        # Roto etiquetas, por si hay muchas aerolíneas
        ax.tick_params(axis='x', rotation=90, labelsize=13)

        # Ajustar los límites del eje X para eliminar márgenes laterales excesivos
        # Por defecto hay un margen del 5% a cada lado, lo reducimos a 0
        ax.margins(x=0.01)  # margen lateral mínimo
        # También podemos forzar el límite exacto
        # ax.set_xlim(-0.5, n - 0.5)

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
    """
    Gráfico de barras apiladas (Schengen vs. no Schengen) para los vuelos de llegada.
    Utiliza la información de origen de cada vuelo y la función IsSchengenAirport.
    Devuelve la figura de matplotlib.
    """
    if not aircrafts:
        return "Error en los datos recibidos. No se encontró información."
    else:
        airports = []
        for airc in aircrafts:
            if airc.origin_airp != "":
                airp = Airport(ic=airc.origin_airp)
                SetSchengen(airp)
                airports.append(airp)
        
        fig = PlotAirports(airports, titulo='Arrivals from Schengen airports VS No Schengen airports')

        return fig

def MapFlights(aircrafts, filename, airports):
    """
    Genera un archivo KML con las rutas desde cada aeropuerto de origen hasta LEBL.
    Colorea las líneas según si el origen es Schengen (verde) o no (rojo).
    Abre automáticamente el archivo en Google Earth si está instalado.
    """

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

    lonLEBL, latLEBL = 0, 0

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

    os.startfile(filename)

def LongDistanceArrivals(aircrafts, airports):
    """
    Filtra y devuelve una lista con los vuelos cuyo aeropuerto de origen se encuentra
    a más de 2000 km de LEBL (distancia calculada mediante la fórmula de Haversine).
    """

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

def LoadDepartures(filename):
    """
    Carga desde un archivo de texto una lista de objetos Aircraft (solo salidas).
    Formato: AIRCRAFT DESTINATION DEPARTURE AIRLINE
    Salta la cabecera, ignora líneas con formato incorrecto.
    Devuelve la lista de vuelos de salida, o vacía si el archivo no existe.
    """
    try:
        departures = []
        with open(filename, 'r') as file:
            # Saltar la primera línea (cabecera)
            next(file, None)
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) < 4:
                    continue   # Ignorar líneas con formato incorrecto
                aircraft_id = parts[0]
                destination = parts[1]
                if len(destination) != 4:
                    continue
                else:
                    valid = True
                    for ch in destination:
                        if not ('a' <= ch <= 'z' or 'A' <= ch <= 'Z'):
                            valid = False
                            break
                    if not valid:
                        continue
                departure_time = normalize_time(parts[2])
                company = parts[3]
                plane = Aircraft(
                    id=aircraft_id,
                    cmp=company,
                    destination_airp=destination,
                    departure_time=departure_time
                )
                departures.append(plane)
        return departures, 0 # Código = 0: Todo bien
    except FileNotFoundError:
        return [], -1 # Código = -1: Archivo no encontrado

def time_to_minutes(t):
    """
    Función extra para convertir hora "hh:mm" a minutos para comparar.
    Sirve para ahorrar trabajo en la función MergeMovements.
    """
    if not t:
        return -1
    parts = t.split(':')
    return int(parts[0]) * 60 + int(parts[1])

def MergeMovements(arrivals, departures):
    """
    Combina listas de llegadas y salidas. Para cada avión, primero verifica que no haya
    incoherencias (dos llegadas seguidas o dos salidas seguidas).
    Si las hay, se añade su ID a la lista de problemáticos y se omite todo el avión.
    Si no las hay, se emparejan llegadas con salidas posteriores (arrival < departure).
    Devuelve:
        - merged: lista de Aircraft (con todos los campos cuando hay pareja)
        - problem_ids: lista de IDs con incoherencias
        - code: 0 si éxito, -1 si alguna lista de entrada está vacía
    """
    if not arrivals or not departures:
        return [], [], -1 # Error: alguna lista vacía
    
    # Diccionario para almacenar todos los eventos por id
    events_by_id = {}
    for a in arrivals:
        events_by_id.setdefault(a.id, []).append(('arrival', time_to_minutes(a.land_time), a))
    for d in departures:
        events_by_id.setdefault(d.id, []).append(('departure', time_to_minutes(d.departure_time), d))

    merged = []
    problem_ids = []

    for aid, events in events_by_id.items():
        # Ordenar eventos por tiempo (y si hay igualdad, las llegadas primero para evitar ambigüedades)
        events.sort(key=lambda x: (x[1], 0 if x[0] == 'arrival' else 1))
        
        # Detectar incoherencias
        has_incoherence = False
        prev_type = None
        for typ, _, _ in events:
            if typ == prev_type:
                has_incoherence = True
                break
            prev_type = typ

        if has_incoherence:
            problem_ids.append(aid)
            continue   # Saltamos este avión por completo

        # Si no hay problemas con las horas del avión:
        pending_arrival = None
        for typ, t, obj in events:
            if typ == 'arrival':
                # Si ya había una llegada pendiente (no debería, porque no hay dos llegadas seguidas)
                if pending_arrival is not None:
                    # Por si acaso, pero aquí no debería ocurrir
                    merged.append(pending_arrival)
                pending_arrival = obj
            else:  # departure
                if pending_arrival is not None:
                    # Emparejar llegada pendiente con esta salida
                    combined = Aircraft(
                        id=aid,
                        cmp=pending_arrival.company,
                        origin_airp=pending_arrival.origin_airp,
                        land_time=pending_arrival.land_time,
                        destination_airp=obj.destination_airp,
                        departure_time=obj.departure_time
                    )
                    merged.append(combined)
                    pending_arrival = None
                else:
                    # Salida sin llegada previa (avión de la noche)
                    merged.append(obj)

        # Si queda alguna llegada sin emparejar al final (no debería por la ausencia de incoherencias,
        # pero puede pasar si hay más llegadas que salidas)
        if pending_arrival is not None:
            merged.append(pending_arrival)

    return merged, problem_ids, 0

def NightAircraft(aircrafts):
    if not aircrafts:
        return [], -1 # Código de error de lista vacía
    night_aircrafts = []
    for airc in aircrafts:
        if airc.land_time == "":
            # Compruebo que el avión NO tenga hora de llegada
            if airc.departure_time != "":
                # Compruebo que el avión tenga hora de salida
                night_aircrafts.append(airc)
    
    return night_aircrafts, 0 # Código que avisa de que todo ha ido bien

if __name__ == "__main__":
    airports = LoadAirports("Airports.txt")

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
    
    MapFlights(flights, 'LEBL_Arrivals.kml', airports)
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
    
    long_flights = LongDistanceArrivals(flights, airports)
    print(f"   ✅ Vuelos de larga distancia (>2000km): {len(long_flights)}")
    
    if long_flights:
        print("   Primeros 5 vuelos de larga distancia:")
        for f in long_flights[:5]:
            print(f"      - {f.id} desde {f.origin_airp}")
    
    MapFlights(long_flights, 'LEBL_Arrivals_MIN2000.kml', airports)
    
    if os.path.exists("LEBL_Arrivals_MIN2000.kml"):
        print("   ✅ Archivo KML creado: LEBL_Arrivals_MIN2000.kml")
    else:
        print("   ❌ Error: No se creó el archivo KML")
    
    # ==========================================
    # NUEVOS TESTS VERSIÓN 4
    # ==========================================
    print("\n" + "="*60)
    print("TEST VERSIÓN 4 - NUEVAS FUNCIONES (SALIDAS, FUSIÓN, NOCTURNOS)")
    print("="*60)

    # 1. Test LoadDepartures
    print("\n📌 1. Probando LoadDepartures('Departures.txt')")
    departures, code_dep = LoadDepartures("Departures.txt")
    if code_dep == 0:
        print(f"   ✅ Salidas cargadas: {len(departures)}")
        if departures:
            print(f"   Primera salida: {departures[0].id} -> {departures[0].destination_airp} a las {departures[0].departure_time}")
    else:
        print("   ⚠️ No se pudo cargar Departures.txt. Se usará una lista vacía para pruebas posteriores.")
        departures = []

    # 2. Test MergeMovements (si tenemos arrivals y departures)
    print("\n📌 2. Probando MergeMovements()")
    if flights and departures:
        merged, problem_ids, code_merge = MergeMovements(flights, departures)
        if code_merge == 0:
            print(f"   ✅ Fusión completada: {len(merged)} vuelos combinados")
            if problem_ids:
                print(f"   ⚠️ Aeronaves con incoherencias horarias: {problem_ids}")
            else:
                print("   ✅ No se detectaron incoherencias.")
            # Mostrar algunos ejemplos
            if merged:
                print("   Ejemplos de vuelos fusionados:")
                count = 0
                for a in merged:
                    if a.origin_airp and a.destination_airp:
                        print(f"      - {a.id}: llega de {a.origin_airp} a {a.land_time} -> sale a {a.destination_airp} a {a.departure_time}")
                        count += 1
                        if count >= 3:
                            break
                if count == 0:
                    print("      (No hay vuelos con llegada y salida emparejados)")
        else:
            print("   ❌ Error en MergeMovements (código -1)")
    else:
        print("   ⚠️ No se puede probar MergeMovements: faltan llegadas o salidas.")

    # 3. Test NightAircraft
    print("\n📌 3. Probando NightAircraft()")
    # Usar la lista fusionada si existe, si no, usar solo salidas
    test_list = merged if 'merged' in locals() and merged else departures
    if test_list:
        night, code_night = NightAircraft(test_list)
        if code_night == 0:
            print(f"   ✅ Aviones nocturnos (solo salida): {len(night)}")
            for a in night[:3]:
                print(f"      - {a.id} sale a {a.destination_airp} a las {a.departure_time}")
        else:
            print("   ❌ Error en NightAircraft (lista vacía)")
    else:
        print("   ⚠️ No hay datos para probar NightAircraft.")

    # ==========================================
    # RESULTADO FINAL
    # ==========================================
    print("\n" + "="*60)
    print("🎉 TEST VERSIÓN 2 + EXTENSIÓN DE LA VERSIÓN 4 COMPLETADO")
    print("="*60)
    print("\n✅ Si no has visto errores, todas las funciones funcionan correctamente.")
    print("✅ Archivos creados: ArrivalsToLEBL.txt, LEBL_Arrivals.kml, LEBL_Arrivals_MIN2000.kml")