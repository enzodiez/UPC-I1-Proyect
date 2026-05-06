from airport import *
from aircraft import *

class BarcelonaAP():
    def __init__(self, ic='', terminals=None):
        self.code = ic
        self.terminals = terminals if terminals is not None else []

class Terminal():
    def __init__(self, name='', boardingAreas=None, airlCodes=None):
        self.name = name
        self.boardingAreas = boardingAreas if boardingAreas is not None else []
        self.airlCodes = airlCodes if airlCodes is not None else []

class BoardingArea():
    def __init__(self, name='', tp='', gates=None):
        self.name = name
        self.type = tp
        self.gates = gates if gates is not None else []

class Gate():
    def __init__(self, name='', occupied=False, id=''):
        self.name = name
        self.occupied = occupied
        self.id = id

def SetGates(area, init_gate, end_gate, prefix):
    try:
        end_gate = int(end_gate)
        init_gate = int(init_gate)
    except ValueError:
        return -1 # Código de error específico para el caso de no poder convertir (o confirmar) que estas dos variables son enteros

    if end_gate < init_gate:
        # Código de error: -1
        return -2
    # Si la lista de gates del área de embarque no está vacía la reinicio vacía
    if area.gates:
        area.gates = []
    
    # Creo tantos gates como se requieran y los voy añadiendo a la lista 'gates' de 'area'
    for i in range(init_gate, end_gate+1):
        gateName = prefix + "G" + str(i)
        area.gates.append(Gate(name=gateName, occupied=False))
    
    return 0 # Para indicar que todo ha ido bien

def LoadAirlines(terminal, t_name):
    try:
        # Si la lista de códigos ICAO de las aerolíneas de la terminal no está vacía la reinicio vacía
        if terminal.airlCodes:
            terminal.airlCodes = []
        
        with open(f'{t_name}_Airlines.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) >= 2:
                    airline_code = parts[1]  # El código ICAO está en la segunda columna
                    terminal.airlCodes.append(airline_code)
                # Si la línea no tiene el formato esperado la ignoro
        
        return 0 # Para indicar que todo ha ido bien

    except FileNotFoundError:
        return -1

def LoadAirportStructure(filename):
    try:
        with open(filename, 'r') as file:
            # Leo el código ICAO
            line = file.readline()
            while line and line.strip() == '':
                line = file.readline()

            if not line:
                return -2  # archivo vacío
            
            icao = line.strip().split()[0]
            airport = BarcelonaAP(ic=icao)

            # Voy leyendo las siguientes líneas
            line = file.readline()
            while line:
                # Salto las líneas vacías
                line = line.strip()
                if not line:
                    line = file.readline()
                    continue

                parts = line.split()
                if not parts:
                    line = file.readline()
                    continue

                if parts[0] == 'Terminal':
                    if len(parts) < 2:
                        return -3  # Información insuficiente, no están las dos palabras que buscamos: Terminal, nombre de la terminal
                    t_name = parts[1]
                    terminal = Terminal(name=t_name)

                    # Cargar aerolíneas del terminal
                    ret_l_a = LoadAirlines(terminal, t_name)
                    if ret_l_a == -1:
                        return -4  # Error al cargar aerolíneas

                    # Leo la siguiente línea, podría ser 'Area' o 'Terminal'
                    line = file.readline()
                    while line:
                        line = line.strip()
                        if not line:
                            line = file.readline()
                            continue

                        parts = line.split()
                        if not parts:
                            line = file.readline()
                            continue

                        if parts[0] == 'Area':
                            # Valido el formato: "Area Nombre Tipo Gates init_gate - end_gate"
                            if len(parts) < 7 or parts[3] != 'Gates' or parts[5] != '-':
                                return -5 # Formato incorrecto (podría mezclarse información o introducirse información errónea)
                            
                            name = parts[1]
                            type_area = parts[2]
                            try:
                                init_gate = int(parts[4])
                                end_gate = int(parts[6])
                            except ValueError:
                                return -6 # Error en los datos leídos
                            
                            area = BoardingArea(name=name, tp=type_area)
                            prefix = t_name + "BA" + name.lower()
                            ret_s_g = SetGates(area, init_gate, end_gate, prefix)
                            if ret_s_g == -1:
                                return -7 # Fórmato de los índices de los gates incorrecto
                            if ret_s_g == -2:
                                return -8 # Índices de los gates ilógicos
                            
                            terminal.boardingAreas.append(area)
                            line = file.readline()
                        else:
                            # No es 'Area'
                            break  # Salgo del bucle de áreas conservando 'line' para la siguiente terminal

                    airport.terminals.append(terminal)
                else:
                    # Línea inesperada, la ignoro y continuo
                    line = file.readline()

            return airport

    except FileNotFoundError:
        return -1

def GateOccupancy (bcn):
    gates = []
    for terminal in bcn.terminals:
        for area in terminal.boardingAreas:
            for gate in area.gates:
                gates.append(gate)
    return gates

def IsAirlineInTerminal(terminal, name):
    if name == '':
        return False, -1 # Nombre de aerolínea inválido
    
    if not terminal.airlCodes:
        return False, 0
    
    try:
        with open(f'{terminal.name}_Airlines.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) >= 2:
                    airline_name = parts[0].strip()
                    airline_code = parts[1].strip()
                    if airline_name == name:
                        # Compruebo si el código está en la lista de la terminal
                        if airline_code in terminal.airlCodes:
                            return True, 0
        # Si recorro todo el archivo sin encontrar el nombre
        return False, 0
    except FileNotFoundError:
        # Si no existe el archivo, no se puede buscar
        return False, -2 # Segúndo código de error: archivo no encontrado

def SearchTerminal(bcn, name):
    for terminal in bcn.terminals:
        isThere, code = IsAirlineInTerminal(terminal, name)
        if code == -1:
            return -1 # Nombre de aerolínea inválido
        if code == -2:
            return -2 # Error de lectura del archivo
        if isThere:
            return terminal.name
    return ""

def AssignGate(bcn, aircraft):
    terminal_name = SearchTerminal(bcn, aircraft.company)

    if terminal_name == -1:
        return -1 #Error, nombre de aerolínea inválido
    if terminal_name == -2:
        return -2 # Error de lectura de los datos
    if terminal_name == "":
        return -3 # No hay puerta disponible

    flight_schengen = IsSchengenAirport(aircraft.origin_airp)

    for terminal in bcn.terminals:
        if terminal.name == terminal_name:
            for area in terminal.boardingAreas:
                if (flight_schengen and area.type == "Schengen") or (not flight_schengen and area.type == "non-Schengen"):
                    for gate in area.gates:
                        if not gate.occupied:
                            gate.occupied = True
                            gate.id = aircraft.id
                            return 0
    return -4