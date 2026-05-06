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

def IsAirlineInTerminal(terminal, icao_code):
    '''
    Información importante!!! Esta función estaba pensada originalmente en el documento del proyecto para trabajar buscando con el
    nombre de la aerolínea. No obstante se nos hace mucho más fácil trabajar buscando por el código ICAO, es por eso que la búsqueda
    se realiza mediante el ICAO y no el nombre de la aerolínea.
    '''

    '''
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
        return False, -2 # Segundo código de error: archivo no encontrado
    '''

    if icao_code == '':
        return False, -1
    if not terminal.airlCodes:
        return False, 0
    return icao_code in terminal.airlCodes, 0

def SearchTerminal(bcn, name):
    for terminal in bcn.terminals:
        isThere, code = IsAirlineInTerminal(terminal, name)
        if code == -1:
            return -1 # Nombre de aerolínea inválido
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

if __name__ == "__main__":
    print("="*60)
    print("TEST VERSIÓN 3 - ESTRUCTURA Y GESTIÓN DEL AEROPUERTO")
    print("="*60)
    
    # ==========================================
    # 1. Test LoadAirportStructure
    # ==========================================
    print("\n📌 1. Probando LoadAirportStructure('LEBL.txt')")
    print("-" * 40)
    
    bcn = LoadAirportStructure("LEBL.txt")
    
    if isinstance(bcn, BarcelonaAP):
        print(f"✅ Aeropuerto {bcn.code} cargado correctamente")
        print(f"   Terminales: {len(bcn.terminals)}")
        for t in bcn.terminals:
            print(f"   - {t.name}: {len(t.boardingAreas)} áreas, {len(t.airlCodes)} aerolíneas cargadas")
            for a in t.boardingAreas:
                print(f"       Área {a.name} ({a.type}): {len(a.gates)} puertas")
    else:
        print(f"❌ Error al cargar aeropuerto. Código: {bcn}")
        exit()
    
    # ==========================================
    # 2. Test GateOccupancy (sin puertas ocupadas aún)
    # ==========================================
    print("\n📌 2. Probando GateOccupancy() (inicialmente todas libres)")
    print("-" * 40)
    
    gates = GateOccupancy(bcn)
    free_gates = [g for g in gates if not g.occupied]
    occupied_gates = [g for g in gates if g.occupied]
    
    print(f"✅ Total puertas: {len(gates)}")
    print(f"   Libres: {len(free_gates)}")
    print(f"   Ocupadas: {len(occupied_gates)}")
    if free_gates:
        print(f"   Ejemplo de puerta libre: {free_gates[0].name}")
    
    # ==========================================
    # 3. Test AssignGate con algunos vuelos
    # ==========================================
    print("\n📌 3. Probando AssignGate() con vuelos reales")
    print("-" * 40)

    # Cargar llegadas desde arrivals.txt
    from aircraft import LoadArrivals
    flights = LoadArrivals("Arrivals.txt")
    
    if not flights:
        print("❌ No se pudieron cargar vuelos. Asegúrate de que 'arrivals.txt' existe.")
    else:
        assigned = 0
        errors = []
        for i, flight in enumerate(flights[:10]):  # Probamos solo primeros 10
            result = AssignGate(bcn, flight)
            if result == 0:
                assigned += 1
                # Buscar la puerta asignada para mostrar información
                for gate in GateOccupancy(bcn):
                    if gate.occupied and gate.id == flight.id:
                        print(f"   ✅ Vuelo {flight.id} ({flight.company}) → puerta {gate.name}")
                        break
            else:
                errors.append((flight.id, result))
        
        print(f"\n   Asignaciones exitosas: {assigned} de {min(10, len(flights))}")
        if errors:
            print("   Errores:")
            for fid, code in errors:
                print(f"      - Vuelo {fid}: código {code}")
    
    # ==========================================
    # 4. Test GateOccupancy después de asignaciones
    # ==========================================
    print("\n📌 4. Verificando ocupación después de asignaciones")
    print("-" * 40)
    
    gates = GateOccupancy(bcn)
    free_gates = [g for g in gates if not g.occupied]
    occupied_gates = [g for g in gates if g.occupied]
    
    print(f"   Puertas libres: {len(free_gates)}")
    print(f"   Puertas ocupadas: {len(occupied_gates)}")
    
    # Mostrar ocupación por terminal y área (en texto)
    print("\n   Resumen de ocupación por área:")
    for terminal in bcn.terminals:
        print(f"   Terminal {terminal.name}:")
        for area in terminal.boardingAreas:
            occupied_in_area = sum(1 for g in area.gates if g.occupied)
            total_in_area = len(area.gates)
            print(f"       Área {area.name} ({area.type}): {occupied_in_area}/{total_in_area} ocupadas")
    
    # ==========================================
    # 5. Test funciones auxiliares (internas)
    # ==========================================
    print("\n📌 5. Probando funciones auxiliares internas")
    print("-" * 40)
    
    # Probar SetGates directamente
    test_area = BoardingArea(name="Test", tp="Schengen")
    ret = SetGates(test_area, 1, 5, "TEST")
    print(f"   SetGates(1,5,'TEST'): código {ret} → {len(test_area.gates)} puertas")
    
    # Probar LoadAirlines en una terminal existente
    if bcn.terminals:
        terminal_test = bcn.terminals[0]
        # Guardar copia de airlCodes antes
        old_codes = terminal_test.airlCodes.copy()
        ret = LoadAirlines(terminal_test, terminal_test.name)
        print(f"   LoadAirlines({terminal_test.name}): código {ret} → {len(terminal_test.airlCodes)} aerolíneas cargadas")
        # Restaurar si no queremos modificar la estructura real (opcional)
        # terminal_test.airlCodes = old_codes
    
    # Probar IsAirlineInTerminal y SearchTerminal con código ICAO
    if bcn.terminals and terminal_test.airlCodes:
        # Tomamos el primer código ICAO de la lista de la terminal (ejemplo: 'ADR', 'AEE', etc.)
        ejemplo_code = terminal_test.airlCodes[0]  # Esto es un código ICAO, no un nombre
        print(f"   Probando con código ICAO: '{ejemplo_code}'")

        # Comprobar si ese código está en la terminal (debería ser True)
        found, code = IsAirlineInTerminal(terminal_test, ejemplo_code)
        print(f"   IsAirlineInTerminal('{ejemplo_code}'): {found}, código {code}")

        # Buscar en qué terminal está ese código (debería ser la terminal actual)
        term_name = SearchTerminal(bcn, ejemplo_code)
        print(f"   SearchTerminal('{ejemplo_code}'): '{term_name}'")
    
    # Probar con código que no existe
    codigo_falso = "XYZ"
    found2, code2 = IsAirlineInTerminal(terminal_test, codigo_falso)
    print(f"   IsAirlineInTerminal('{codigo_falso}'): {found2}, código {code2}")
    term_name2 = SearchTerminal(bcn, codigo_falso)
    print(f"   SearchTerminal('{codigo_falso}'): '{term_name2}'")  # Debería ser cadena vacía

    # ==========================================
    # RESULTADO FINAL
    # ==========================================
    print("\n" + "="*60)
    print("🎉 TEST VERSIÓN 3 COMPLETADO")
    print("="*60)
    print("\n✅ Si no has visto errores, todas las funciones funcionan correctamente.")
    print("✅ La estructura del aeropuerto se ha construido y se han asignado puertas.")
    print("✅ La ocupación se puede consultar mediante GateOccupancy().")
    print("   (El gráfico visual es una mejora opcional para versión final)")