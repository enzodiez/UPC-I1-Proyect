class BarcelonaAP():
    def __init__(self, ic='', terminals=None):
        self.code = ic
        self.terminals = terminals if terminals is not None else []

class Terminal():
    def __init__(self, name='', ba=None, airlCodes=None):
        self.name = name
        self.boardingAreas = ba if ba is not None else []
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
        return -2 # Código de error específico para el caso de no poder convertir (o confirmar) que estas dos variables son enteros

    if end_gate < init_gate:
        # Código de error: -1
        return -1
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
        return -1 # Mismo código de error que para SetGates()

def IsAirlineInTerminal(terminal, name):
    if name == '':
        return False, -1
    
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