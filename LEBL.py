from airport import *
from aircraft import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy

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

def vuelos_menos_dos_horas(aircrafts):
    if not aircrafts:
        return -1
    
    count = 0

    for airc in aircrafts:
        if airc.land_time != "" and airc.departure_time != "":
            llegada = time_to_minutes(airc.land_time) # La hora de llegada en minutos
            salida = time_to_minutes(airc.departure_time) # La hora de salida en minutos
            tiempo_estacionado = salida - llegada # Diferencia en minutos entre la salida y la llegada
            tiempo_limite = 120  # 120 minutos son 2 horas
            if tiempo_estacionado < tiempo_limite:
                count += 1
    
    return count

def SetGates(area, init_gate, end_gate, prefix):
    """
    Crea las puertas de un área de embarque con nombres "prefijo + G + número".
    Reinicia la lista si ya existía. Devuelve 0 si éxito, -1 si error de conversión, -2 si end_gate < init_gate.
    """
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
    """
    Carga los códigos ICAO de las aerolíneas asignadas a una terminal desde 't_name_Airlines.txt'.
    Actualiza terminal.airlCodes. Devuelve 0 si éxito, -1 si archivo no encontrado.
    """
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
    """
    Construye toda la estructura del aeropuerto (terminales, áreas, puertas, asignación de aerolíneas) desde un archivo.
    Devuelve un objeto BarcelonaAP o un código de error negativo.
    """
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
                            
                            full_name = t_name + 'BA' + name.lower()
                            area = BoardingArea(name=full_name, tp=type_area)
                            prefix = full_name
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

def GateOccupancy(bcn):
    """
    Recorre el aeropuerto y devuelve una lista de diccionarios con información de cada puerta:
    terminal, área, nombre, ocupación y avión (si ocupado).
    """

    gates = []

    for terminal in bcn.terminals:

        for area in terminal.boardingAreas:

            for gate in area.gates:

                gate_info = {
                    "terminal": terminal.name,
                    "area": area.name,
                    "gate": gate.name,
                    "occupied": gate.occupied,
                    "aircraft": gate.id
                }

                gates.append(gate_info)

    return gates

def IsAirlineInTerminal(terminal, icao_code):
    """
    Indica si una aerolínea (por su código ICAO) está asignada a esta terminal.
    Devuelve una tupla (bool, código_error): 0 = éxito, -1 = código vacío, -2 = archivo no encontrado (no usado actualmente).
    """

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
    """
    Busca en qué terminal está asignada una aerolínea (por código ICAO).
    Devuelve el nombre de la terminal, -1 si error, o cadena vacía si no se encuentra.
    """
    for terminal in bcn.terminals:
        isThere, code = IsAirlineInTerminal(terminal, name)
        if code == -1:
            return -1 # Nombre de aerolínea inválido
        if isThere:
            return terminal.name
    return ""

def AssignGate(bcn, aircraft):
    """
    Asigna una puerta libre a un vuelo según su compañía (busca terminal) y si el vuelo es Schengen.
    Devuelve 0 si éxito, -1 (aerolínea inválida), -2 (error lectura), -3 (aerolínea no registrada), -4 (sin puerta libre).
    """
    terminal_name = SearchTerminal(bcn, aircraft.company)

    if terminal_name == -1:
        return -1 # Error, nombre de aerolínea inválido
    if terminal_name == -2:
        return -2 # Error de lectura de los datos
    if terminal_name == "":
        return -3 # Aerolínea no registrada

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
    return -4 # No hay puerta disponible

def AssignNightGates(bcn, aircrafts):
    """
    Asigna puerta a los aviones nocturnos (solo salida, sin llegada).
    Primero libera TODAS las puertas del aeropuerto (simula el inicio del día).
    Luego asigna puerta a cada avión nocturno.
    Devuelve un diccionario con los IDs de aviones que no pudieron asignarse
    y el código de error correspondiente.
    """
    if not aircrafts:
        return {}, -1   # Error: lista vacía

    # Liberar todas las puertas del aeropuerto (reseteo completo)
    for terminal in bcn.terminals:
        for area in terminal.boardingAreas:
            for gate in area.gates:
                gate.occupied = False
                gate.id = ""

    # Asignar puertas a los nocturnos (solo los que cumplen condición)
    problem_airc = {}
    for airc in aircrafts:
        # Solo aviones sin llegada y con salida
        if airc.land_time == "" and airc.departure_time != "":
            cd = AssignGate(bcn, airc)
            if cd != 0:
                problem_airc[airc.id] = cd
    return problem_airc, 0

def FreeGate (bcn, id):
    for terminal in bcn.terminals:
        for area in terminal.boardingAreas:
            for gate in area.gates:
                if gate.id == id:
                    gate.occupied = False
                    return 0 #Todo ha ido bien

    else:
        return -1 # No se ha encontrado ningun gate con ese avion

def AssignGatesAtTime(bcn, aircrafts, time):
    """
    Asigna puertas a los vuelos que aterrizan durante la hora que empieza en 'time'
    (formato 'hh:mm'). Antes de asignar, libera las puertas de aviones que han
    despegado antes del inicio de esa hora.
    Devuelve el número de aviones que aterrizan en ese período pero quedan sin
    puerta (por ocupación total).
    """
    t_min = time_to_minutes(time)
    t_end_min = t_min + 60

    # Diccionario para búsqueda rápida de avión por id
    aircraft_dict = {a.id: a for a in aircrafts}

    # Liberar las puertas de aviones que ya han despegado antes del inicio del período
    for terminal in bcn.terminals:
        for area in terminal.boardingAreas:
            for gate in area.gates:
                if gate.occupied and gate.id:
                    a = aircraft_dict.get(gate.id)
                    if a and a.departure_time:
                        dep_min = time_to_minutes(a.departure_time)
                        if dep_min < t_min:
                            gate.occupied = False
                            gate.id = ''

    # Asignar puertas a los vuelos que aterrizan durante el período
    # Filtrar y ordenar por hora de llegada
    landing_this_hour = [
        a for a in aircrafts
        if a.land_time and t_min <= time_to_minutes(a.land_time) < t_end_min
    ]
    landing_this_hour.sort(key=lambda a: time_to_minutes(a.land_time))

    not_assigned = 0
    for a in landing_this_hour:
        if AssignGate(bcn, a) != 0:
            not_assigned += 1
    return not_assigned

def PlotDayOccupancy(bcn, aircrafts):
    """
    Genera un gráfico con la ocupación de puertas por terminal y el número de
    aviones no asignados, para cada período de una hora del día (0 a 23).
    El estado inicial de bcn es el de inicio del día (solo aviones nocturnos).
    Devuelve la figura de matplotlib.
    """
    hours = list(range(24))
    # Estructuras de datos: por terminal y por hora
    terminal_names = [t.name for t in bcn.terminals]
    occupancy = {tname: [0]*24 for tname in terminal_names}
    not_assigned_per_hour = [0]*24

    # Copia del aeropuerto (para no modificar el original)
    bcn_copy = copy.deepcopy(bcn)

    # Para cada período horario, ejecutar AssignGatesAtTime y medir ocupación
    for h in range(24):
        time_str = f"{h:02d}:00"
        # Primero, asignar puertas en este período (libera y asigna)
        na = AssignGatesAtTime(bcn_copy, aircrafts, time_str)
        not_assigned_per_hour[h] = na
        # Registrar ocupación por terminal después de la asignación
        for terminal in bcn_copy.terminals:
            occ = 0
            for area in terminal.boardingAreas:
                for gate in area.gates:
                    if gate.occupied:
                        occ += 1
            occupancy[terminal.name][h] = occ

    # Dibujar gráfico
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Gráfico 1: ocupación por terminal
    for tname in terminal_names:
        ax1.plot(hours, occupancy[tname], marker='o', label=f"Terminal {tname}")
    
    ax1.set_xlabel("Hour of day")
    ax1.set_ylabel("Number of occupied gates")
    ax1.set_title("Gate occupancy per terminal")
    ax1.legend()
    ax1.grid(True)

    # Gráfico 2: aviones no asignados
    ax2.bar(hours, not_assigned_per_hour, color='salmon')
    ax2.set_xlabel("Hour of day")
    ax2.set_ylabel("Aircraft not assigned")
    ax2.set_title("Unassigned arrivals per hour")
    ax2.grid(axis='y')
    plt.tight_layout()

    return fig

def PlotTerminalOccupancy(gates, terminal_name):
    """
    Dibuja un esquema de una terminal: áreas y puertas, con cuadrados de color verde (libre) o rojo (ocupado).
    Recibe la lista de ocupación (GateOccupancy) y el nombre de la terminal. Devuelve la figura de matplotlib.
    """

    """
    Dibuja gráficamente la ocupación de UNA terminal.

    Parámetros
    ----------
    gates : list
        Lista devuelta por GateOccupancy()

    terminal_name : str
        Nombre de la terminal a dibujar
    """

    # =====================================================
    # FILTRAR GATES DE LA TERMINAL
    # =====================================================

    terminal_gates = []

    for gate in gates:

        if gate["terminal"] == terminal_name:
            terminal_gates.append(gate)

    # Si no hay gates
    if not terminal_gates:
        return None

    # =====================================================
    # AGRUPAR GATES POR ÁREA
    # =====================================================

    areas = {}

    for gate in terminal_gates:

        area_name = gate["area"]

        if area_name not in areas:
            areas[area_name] = []

        areas[area_name].append(gate)

    # =====================================================
    # ORDENAR GATES NUMÉRICAMENTE
    # =====================================================

    for area_name in areas:

        areas[area_name].sort(
            key=lambda g: int(
                ''.join(filter(str.isdigit, g["gate"]))
            )
        )

    # =====================================================
    # CREAR FIGURA
    # =====================================================

    max_gates = max(len(g) for g in areas.values())

    figure_height = max(8, max_gates * 0.45)

    fig, ax = plt.subplots(
        figsize=(18, figure_height)
    )

    ax.axis('off')

    ax.set_title(
        f"Terminal {terminal_name} - Gate Occupancy",
        fontsize=20,
        fontweight='bold',
        pad=25
    )

    # =====================================================
    # PARÁMETROS VISUALES
    # =====================================================

    horizontal_y = 0

    area_spacing = 14

    gate_spacing = 1.8

    vertical_start_y = -2

    gate_length = 3

    terminal_color = '#0B5A7A'

    # =====================================================
    # LONGITUD TERMINAL
    # =====================================================

    area_names = list(areas.keys())

    num_areas = len(area_names)

    terminal_length = area_spacing * (num_areas - 1)

    # =====================================================
    # DIBUJAR TERMINAL
    # =====================================================

    ax.plot(
        [0, terminal_length],
        [horizontal_y, horizontal_y],
        linewidth=25,
        color=terminal_color
    )

    # Nombre terminal
    ax.text(
        -5,
        horizontal_y,
        terminal_name,
        fontsize=22,
        fontweight='bold',
        va='center'
    )

    # =====================================================
    # DIBUJAR ÁREAS
    # =====================================================

    for area_index, area_name in enumerate(area_names):

        gates_area = areas[area_name]

        num_gates = len(gates_area)

        x_area = area_index * area_spacing

        vertical_length = gate_spacing * num_gates

        # -------------------------------------------------
        # Línea vertical área
        # -------------------------------------------------

        ax.plot(
            [x_area, x_area],
            [
                vertical_start_y,
                vertical_start_y - vertical_length
            ],
            linewidth=25,
            color=terminal_color
        )

        # -------------------------------------------------
        # Nombre área
        # -------------------------------------------------

        ax.text(
            x_area,
            vertical_start_y - vertical_length - 3,
            area_name,
            fontsize=20,
            fontweight='bold',
            ha='center'
        )

        # =================================================
        # DIBUJAR GATES
        # =================================================

        current_y = vertical_start_y - gate_spacing

        for gate_index, gate in enumerate(gates_area):

            # -------------------------------------------------
            # Zigzag izquierda/derecha
            # -------------------------------------------------

            if gate_index % 2 == 0:
                direction = 1
            else:
                direction = -1

            x_end = x_area + direction * gate_length

            # -------------------------------------------------
            # Línea gate
            # -------------------------------------------------

            ax.plot(
                [x_area, x_end],
                [current_y, current_y],
                linewidth=6,
                color=terminal_color
            )

            # -------------------------------------------------
            # Color ocupación
            # -------------------------------------------------

            if gate["occupied"]:
                square_color = 'red'
            else:
                square_color = 'limegreen'

            # -------------------------------------------------
            # Cuadrado
            # -------------------------------------------------

            square_size = 0.9

            rect = patches.Rectangle(
                (
                    x_end - square_size / 2,
                    current_y - square_size / 2
                ),
                square_size,
                square_size,
                facecolor=square_color,
                edgecolor='black'
            )

            ax.add_patch(rect)

            # -------------------------------------------------
            # Posición texto
            # -------------------------------------------------

            if direction == 1:

                text_x = x_end + 1.3
                align = 'left'

            else:

                text_x = x_end - 1.3
                align = 'right'

            # -------------------------------------------------
            # Nombre gate
            # -------------------------------------------------

            ax.text(
                text_x,
                current_y + 0.15,
                gate["gate"],
                fontsize=9,
                ha=align,
                va='bottom'
            )

            # -------------------------------------------------
            # ID avión
            # -------------------------------------------------

            if gate["occupied"]:

                ax.text(
                    text_x,
                    current_y - 0.5,
                    gate["aircraft"],
                    fontsize=7,
                    color='darkred',
                    ha=align,
                    va='top'
                )

            # siguiente gate
            current_y -= gate_spacing

    # =====================================================
    # LEYENDA
    # =====================================================

    green_patch = patches.Patch(
        color='limegreen',
        label='Free'
    )

    red_patch = patches.Patch(
        color='red',
        label='Occupied'
    )

    ax.legend(
        handles=[green_patch, red_patch],
        loc='upper right'
    )

    # =====================================================
    # AJUSTAR LIMITES
    # =====================================================

    ax.set_xlim(
        -8,
        terminal_length + 8
    )

    ax.set_ylim(
        -max_gates * gate_spacing - 10,
        5
    )

    # Parámetros rect=[left, bottom, right, top]
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    return fig

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
    # 2. Test GateOccupancy (versión diccionario)
    # ==========================================
    print("\n📌 2. Probando GateOccupancy() (inicialmente todas libres)")
    print("-" * 40)
    
    gates_info = GateOccupancy(bcn)   # lista de diccionarios
    free_gates = [g for g in gates_info if not g["occupied"]]
    occupied_gates = [g for g in gates_info if g["occupied"]]
    
    print(f"✅ Total puertas: {len(gates_info)}")
    print(f"   Libres: {len(free_gates)}")
    print(f"   Ocupadas: {len(occupied_gates)}")
    if free_gates:
        print(f"   Ejemplo de puerta libre: {free_gates[0]['gate']} (terminal {free_gates[0]['terminal']}, área {free_gates[0]['area']})")
    
    # ==========================================
    # 3. Test AssignGate con algunos vuelos
    # ==========================================
    print("\n📌 3. Probando AssignGate() con vuelos reales")
    print("-" * 40)

    from aircraft import LoadArrivals
    flights = LoadArrivals("Arrivals.txt")
    
    if not flights:
        print("❌ No se pudieron cargar vuelos. Asegúrate de que 'arrivals.txt' existe.")
    else:
        assigned = 0
        errors = []
        for i, flight in enumerate(flights[:10]):   # probamos primeros 10
            result = AssignGate(bcn, flight)
            if result == 0:
                assigned += 1
                # Buscar la puerta asignada (en la nueva estructura)
                for ginfo in GateOccupancy(bcn):
                    if ginfo["occupied"] and ginfo["aircraft"] == flight.id:
                        print(f"   ✅ Vuelo {flight.id} ({flight.company}) → puerta {ginfo['gate']} (terminal {ginfo['terminal']}, área {ginfo['area']})")
                        break
            else:
                errors.append((flight.id, result))
        
        print(f"\n   Asignaciones exitosas: {assigned} de {min(10, len(flights))}")
        if errors:
            print("   Errores:")
            for fid, code in errors:
                print(f"      - Vuelo {fid}: código {code}")
    
    # ==========================================
    # 4. GateOccupancy después de asignaciones
    # ==========================================
    print("\n📌 4. Verificando ocupación después de asignaciones")
    print("-" * 40)
    
    gates_info = GateOccupancy(bcn)
    free_gates = [g for g in gates_info if not g["occupied"]]
    occupied_gates = [g for g in gates_info if g["occupied"]]
    
    print(f"   Puertas libres: {len(free_gates)}")
    print(f"   Puertas ocupadas: {len(occupied_gates)}")
    
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
    
    # SetGates
    test_area = BoardingArea(name="Test", tp="Schengen")
    ret = SetGates(test_area, 1, 5, "TEST")
    print(f"   SetGates(1,5,'TEST'): código {ret} → {len(test_area.gates)} puertas")
    
    # LoadAirlines
    if bcn.terminals:
        terminal_test = bcn.terminals[0]
        ret = LoadAirlines(terminal_test, terminal_test.name)
        print(f"   LoadAirlines({terminal_test.name}): código {ret} → {len(terminal_test.airlCodes)} aerolíneas cargadas")
    
    # IsAirlineInTerminal y SearchTerminal con código ICAO
    if bcn.terminals and terminal_test.airlCodes:
        ejemplo_code = terminal_test.airlCodes[0]
        print(f"   Probando con código ICAO: '{ejemplo_code}'")
        found, code = IsAirlineInTerminal(terminal_test, ejemplo_code)
        print(f"   IsAirlineInTerminal('{ejemplo_code}'): {found}, código {code}")
        term_name = SearchTerminal(bcn, ejemplo_code)
        print(f"   SearchTerminal('{ejemplo_code}'): '{term_name}'")
    
    # Código falso
    codigo_falso = "XYZ"
    found2, code2 = IsAirlineInTerminal(terminal_test, codigo_falso)
    print(f"   IsAirlineInTerminal('{codigo_falso}'): {found2}, código {code2}")
    term_name2 = SearchTerminal(bcn, codigo_falso)
    print(f"   SearchTerminal('{codigo_falso}'): '{term_name2}'")
    
    # ==========================================
    # 6. MOSTRAR GRÁFICOS DE OCUPACIÓN (PlotTerminalOccupancy)
    # ==========================================
    print("\n📌 6. Generando gráficos de ocupación de terminales")
    print("-" * 40)
    
    for terminal in bcn.terminals:
        print(f"   Generando gráfico para terminal {terminal.name}...")
        fig = PlotTerminalOccupancy(GateOccupancy(bcn), terminal.name)
        if fig is not None:
            plt.show()        # muestra cada gráfico (se pausa hasta cerrar)
        else:
            print(f"      No se pudo generar para terminal {terminal.name}")
    
    # ==========================================
    # NUEVOS TESTS VERSIÓN 4
    # ==========================================
    print("\n" + "="*60)
    print("TEST VERSIÓN 4 - NUEVAS FUNCIONES (ASIGNACIÓN DINÁMICA, OCUPACIÓN)")
    print("="*60)

    # Cargar llegadas y salidas
    from aircraft import LoadArrivals, LoadDepartures, MergeMovements, NightAircraft
    flights = LoadArrivals("Arrivals.txt")
    departures, _ = LoadDepartures("Departures.txt")
    # Fusionar movimientos para tener lista completa
    if flights and departures:
        merged, _, _ = MergeMovements(flights, departures)
        all_aircrafts = merged
    elif flights:
        all_aircrafts = flights
    else:
        all_aircrafts = []

    # 1. Test AssignNightGates
    print("\n📌 1. Probando AssignNightGates()")
    # Primero necesitamos algunos aviones nocturnos. Los extraemos de la lista fusionada (solo salida)
    night_aircrafts, _ = NightAircraft(all_aircrafts) if all_aircrafts else ([], -1)
    if night_aircrafts:
        problem_dict, code_ng = AssignNightGates(bcn, night_aircrafts)
        if code_ng == 0:
            print(f"   ✅ Puertas asignadas a {len(night_aircrafts) - len(problem_dict)}/{len(night_aircrafts)} aviones nocturnos")
            if problem_dict:
                print(f"   ⚠️ Problemas con aviones: {problem_dict}")
        else:
            print("   ❌ Error en AssignNightGates")
    else:
        print("   ⚠️ No hay aviones nocturnos para probar AssignNightGates (se necesitan solo salidas).")

    # 2. Test FreeGate
    print("\n📌 2. Probando FreeGate()")
    # Buscar algún gate ocupado (por ejemplo, después de AssignNightGates)
    occupied_gate_found = False
    for terminal in bcn.terminals:
        for area in terminal.boardingAreas:
            for gate in area.gates:
                if gate.occupied:
                    aircraft_id = gate.id
                    result = FreeGate(bcn, aircraft_id)
                    if result == 0:
                        print(f"   ✅ Gate {gate.name} liberado del avión {aircraft_id}")
                        occupied_gate_found = True
                        break
                if occupied_gate_found:
                    break
            if occupied_gate_found:
                break
        if occupied_gate_found:
            break
    if not occupied_gate_found:
        print("   ⚠️ No hay puertas ocupadas para probar FreeGate.")

    # 3. Test AssignGatesAtTime
    print("\n📌 3. Probando AssignGatesAtTime()")
    if all_aircrafts:
        # Elegir una hora, por ejemplo las 6:00
        test_hour = "06:00"
        not_assigned = AssignGatesAtTime(bcn, all_aircrafts, test_hour)
        print(f"   ✅ Para el período que empieza a las {test_hour}, aviones no asignados: {not_assigned}")
    else:
        print("   ⚠️ No hay lista de aeronaves para probar AssignGatesAtTime.")

    # 4. Test PlotDayOccupancy
    print("\n📌 4. Probando PlotDayOccupancy()")
    if all_aircrafts:
        fig = PlotDayOccupancy(bcn, all_aircrafts)
        if fig:
            print("   ✅ Gráfico de ocupación diaria generado. Se mostrará en 3 segundos.")
            plt.ion()
            plt.show(block=False)
            plt.pause(3)
            plt.close()
    else:
        print("   ⚠️ No hay suficientes datos para PlotDayOccupancy.")

    # Resumen final
    print("\n" + "="*60)
    print("🎉 TEST VERSIÓN 4 COMPLETADO")
    print("="*60)
    print("\n✅ Si no has visto errores, las nuevas funciones funcionan correctamente.")

    # ==========================================
    # RESULTADO FINAL
    # ==========================================
    print("\n" + "="*60)
    print("🎉 TEST VERSIÓN 3 + EXTENSIÓN DE LA VERSIÓN 4 COMPLETADO")
    print("="*60)
    print("\n✅ Todas las funciones se han probado correctamente.")
    print("✅ Se han generado gráficos de ocupación para cada terminal.")
    print("✅ La estructura del aeropuerto se ha construido y se han asignado puertas.")