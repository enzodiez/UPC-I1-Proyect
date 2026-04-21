from airport import IsSchengenAirport, LoadAirports, Airport, SetSchengen, PlotAirports
import os
import matplotlib.pyplot as plt

class Aircraft():
    def __init__(self, id="", cmp="", origin_airp="", land_time=""):
        self.id = id
        self.company = cmp
        self.origin_airp = origin_airp
        self.land_time = land_time

def LoadArrivals(filename):
    arrivals = []

    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        for line in lines[1:]:
            if len(line) < 4: #asegurar una correcta estructura
                continue
            parts = line.split()
            aircraft_id = parts[0]
            origin = parts[1]
            arrival_time = parts[2]
            company = parts[3]

            plane = Aircraft(
                id=aircraft_id,
                cmp=company,
                origin_airp=origin,
                land_time=arrival_time
            )

            arrivals.append(plane)

        except FileNotFoundError:
            return []

    return arrivals






def PlotArrivals():


def SaveFlights(aircrafts, filename):
    if not aircrafts:
        return "Error en los datos recibidos. No se encontró información."
    else:
        file = open(filename, 'w')
        i = 0
        while i < len(aircrafts):
            a = aircrafts[i]
            txt = f"{a.id or "-"} {a.origin_airp or "-"} {a.land_time or "-"} {a.company or "-"}"
            file.write(txt)
            i += 1
        file.close()
        '''
        LO MISMO PERO MÁS REDUCIDO
        ---------------------------
        for aircraft in aircrafts:
        txt = f"{aircraft.id or '-'} {aircraft.origin_airp or '-'} {aircraft.land_time or '-'} {aircraft.company or '-'}"
        file.write(txt)
        '''
        return "Registro de llegadas a LEBL hoy guardado correctamente."

def PlotAirlines(aircrafts):
    if not aircrafts:
        return "Error en los datos recibidos. No se encontró información."
    else:
        airline_flights = {}
        for airc in aircrafts:
            airline_flights[airc.company] += 1
        
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
        ax.tick_params(axis='x', rotation=45, ha='right')

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
    
    airports = LoadAirports('Airports.txt')
    lonLEBL, latLEBL = 0, 0
    lonLatIndx = [] # Los elementos son listas de longitud=3 que contiene la longitud, la latitud y el índice (en ese orden) de los aircrafts de la lista aircrafts

    for elem in airports:
        if elem.icaoCode == 'LEBL':
            lonLEBL, latLEBL = elem.longitude, elem.latitude
        else:
            for n in range(len(aircrafts)):
                if elem.icaoCode == aircrafts[n].id:
                    lonLatIndx.append([elem.longitude, elem.latitude, n])
    
    # Ordeno la lista lonLatIndx según el índice de las listas "elemento" para tenerla en el mismo orden que la lista aircrafts
    lonLatIndx.sort(key=lambda x: x[2])
    
    for i in range(len(aircrafts)):
        a = aircrafts[i]
        ic = a.origin_airp
        name = f"Route {ic} - LEBL"

        if IsSchengenAirport(ic):
            style = 'Schengen'
        else:
            style = 'Non Schengen'

        txt.append(f"""    <Placemark>
        <name>{name}</name>
        <styleUrl>#{style}</styleUrl>
        <LineString>
            <altitudeMode<clampToGround</altitudeMode>
            <extrude>1</extrude>
            <tessellate>1</tessellate>
            <coordinates>
                {lonLatIndx[i][0]},{lonLatIndx[i][1]}
                {lonLEBL},{latLEBL}
            </coordinates>
        </LineString>
    </Placemark>
""")
    
    txt.append("""</Document>
</kml>""")
    
    new_txt = ''.join(txt)

    file = open('LEBL_Arrivals.kml', 'w')
    file.write(new_txt)
    file.close()

    print("Abriendo mapa de vuelos a LEBL hoy en Google Earth...")
    os.startfile('LEBL_Arrivals.kml')