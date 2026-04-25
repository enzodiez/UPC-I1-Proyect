class BarcelonaAP():
    def __init__(self, ic='', terminals=[]):
        self.code = ic
        self.terminals = terminals

class Terminal():
    def __init__(self, name='', ba=[], airlCodes=[]):
        self.name = name
        self.boardingAreas = ba
        self.airlCodes = airlCodes

class BoardingArea():
    def __init__(self, name='', tp='', gates=[]):
        self.name = name
        self.type = tp
        self.gates = gates

class Gate():
    def __init__(self, name='', occupied=False, id=''):
        self.name = name
        self.occupied = occupied
        self.id = id

def SetGates(area, init_gate, end_gate, prefix):
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

def LoadAirlines(terminal, t_name):
    try:
        # Si la lista de códigos ICAO de las aerolíneas de la terminal no está vacía la reinicio vacía
        if terminal.airlCodes:
            terminal.airlCodes = []
        
        file = open(f'{t_name}_Airlines.txt', 'r')

        '''Leo las líneas del archivo una a una, separándola por el carácter '\t' que indica una tabulación y
        quedándome solo con el segundo elemento de la lista, lo cual me deja únicamente con el código ICAO
        de la aerolínea, por eso la variable se llama airline_code y no line como la llamaríamos comunmente'''
        airline_code = file.readline().split('\t')[1]
        while airline_code != '':
            # Añado a la lista de códigos ICAO de las aerolíneas de la terminal el código dado y leo otra línea
            terminal.airlCodes.append(airline_code)
            airline_code = file.readline().split('\t')[1]

    except FileNotFoundError:
        return "Error de lectura: archivo no encontrado"