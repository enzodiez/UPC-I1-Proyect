from airport import IsSchengenAirport as ISA

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
        apdata.append(''.join(f"{name} {lat:0.5f} {lon:0.5f}"))
    F.close()
    return apdata



def Convertir_a_gms (value, positive, negative): #Defino esta función para pasar de grados a grados, minutos y segundos, con la N, S, W y E como en el documento airports.txt, por si hace falta en algún momento
    direction = positive if value >= 0 else negative
    value = abs(value)

    degrees = int(value)
    minutes = int((value - degrees) * 60)
    seconds = int((((value - degrees) * 60) - minutes) * 60)

    return f"{direction}{degrees:02d}{minutes:02d}{seconds:02d}"


#Ahora, suponiendo que los aeropuesrtos a agregar se dan del modo: aeropuerto = {"code": "LEBL", "lat": 41.26589, "lon": 2.08545}
def AddAirportlist (airports, airport):
    for a in airports:
        if a["code"] == airport["code"]:
            return "Este aeropuerto ya se encuentra en la lista"
    
    airports.append(airport)
    return "Aeropuerto agregado"


def AddAirport (airports, airport):
    f = open(documentodeaeropuertos, "r") #pon el documento de airports.txt
    for line in f:
        if line.startswith(airport["code"]):
            f.close()
            return "Este aeropuerto ya se encuentra en la lista"
    f.close()
    f = open(documentodeaeropuertos, "a")
    lat = Convertir_a_gms (airport["lat"], 'N', 'S')
    lon = Convertir_a_gms (airport["lon"], 'E', 'W')
    f.write(f"{airport["code"]} {lat} {lon}\n")
    f.close()
    return "Aeropuerto agregado"


def RemoveAirportlist (airports, code):
    for i in range(len(airports)):
        if airports[i]["code"] == code:
            airports.pop(i)
            return "Aeropuerto eliminado"
    return "Este aeropuerto no se encuentra en la lista"


def RemoveAirport(airports, code):
    f = open(documentodeaeropuertos, "r")
    lines = f.readlines()
    f.close()
    encontrado = False
    nuevas_lineas = []
    for line in lines:
        if line.startswith(code):
            encontrado = True
        else:
            nuevas_lineas.append(line)
    if not encontrado:
        return "Este aeropuerto no se encuentra en la lista"
    f = open("airports.txt", "w")
    for line in nuevas_lineas:
        f.write(line)
    f.close()
    return "Aeropuerto eliminado"