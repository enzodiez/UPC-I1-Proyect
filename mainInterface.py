import customtkinter as ctk
from tkinter import messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from airport import *
from aircraft import *
from LEBL import *

# Configuración de apariencia
ctk.set_appearance_mode("dark")  # Modos: "system" (standard), "dark", "light"
ctk.set_default_color_theme("blue")  # Temas: "blue" (standard), "green", "dark-blue"

class SplashScreen(ctk.CTkToplevel):
    def __init__(self):
        # Forzar modo oscuro para la splash (luego la interfaz principal lo seguirá)
        ctk.set_appearance_mode("dark")
        super().__init__()
        self.title("")
        self.geometry("600x400")
        self.overrideredirect(True)   # Sin bordes para un look moderno
        self.resizable(False, False)
        
        # Fondo oscuro elegante
        self.configure(fg_color=("#1e1e1e", "#f0f0f0"))
        
        # Centrar ventana de forma nativa en CustomTkinter
        self.update_idletasks()
        self.tk.eval(f'tk::PlaceWindow {self._w} center')
        
        # Marco principal para centrar contenido
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Título principal
        self.label_title = ctk.CTkLabel(
            main_frame, text="I1-Proyect", font=("Arial", 48, "bold"),
            text_color=("#ffffff", "#000000")
        )
        self.label_title.pack(pady=20)
        
        # Subtítulo
        self.label_sub = ctk.CTkLabel(
            main_frame, text="Airport Management System", font=("Arial", 16),
            text_color=("#cccccc", "#333333")
        )
        self.label_sub.pack(pady=5)
        
        # Barra de progreso estilizada
        self.progress = ctk.CTkProgressBar(
            main_frame, width=500, height=12, corner_radius=6,
            progress_color="#1f8d4a",  # Verde atractivo
            fg_color="#444444"
        )
        self.progress.pack(pady=50)
        self.progress.set(0)
        
        # Mensaje dinámico
        self.message = ctk.CTkLabel(
            main_frame, text="Iniciando...", font=("Arial", 12),
            text_color=("#aaaaaa", "#555555")
        )
        self.message.pack(pady=10)
        
        # Secuencia de carga
        self.stages = [
            (0.1, "Cargando módulos..."),
            (0.3, "Conectando con bases de datos..."),
            (0.5, "Cargando estructura del aeropuerto..."),
            (0.7, "Preparando interfaz..."),
            (0.9, "¡Casi listo!"),
        ]
        self.stage_index = 0
        self.start_loading()
    
    def start_loading(self):
        if self.stage_index < len(self.stages):
            progress, msg = self.stages[self.stage_index]
            self.progress.set(progress)
            self.message.configure(text=msg)
            self.stage_index += 1
            self.after(800, self.start_loading)
        else:
            self.progress.set(1.0)
            self.message.configure(text="¿Estás listo para sumergirte en el mundo de la gestión aeroportuaria?")
            self.show_start_button()
    
    def show_start_button(self):
        self.start_button = ctk.CTkButton(
            self, text="¡Empezar!", command=self.destroy,
            width=200, height=45, corner_radius=10,
            font=("Arial", 14, "bold"), fg_color="#1f8d4a", hover_color="#166b39"
        )
        self.start_button.place(relx=0.5, y=340, anchor="center")

class InterfazPrincipal(ctk.CTk):
    # Configura la ventana principal, los frames, botones y variables iniciales.
    def __init__(self):
        # Crear la ventana principal (aún no visible)
        super().__init__()
        
        # Ocultarla temporalmente
        self.withdraw()
        
        # Mostrar splash screen
        splash = SplashScreen()
        self.wait_window(splash)   # Espera a que se cierre la splash
        
        self.after(0, lambda: self.state('zoomed'))
        self.title("I1-Proyect")

        # Matriz de la interfaz
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=1)

        # En la columna izquierda se configurar los botones de las opciones
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)

        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(0, weight=1)
        self.options_frame.grid_rowconfigure(1, weight=1)
        self.options_frame.grid_rowconfigure(2, weight=1)
        self.options_frame.grid_rowconfigure(3, weight=1)
        self.options_frame.grid_rowconfigure(4, weight=1)
        self.options_frame.grid_rowconfigure(5, weight=1)
        self.options_frame.grid_rowconfigure(6, weight=1)
        self.options_frame.grid_rowconfigure(7, weight=1)

        self.registros = ctk.CTkButton(self.options_frame, text="Registros", corner_radius=5, border_width=2, command=self.ejecutar_registros)
        self.registros.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)

        self.visz_data = ctk.CTkButton(self.options_frame, text="Información técnica", corner_radius=5, border_width=2, command=self.ejecutar_info_tecn)
        self.visz_data.grid(row=1, column=0, sticky='nsew', padx=15, pady=15)

        self.graphs = ctk.CTkButton(self.options_frame, text="Gráficos", corner_radius=5, border_width=2, command=self.ejecutar_graficos)
        self.graphs.grid(row=2, column=0, sticky='nsew', padx=15, pady=15)

        self.maps = ctk.CTkButton(self.options_frame, text="Mapas con Google Earth", corner_radius=5, border_width=2, command=self.ejecutar_google_earth)
        self.maps.grid(row=3, column=0, sticky='nsew', padx=15, pady=15)

        self.cargar_bcn = ctk.CTkButton(self.options_frame, text="Cargar estructura del aeropuerto de Barcelona", corner_radius=5, border_width=2, command=self.cargar_estructura_bcn)
        self.cargar_bcn.grid(row=4, column=0, sticky='nsew', padx=15, pady=15)

        self.btn_cargar_llegadas = ctk.CTkButton(self.options_frame, text="Cargar llegadas al aeropuerto de Barcelona", corner_radius=5, border_width=2, command=self.cargar_llegadas)
        self.btn_cargar_llegadas.grid(row=5, column=0, sticky='nsew', padx=15, pady=15)

        self.btn_cargar_salidas = ctk.CTkButton(self.options_frame, text="Cargar salidas del aeropuerto de Barcelona", corner_radius=5, border_width=2, command=self.cargar_salidas)
        self.btn_cargar_salidas.grid(row=6, column=0, sticky='nsew', padx=15, pady=15)

        self.switch_appear = ctk.StringVar(value="on")
        self.appearance = ctk.CTkSwitch(self.options_frame, text='Modo Oscuro', onvalue='on', offvalue='off', variable=self.switch_appear, command=self.cambiar_modo_toggle)
        self.appearance.grid(row=7, column=0, sticky='nsew', padx=15, pady=15)

        self.principal_frame = ctk.CTkFrame(self)
        self.principal_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.bcn = None
        self.all_flights = []
        self.arrivals = []
        self.departures = []

        # Sirve para poder cerrar bien la interfaz
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Finalmente, mostrar la ventana
        self.deiconify()
    
    # Este método me lo ha explicado la IA DeepSeek
    # Sirve para poder cerrar bien todos los gráficos y evitar que aparezcan errores en la terminal si se cierra la aplicación con gráficos abiertos.
    # Cierra todas las figuras de matplotlib y destruye la ventana principal.
    def on_closing(self):
        # Cerrar todas las figuras de matplotlib
        plt.close('all')
        # Destruir la ventana principal
        self.quit()
        self.destroy()

    # Cambia el modo claro/oscuro de customtkinter y actualiza el tema de matplotlib.
    def cambiar_modo_toggle(self):
        if self.switch_appear.get() == "on":
            ctk.set_appearance_mode("dark")
            self.appearance.configure(text="Modo Oscuro")
        else:
            ctk.set_appearance_mode("light")
            self.appearance.configure(text="Modo Claro")
        
        self.configurar_tema_matplotlib()
    
    # Ajusta los colores de matplotlib según el modo actual (claro u oscuro).
    def configurar_tema_matplotlib(self):
        modo = ctk.get_appearance_mode()
        if modo == "Dark":
            plt.rcParams.update({
                'figure.facecolor': '#2b2b2b',
                'axes.facecolor': '#2b2b2b',
                'text.color': 'white',
                'axes.labelcolor': 'white',
                'xtick.color': 'white',
                'ytick.color': 'white'
            })
        else:   # "Light"
            plt.rcParams.update({
                'figure.facecolor': 'white',
                'axes.facecolor': 'white',
                'text.color': 'black',
                'axes.labelcolor': 'black',
                'xtick.color': 'black',
                'ytick.color': 'black'
            })
    
    # Carga la estructura del aeropuerto desde LEBL.txt; si ya existe, pide confirmación.
    def cargar_estructura_bcn(self):
        # Si ya hay una estructura cargada, pregunto al usuario
        if self.bcn is not None:
            respuesta = messagebox.askyesno(
                "Confirmar recarga",
                "Ya hay una estructura del aeropuerto cargada.\n"
                "Recargar borrará las asignaciones actuales de puertas.\n"
                "¿Deseas continuar?"
            )
            if not respuesta:
                return
        
        nuevo_bcn = LoadAirportStructure("LEBL.txt")
        
        if isinstance(nuevo_bcn, int):
            if nuevo_bcn == -1:
                aviso = 'No se encontró la información del aeropuerto.'
            elif nuevo_bcn == -2:
                aviso = 'No hay información sobre el aeropuerto.'
            elif nuevo_bcn == -3:
                aviso = 'Información sobre el aeropuerto insuficiente.'
            elif nuevo_bcn == -4:
                aviso = 'Error al cargar las aerolíneas asociadas.'
            elif nuevo_bcn == -5:
                aviso = 'Archivo corrupto/formato no válido.'
            elif nuevo_bcn == -6:
                aviso = 'Fallo en la lectura de los datos, información incompatible con la estructura del aeropuerto.'
            elif nuevo_bcn == -7:
                aviso = 'Índices de las puertas de embarque inválidos.'
            elif nuevo_bcn == -8:
                aviso = 'Índices de las puertas de embarque ilógicos.'
            messagebox.showerror('Error', aviso)
        else:
            self.bcn = nuevo_bcn
            messagebox.showinfo('Éxito', 'La estructura del aeropuerto se ha cargado exitosamente!')
    
    # Permite seleccionar un archivo de llegadas y añade sus vuelos a la lista self.arrivals.
    def cargar_llegadas(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de llegadas",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            nuevos_arrivals = LoadArrivals(filename)
            if nuevos_arrivals:
                self.arrivals.extend(nuevos_arrivals)
                messagebox.showinfo("Éxito", f"Se añadieron {len(nuevos_arrivals)} vuelos.\nTotal: {len(self.arrivals)}")
            else:
                messagebox.showerror("Error", "El archivo no contiene datos válidos.")
    
    # Permite seleccionar un archivo de salidas y añade sus vuelos a la lista self.departures.
    def cargar_salidas(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo de salidas",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            nuevos_departures, code = LoadDepartures(filename)
            if code == 0 and nuevos_departures:
                self.departures.extend(nuevos_departures)
                messagebox.showinfo("Éxito", f"Se añadieron {len(nuevos_departures)} vuelos.\nTotal: {len(self.departures)}")
            elif code == -1:
                messagebox.showerror("Error", "No se encontró el archivo de salidas.")
            else:
                messagebox.showerror("Error", "El archivo no contiene datos válidos.")
    
    # Muestra el submenú de registros (gestión de aeropuertos, guardado de vuelos, asignación de puertas, etc.).
    def ejecutar_registros(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        label = ctk.CTkLabel(self.principal_frame, text="¿Qué qué tipo de acción desea realizar?", font=("Arial", 20))
        label.pack(pady=20)
        
        # Creo un subframe para los botones
        btn_frame = ctk.CTkFrame(self.principal_frame, fg_color="transparent")
        btn_frame.pack(expand=True)

        # Creo botones para las múltiples opciones dentro del subframe
        btn_map_airp = ctk.CTkButton(btn_frame, text='Gestionar aeropuertos', command=self.ejecutar_gestionar_airp)
        btn_map_airp.pack(pady=20)

        btn_lebl_arrivals = ctk.CTkButton(btn_frame, text='Guardar llegadas hoy a LEBL', command=self.procesar_save_flights)
        btn_lebl_arrivals.pack(pady=20)

        btn_save_schengen = ctk.CTkButton(btn_frame, text='Guardar aeropuertos Schengen', command=self.procesar_guardar_schengen)
        btn_save_schengen.pack(pady=20)

        btn_assign_gates = ctk.CTkButton(btn_frame, text='Assignar puertas de embarque', command=self.procesar_asignar_puertas)
        btn_assign_gates.pack(pady=20)

        btn_clear_flights = ctk.CTkButton(btn_frame, text='Limpiar vuelos cargados', command=self.limpiar_vuelos)
        btn_clear_flights.pack(pady=20)

        btn_merge_movements = ctk.CTkButton(btn_frame, text='Fusionar llegadas y salidas cargadas', command=self.fusionar_movimientos)
        btn_merge_movements.pack(pady=20)

        btn_gates_time = ctk.CTkButton(btn_frame, text='Asignar puertas por período horario', command=self.ejecutar_asignar_gates_hora)
        btn_gates_time.pack(pady=20)

        btn_night_gates = ctk.CTkButton(btn_frame, text='Asignar puertas a aviones nocturnos', command=self.procesar_asignar_vuelos_noche)
        btn_night_gates.pack(pady=20)
    
    # Asigna las puertas de embarque a los aviones nocturnos, los que pasan la noche en el aeropuerto
    def procesar_asignar_vuelos_noche(self):
        if self.bcn is None or not isinstance(self.bcn, BarcelonaAP):
            messagebox.showerror("Error", "Primero debe cargar la estructura del aeropuerto")
            return
        
        if not self.all_flights:
            messagebox.showerror("Error", "Primero debe cargar los vuelos (botón 'Cargar llegadas' + botón 'Cargar salidas + botón 'Fusionar llegadas y salidas')")
            return
        
        night_aircrafts, cd = NightAircraft(self.all_flights)

        if cd == -1: # Muy raro porque ya se comprueba que all_flights no esté vacía. No debería suceder nunca
            messagebox.showerror('Error', 'No hay vuelos cargados')
            return
        elif cd == 0 and night_aircrafts == []: # Raro pero podría pasar
            messagebox.showwarning('Advertencia', 'No se ha encontrado ningún avión con las características requeridas.')
            return
        else:
            problem_airc, code = AssignNightGates(self.bcn, night_aircrafts)

            if code == -1: # No debería suceder nunca
                messagebox.showerror('Error', 'No hay vuelos nocturnos cargados')
                return
            else:
                msg = 'Asignación de puertas a los aviones nocturnos realizada.'
                if problem_airc:
                    problem_details = "\n".join([f"{aid}: código {code}" for aid, code in list(problem_airc.items())[:10]])
                    if len(problem_airc) > 10:
                        problem_details += f"\n... y {len(problem_airc)-10} más."
                    msg += f"\n\nAviones con problemas:\n{problem_details}"
                    messagebox.showwarning('Información con advertencia', msg)
                else:
                    messagebox.showinfo('Información', msg)
    
    # Recibe la hora del día en la cual realizar la asignación de las puertas de embarque
    def ejecutar_asignar_gates_hora(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        label = ctk.CTkLabel(self.principal_frame, text="Asignar puertas por período horario. Elige la hora.", font=("Arial", 20))
        label.pack(pady=20)
        
        # Creo un subframe para los botones
        btn_frame = ctk.CTkFrame(self.principal_frame, fg_color="transparent")
        btn_frame.pack(expand=True)

        # Creo una lista desplegable y un botón de confirmación
        opciones = ['---', '00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00',
                    '11:00', '12:00', '13:00','14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00',
                    '23:00']
        self.desplegable = ctk.CTkOptionMenu(master=btn_frame, values=opciones)
        self.desplegable.pack(pady=30)
        self.desplegable.set(opciones[0]) # Valor por defecto

        btn_map_airp = ctk.CTkButton(btn_frame, text='Confirmar hora', command=self.procesar_asignar_gates_hora)
        btn_map_airp.pack(pady=30)
    
    # Procesa la asignación de las puertas de embarque en una hora especificada del día
    def procesar_asignar_gates_hora(self):
        hora = self.desplegable.get()

        if hora != '---':
            if self.bcn is None or not isinstance(self.bcn, BarcelonaAP):
                messagebox.showerror("Error", "Primero debe cargar la estructura del aeropuerto")
                return
            
            if not self.all_flights:
                messagebox.showerror("Error", "Primero debe cargar los vuelos (botón 'Cargar llegadas' + botón 'Cargar salidas + botón 'Fusionar llegadas y salidas')")
                return

            messagebox.showinfo('Confirmación', f'Ha selecionado el período horario: {hora}.')
            not_assigned = AssignGatesAtTime(self.bcn, self.all_flights, hora)
            msg = 'Asignación realizada!'
            if not_assigned != 0:
                msg += f'\n\nNúmero de aviónes que no han podido ser asignados: {not_assigned}'
                messagebox.showwarning('Información con advertencia', msg)
            else:
                messagebox.showinfo('Información', msg)
            
            self.ejecutar_registros()
        else:
            messagebox.showwarning('Advertencia', 'Debe seleccionar un período horario.')
    
    # Muestra el submenú de mapas de Google Earth (aeropuertos, todos los vuelos, larga distancia).
    def ejecutar_google_earth(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        label = ctk.CTkLabel(self.principal_frame, text="Mapas con Google Earth", font=("Arial", 20))
        label.pack(pady=20)
        
        # Creo un subframe para los botones
        btn_frame = ctk.CTkFrame(self.principal_frame, fg_color="transparent")
        btn_frame.pack(expand=True)

        # Creo botones para las múltiples opciones de mapas con Google Earth dentro del subframe
        btn_map_airp = ctk.CTkButton(btn_frame, text='Mapa Aeropuertos', command=lambda: MapAirports(LoadAirports('Airports.txt')))
        btn_map_airp.pack(pady=30)

        btn_lebl_arrivals = ctk.CTkButton(btn_frame, text='Vuelos a LEBL hoy', command=self.procesar_all_arrivals)
        btn_lebl_arrivals.pack(pady=30)

        btn_long_dist_arrv = ctk.CTkButton(btn_frame, text='Llegadas a LEBL de vuelos de larga distancia', command=self.procesar_long_dist_arrv)
        btn_long_dist_arrv.pack(pady=30)

    # Muestra el submenú para gestionar aeropuertos (crear o eliminar).
    def ejecutar_gestionar_airp(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        label = ctk.CTkLabel(self.principal_frame, text="¿Qué quieres?", font=("Arial", 20))
        label.pack(pady=40)

        # Creo un subframe para los botones
        btn_frame = ctk.CTkFrame(self.principal_frame, fg_color="transparent")
        btn_frame.pack(expand=True)

        # Los dos botones los creo dentro del subframe
        btn_crear = ctk.CTkButton(btn_frame, text='Crear', fg_color='green', command=self.ejecutar_create_airp)
        btn_crear.pack(side="left", padx=20)

        btn_elim = ctk.CTkButton(btn_frame, text='Eliminar', fg_color='red', command=self.ejecutar_eliminate_airp)
        btn_elim.pack(side="left", padx=20)
    
    # Muestra el formulario para eliminar un aeropuerto.
    def ejecutar_eliminate_airp(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        label = ctk.CTkLabel(self.principal_frame, text="Introduce el código ICAO del aeropuerto", font=("Arial", 20))
        label.pack(pady=20)

        self.input_ic = ctk.CTkEntry(self.principal_frame, placeholder_text='Código ICAO')
        self.input_ic.pack(pady=100)

        btn_elim = ctk.CTkButton(self.principal_frame, text='Eliminar', fg_color='red', command=self.procesar_eliminate_airp)
        btn_elim.pack(pady=100)
    
    # Muestra el submenú de información técnica (tabla de aeropuertos, ocupación de puertas).
    def ejecutar_info_tecn(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        label = ctk.CTkLabel(self.principal_frame, text="¿Qué información buscas?", font=("Arial", 20))
        label.pack(pady=20)
        
        # Creo un subframe para los botones
        btn_frame = ctk.CTkFrame(self.principal_frame, fg_color="transparent")
        btn_frame.pack(expand=True)

        # Creo botones para las múltiples opciones dentro del subframe
        btn_airp_data = ctk.CTkButton(btn_frame, text='Información aeropuertos', command=lambda: self.ejecutar_visz_airports(LoadAirports('Airports.txt')))
        btn_airp_data.pack(pady=30)

        btn_gates_occupancy = ctk.CTkButton(btn_frame, text='Información sobre las puertas de embarque', command=self.visz_gates_occupancy)
        btn_gates_occupancy.pack(pady=30)

        btn_generate_pdf = ctk.CTkButton(btn_frame, text='Generar informe PDF', command=self.generar_informe_pdf)
        btn_generate_pdf.pack(pady=30)

        btn_horario_operaciones = ctk.CTkButton(btn_frame, text='Horario de operaciones', command=self.mostrar_horario_operaciones)
        btn_horario_operaciones.pack(pady=30)

        btn_vuelos_menos_dos_horas = ctk.CTkButton(btn_frame, text='Cantidad de vuelos con menos de dos horas de estacionamiento.', command=self.informacion_vuelos_menos_dos_horas)
        btn_vuelos_menos_dos_horas.pack(pady=30)
    
    def informacion_vuelos_menos_dos_horas(self):
        if not self.all_flights:
            messagebox.showerror("Error", "No hay vuelos cargados (fusione primero llegadas y salidas).")
            return
        
        cantidad = vuelos_menos_dos_horas(self.all_flights)

        if cantidad == -1: # Este caso no debería darse nunca porque se comprueba en el IF de arriba
            messagebox.showerror("Error", "No hay vuelos cargados!")
        else:
            messagebox.showinfo("Información", f"Hay {cantidad} vuelos cuyo periodo de estacionamiento en el aeropuerto será inferior a dos horas.")

    # Genera un informe en PDF con el estado actual del aeropuerto.
    def generar_informe_pdf(self):
        if self.bcn is None:
            messagebox.showerror("Error", "Cargue primero la estructura del aeropuerto.")
            return
        if not self.all_flights:
            messagebox.showerror("Error", "No hay vuelos cargados (fuse primero llegadas y salidas).")
            return

        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        import io
        from datetime import datetime

        # Elegir archivo de salida
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Guardar informe PDF"
        )
        if not filename:
            return

        # Recopilar datos
        total_gates = 0
        free_gates = 0
        occupied_gates = 0
        occupancy_by_terminal = {}
        for t in self.bcn.terminals:
            occ = 0
            for a in t.boardingAreas:
                for g in a.gates:
                    total_gates += 1
                    if g.occupied:
                        occ += 1
            free = len([g for a in t.boardingAreas for g in a.gates if not g.occupied])
            occupied_gates += occ
            free_gates += free
            occupancy_by_terminal[t.name] = (occ, len([g for a in t.boardingAreas for g in a.gates]))

        # Vuelos no asignados (con AssignGate devuelve -3 o -4; pero podemos contar los que no tienen puerta asignada)
        # Para simplificar, usamos la lista de vuelos y comprobamos si algún gate tiene su id (no es trivial)
        # Mejor: contar vuelos que en la asignación estática fallaron? O podemos simular una asignación completa y ver errores.
        # En lugar de complicar, mostraremos solo estadísticas básicas.

        # Generar gráfico de ocupación por terminal (usando matplotlib)
        fig, ax = plt.subplots(figsize=(6, 4))
        terminals = list(occupancy_by_terminal.keys())
        occupied_counts = [occupancy_by_terminal[t][0] for t in terminals]
        ax.bar(terminals, occupied_counts, color='steelblue')
        ax.set_ylabel("Puertas ocupadas")
        ax.set_title("Ocupación por terminal")
        # Guardar figura en un buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        img_buffer.seek(0)
        plt.close(fig)

        # Crear PDF
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(name='Title', parent=styles['Title'], alignment=1, spaceAfter=20)
        normal_style = styles['Normal']
        content = []

        # Título y fecha
        content.append(Paragraph("Informe del Aeropuerto de Barcelona (LEBL)", title_style))
        content.append(Spacer(1, 12))
        content.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", normal_style))
        content.append(Spacer(1, 12))

        # Estadísticas generales
        content.append(Paragraph(f"<b>Total puertas:</b> {total_gates}", normal_style))
        content.append(Paragraph(f"<b>Puertas libres:</b> {free_gates}", normal_style))
        content.append(Paragraph(f"<b>Puertas ocupadas:</b> {occupied_gates}", normal_style))
        content.append(Spacer(1, 12))

        # Tabla de ocupación por terminal
        table_data = [["Terminal", "Puertas totales", "Puertas ocupadas", "Ocupación (%)"]]
        for t in terminals:
            total = occupancy_by_terminal[t][1]
            occ = occupancy_by_terminal[t][0]
            percent = (occ / total * 100) if total > 0 else 0
            table_data.append([t, str(total), str(occ), f"{percent:.1f}%"])
        table = Table(table_data, colWidths=[80, 80, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        content.append(table)
        content.append(Spacer(1, 12))

        # Gráfico de barras (imagen)
        img = Image(img_buffer, width=400, height=250)
        content.append(img)
        content.append(Spacer(1, 12))

        # Lista de aviones nocturnos (si hay)
        night_aircrafts, _ = NightAircraft(self.all_flights)
        if night_aircrafts:
            content.append(Paragraph("<b>Aviones nocturnos (solo salida):</b>", normal_style))
            night_list = ", ".join([a.id for a in night_aircrafts[:10]])
            if len(night_aircrafts) > 10:
                night_list += f" y {len(night_aircrafts)-10} más."
            content.append(Paragraph(night_list, normal_style))
            content.append(Spacer(1, 12))

        # Observaciones finales
        content.append(Paragraph("Informe generado automáticamente por el sistema I1-Proyect.", normal_style))

        # Construir PDF
        doc.build(content)
        messagebox.showinfo("Informe PDF", f"Informe guardado en:\n{filename}")

    # Muestra en una tabla la información de todos los aeropuertos cargados.
    def ejecutar_visz_airports(self, airports):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        # Por ahora, su función es la de mostrar la información que hay de TODOS los aeropuertos en airports.txt
        # pero con las coordenadas en números gracias a la función LoadAirports('airports.xt')
        self.tabla = ctk.CTkScrollableFrame(self.principal_frame, label_text="Información de los aeropuertos registrados")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabla.grid_columnconfigure((0, 1, 2), weight=1)

        headers = ["Código ICAO", "Latitud", "Longitud", "¿Schengen?"]
        for col, texto in enumerate(headers):
            header = ctk.CTkLabel(
                self.tabla, 
                text=texto, 
                font=("Arial", 14, "bold"),
                fg_color=("#3a7ebf", "#1f538d"),
                text_color="white",
                corner_radius=5
            )
            header.grid(row=0, column=col, sticky="nsew", padx=2, pady=5)
        
        # Empiezo en la fila 1 porque la 0 son los encabezados
        for i, airp in enumerate(airports, start=1):
            icaoCode = airp.icaoCode
            lat = airp.latitude
            lon = airp.longitude
            sch = airp.schengen
            airp_data = [icaoCode, lat, lon, sch]
            for j in range(4):
                dato = ctk.CTkLabel(
                    self.tabla,
                    text=airp_data[j],
                    fg_color='transparent' if i % 2 == 0 else ("#f0f0f0", "#0085B5") #Sentencia if para tener las filas en colores alternos (más facil para seguir una línea)
                )
                dato.grid(row=i, column=j, sticky='nsew', padx=2, pady=2)

    # Muestra el submenú de gráficos (barras, frecuencias, ocupación de puertas).
    def ejecutar_graficos(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        label = ctk.CTkLabel(self.principal_frame, text="¿Qué gráfico quieres?", font=("Arial", 20))
        label.pack(pady=20)
        
        # Creo un subframe para los botones
        btn_frame = ctk.CTkFrame(self.principal_frame, fg_color="transparent")
        btn_frame.pack(expand=True)

        # Creo botones para las múltiples opciones de gráficos dentro del subframe
        btn_grph_sch_nSch = ctk.CTkButton(btn_frame, text='Aeropuertos Schengen & No Schengen', command=self.mostrar_grph_sch_nSch)
        btn_grph_sch_nSch.pack(pady=20)

        btn_grph_arrv_frq = ctk.CTkButton(btn_frame, text='Frecuencias de llegadas a LEBL hoy', command=self.mostrar_grph_arrv_frq)
        btn_grph_arrv_frq.pack(pady=20)

        btn_grph_airlns = ctk.CTkButton(btn_frame, text='Cantidad de llegadas a LEBL hoy por aerolínea', command=self.mostrar_grph_airlns)
        btn_grph_airlns.pack(pady=20)

        btn_grph_flights_type = ctk.CTkButton(btn_frame, text='Llegadas a LEBL hoy desde zona Schengen VS No Schengen', command=self.mostrar_grph_flights_type)
        btn_grph_flights_type.pack(pady=20)

        btn_grph_gates = ctk.CTkButton(btn_frame, text='Mostrar ocupación de los Gates por terminal', command=self.mostrar_grph_gates_occupancy)
        btn_grph_gates.pack(pady=20)

        btn_grph_gates_per_hour = ctk.CTkButton(btn_frame, text='Mostrar ocupación de los Gates a lo largo del día', command=self.mostrar_grph_day_occupancy)
        btn_grph_gates_per_hour.pack(pady=20)

        btn_simulate_day = ctk.CTkButton(btn_frame, text='Ocupación interactiva por hora', command=self.mostrar_ocupacion_interactiva)
        btn_simulate_day.pack(pady=20)
    
    # Muestra un gráfico interactivo con slider para explorar la ocupación hora a hora.
    def mostrar_ocupacion_interactiva(self):
        if self.bcn is None:
            messagebox.showerror("Error", "Cargue primero la estructura del aeropuerto.")
            return
        if not self.all_flights:
            messagebox.showerror("Error", "Cargue y fusione los vuelos primero.")
            return

        # Ventana emergente
        win = ctk.CTkToplevel(self)
        win.title("Ocupación horaria interactiva")
        win.geometry("1000x700")
        
        # Marco para el slider y botones
        control_frame = ctk.CTkFrame(win)
        control_frame.pack(pady=10)
        
        hour_var = ctk.IntVar(value=0)
        slider = ctk.CTkSlider(control_frame, from_=0, to=23, number_of_steps=23, variable=hour_var,
                            command=lambda x: update_plot(int(x)))
        slider.pack(side="left", padx=10)
        
        label_hour = ctk.CTkLabel(control_frame, text="Hora: 00:00")
        label_hour.pack(side="left", padx=10)
        
        # Botones de reproducción
        playing = [False]
        def play():
            playing[0] = True
            def step():
                if playing[0] and hour_var.get() < 23:
                    hour_var.set(hour_var.get() + 1)
                    update_plot(hour_var.get())
                    win.after(500, step)
            step()
        def stop():
            playing[0] = False
        btn_play = ctk.CTkButton(control_frame, text="▶ Reproducir", command=play)
        btn_play.pack(side="left", padx=5)
        btn_stop = ctk.CTkButton(control_frame, text="⏹ Detener", command=stop)
        btn_stop.pack(side="left", padx=5)
        
        # Marco para el gráfico
        frame_graph = ctk.CTkFrame(win)
        frame_graph.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear figura y canvas
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        canvas = FigureCanvasTkAgg(fig, master=frame_graph)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Total de puertas (para escala)
        total_gates = 0
        for t in self.bcn.terminals:
            for area in t.boardingAreas:
                total_gates += len(area.gates)
        
        def update_plot(hour):
            label_hour.configure(text=f"Hora: {hour:02d}:00")
            # Copia del aeropuerto para no modificar el original
            import copy
            bcn_copy = copy.deepcopy(self.bcn)
            # Aplicar asignaciones desde la hora 0 hasta la hora seleccionada
            for h in range(hour + 1):
                time_str = f"{h:02d}:00"
                AssignGatesAtTime(bcn_copy, self.all_flights, time_str)
            # Calcular ocupación por terminal
            terminal_names = []
            occ_values = []
            for t in bcn_copy.terminals:
                terminal_names.append(t.name)
                occ = 0
                for area in t.boardingAreas:
                    for gate in area.gates:
                        if gate.occupied:
                            occ += 1
                occ_values.append(occ)
            
            ax1.clear()
            ax1.bar(terminal_names, occ_values, color='steelblue')
            ax1.set_ylabel("Puertas ocupadas")
            ax1.set_title(f"Ocupación de puertas a las {hour:02d}:00")
            ax1.set_ylim(0, total_gates)
            
            ax2.clear()
            ax2.text(0.5, 0.5, f"Aviones no asignados en el período {hour:02d}:00 - {hour+1:02d}:00:\n"
                    "Consulta el gráfico 'Mostrar ocupación de los Gates a lo largo del día' para ver estadísticas completas.",
                    ha='center', va='center', transform=ax2.transAxes, fontsize=10)
            ax2.axis('off')
            canvas.draw()
        
        # Inicializar
        update_plot(0)
    
    # Muestra un gráfico de la ocupación de los gates por teminal a lo largo del día
    def mostrar_grph_day_occupancy(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        if self.bcn is None:
            messagebox.showerror("Error", "Carga primero la estructura del aeropuerto")
            return

        if not self.all_flights:
            messagebox.showerror("Error", "Primero debe cargar los vuelos (botón 'Cargar llegadas' + botón 'Cargar salidas + botón 'Fusionar llegadas y salidas')")
            return
        
        try:
            self.configurar_tema_matplotlib()

            # Obtengo la figura
            fig = PlotDayOccupancy(self.bcn, self.all_flights)

            # Lo integro en CustomTkinter
            canvas = FigureCanvasTkAgg(fig, master=self.principal_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side='top', fill='both', expand=True, padx=20, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error de Gráfico", f"No se pudo generar el gráfico: {e}")
    
    # Muestra el formulario para crear un nuevo aeropuerto.
    def ejecutar_create_airp(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        label = ctk.CTkLabel(self.principal_frame, text="Crear Aeropuerto", font=("Arial", 20))
        label.pack(pady=20)

        self.input_ic = ctk.CTkEntry(self.principal_frame, placeholder_text='Código ICAO')
        self.input_ic.pack(pady=10)
        self.input_lat = ctk.CTkEntry(self.principal_frame, placeholder_text='Latitud')
        self.input_lat.pack(pady=10)
        self.input_lon = ctk.CTkEntry(self.principal_frame, placeholder_text='Longitud')
        self.input_lon.pack(pady=10)

        crear = ctk.CTkButton(self.principal_frame, text='Crear', fg_color='green', command=self.procesar_create_airp)
        crear.pack(pady=20)
    
    # Valida los datos ingresados, crea un aeropuerto y lo añade a la lista y al archivo Schengen.
    def procesar_create_airp(self):
        codICAO = self.input_ic.get()
        latitud = self.input_lat.get()
        longitud = self.input_lon.get()

        # Valido que las casillas no estén vacías
        if not codICAO or not latitud or not longitud:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
        
        try:
            lat = float(latitud)
            lon = float(longitud)
        except ValueError as e:
            messagebox.showerror('Error', '"Latitud" y "Longitud" deben ser números (punto decimal)')
            return
        
        if codICAO == '':
            messagebox.showerror('Error', 'El campo "Código ICAO" no puede estar vacío.')
            return
        elif len(codICAO) != 4:
            messagebox.showerror('Error', 'Los códigos ICAO son de 4 LETRAS')
            return
        else:
            for ch in list(codICAO):
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
                    pass
                else:
                    messagebox.showerror('Error', 'Todos los caracteres de Código ICAO deben ser letras')
                    return
        
        nuevo_aeropuerto = Airport(ic=codICAO.upper(), lat=latitud, lon=longitud)
        SetSchengen(nuevo_aeropuerto)

        if not AddAirport(LoadAirports('Airports.txt'), nuevo_aeropuerto):
            messagebox.showerror('Error', f'El Aeropuerto con el código {nuevo_aeropuerto.icaoCode} ya está en nuestros datos.')
            return
        else:
            messagebox.showinfo('Creado!', f'Aeropuerto {nuevo_aeropuerto.icaoCode} creado exitosamente!')

        # Limpio las casillas
        self.input_ic.delete(0, 'end')
        self.input_lat.delete(0, 'end')
        self.input_lon.delete(0, 'end')

        # El cursor vuelve a la primera casilla
        self.input_ic.focus()
    
    # Valida el código ICAO ingresado y elimina el aeropuerto de la lista en memoria.
    def procesar_eliminate_airp(self):
        ic = self.input_ic.get()

        if ic == '':
            messagebox.showerror('Error', 'El campo no puede estar vacío.')
            return
        elif len(ic) != 4:
            messagebox.showerror('Error', 'Los códigos ICAO son de 4 LETRAS')
            return
        else:
            for ch in list(ic):
                if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
                    pass
                else:
                    messagebox.showerror('Error', 'Todos los caracteres deben ser letras')
                    return
        
        if RemoveAirport(LoadAirports('Airports.txt'), ic):
            messagebox.showinfo('Eliminado', f'Aeropuerto de código {ic} eliminado correctamente.')
        else:
            messagebox.showerror('Error', f'Este aeropuerto no se encuentra en nuestros datos.')
        
        #Limpio la casilla
        self.input_ic.delete(0, 'end')

    # Limpia la lista de vuelos cargados previa confirmación del usuario.
    def limpiar_vuelos(self):
        if self.all_flights:
            if messagebox.askyesno("Limpiar", "¿Eliminar todos los vuelos cargados?"):
                self.all_flights = []
                messagebox.showinfo("Listo", "Vuelos eliminados.")
    
    # Fusiona la lista de llegadas y salidas en la lista all_flights y luego las vacía
    def fusionar_movimientos(self):
        merged, problems, code = MergeMovements(self.arrivals, self.departures)
        
        if code == -1:
            messagebox.showerror("Error", "No se pudo fusionar: una de las listas (llegadas o salidas) está vacía.")
            return
        
        if code == 0 and merged:
            self.all_flights = merged
            msg = f"Fusión completada: {len(merged)} vuelos combinados."
            if problems:
                msg += f"\n\nAeronaves con incoherencias horarias: {', '.join(problems[:10])}"
                if len(problems) > 10:
                    msg += f" y {len(problems)-10} más."
                messagebox.showwarning("Fusión completada con advertencias", msg)
            else:
                messagebox.showinfo("Fusión completada", msg)
            # Vaciar listas temporales
            self.arrivals = []
            self.departures = []
        else:
            # Es muy raro que code == 0 pero merged vacío, pero podría ocurrir
            messagebox.showerror("Error", "No se pudo generar la lista de vuelos fusionados.")
    
    # Asigna puertas a todos los vuelos cargados utilizando la estructura del aeropuerto.
    def procesar_asignar_puertas(self):
        if self.bcn is None or not isinstance(self.bcn, BarcelonaAP):
            messagebox.showerror("Error", "Primero debe cargar la estructura del aeropuerto")
            return
        if not self.all_flights:
            messagebox.showerror("Error", "Primero debe cargar los vuelos (botón 'Cargar llegadas' + botón 'Cargar salidas + botón 'Fusionar llegadas y salidas')")
            return
        
        ok = 0
        errors = {-1: 0, -2: 0, -3: 0, -4: 0 }
        for flight in self.all_flights:
            ret_rn = AssignGate(self.bcn, flight)
            if ret_rn == 0:
                ok += 1
            else:
                errors[ret_rn] += 1
        
        mensaje = f"Puertas asignadas: {ok}/{len(self.all_flights)}"

        if errors.get(-1):
            mensaje += f"\nNombres de aerolíneas inválidos: {errors[-1]}"
        if errors.get(-2):
            mensaje += f"\nError de lectura de aerolíneas: {errors[-2]}"
        if errors.get(-3):
            mensaje += f"\nAerolíneas no registradas: {errors[-3]}"
        if errors.get(-4):
            mensaje += f"\nSin puertas libres: {errors[-4]}"
        messagebox.showinfo("Asignación", mensaje)
    
    # Guarda los aeropuertos Schengen en un archivo fijo (SchengenAirports.txt).
    def procesar_guardar_schengen(self):
        airports = LoadAirports('Airports.txt')
        SaveSchengenAirports(airports, 'SchengenAirports.txt')
        messagebox.showinfo("Guardado", "Archivo SchengenAirports.txt creado")
    
    # Genera el KML con todos los vuelos cargados y lo abre en Google Earth.
    def procesar_all_arrivals(self):
        if not self.all_flights:
            messagebox.showerror("Error", "Primero debe cargar los vuelos (botón 'Cargar llegadas' + botón 'Cargar salidas + botón 'Fusionar llegadas y salidas')")
            return
        
        MapFlights(self.all_flights, filename='LEBL_Arrivals.kml')

    # Genera el KML solo con vuelos de larga distancia (>2000 km) y lo abre en Google Earth.
    def procesar_long_dist_arrv(self):
        if not self.all_flights:
            messagebox.showerror("Error", "Primero debe cargar los vuelos (botón 'Cargar llegadas' + botón 'Cargar salidas + botón 'Fusionar llegadas y salidas')")
            return
        
        MapFlights(LongDistanceArrivals(self.all_flights), filename='LEBL_Arrivals_MIN2000.kml')
    
    # Muestra una tabla con la ocupación actual de todas las puertas del aeropuerto.
    def visz_gates_occupancy(self):
        if self.bcn is None or not isinstance(self.bcn, BarcelonaAP):
            messagebox.showerror("Error", "Primero debe cargar la estructura del aeropuerto.")
            return

        for widget in self.principal_frame.winfo_children():
            widget.destroy()

        gates_info = GateOccupancy(self.bcn) # Lista de diccionarios con la información de cada gate

        self.tabla = ctk.CTkScrollableFrame(self.principal_frame, label_text="Ocupación de puertas")
        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        headers = ["Terminal", "Área", "Puerta", "Estado", "Aircraft ID"]
        for col, texto in enumerate(headers):
            header = ctk.CTkLabel(
                self.tabla, text=texto, font=("Arial", 14, "bold"),
                fg_color=("#3a7ebf", "#1f538d"), text_color="white", corner_radius=5
            )
            header.grid(row=0, column=col, sticky="nsew", padx=2, pady=5)
            self.tabla.grid_columnconfigure(col, weight=1)

        for i, g in enumerate(gates_info, start=1):
            estado = "Ocupada" if g["occupied"] else "Libre"
            datos = [g["terminal"], g["area"], g["gate"], estado, g["aircraft"] if g["occupied"] else ""]
            for j, val in enumerate(datos):
                label = ctk.CTkLabel(
                    self.tabla, text=val,
                    fg_color='transparent' if i % 2 == 0 else ("#f0f0f0", "#0085B5")
                )
                label.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
    
    # Muestra ventanas con el gráfico de ocupación de cada terminal.
    def mostrar_grph_gates_occupancy(self):
        if self.bcn is None:
            messagebox.showerror("Error", "Carga primero la estructura del aeropuerto")
            return
        
        self.configurar_tema_matplotlib()

        gates_info = GateOccupancy(self.bcn)
        for terminal in self.bcn.terminals:
            fig = PlotTerminalOccupancy(gates_info, terminal.name)
            if fig:
                ventana = ctk.CTkToplevel(self)
                ventana.title(f"Ocupación Terminal {terminal.name}")
                canvas = FigureCanvasTkAgg(fig, master=ventana)
                canvas.draw()
                canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Abre un diálogo para guardar la lista de vuelos en un archivo de texto.
    def procesar_save_flights(self):
        if not self.all_flights:
            messagebox.showerror("Error", "Primero debe cargar los vuelos (botón 'Cargar llegadas' + botón 'Cargar salidas + botón 'Fusionar llegadas y salidas')")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            tipo, mensaje = SaveFlights(self.all_flights, filename)
            if tipo == 'ERROR':
                messagebox.showerror('Error', mensaje)
            else:
                messagebox.showinfo('Información', mensaje)

    # Muestra el gráfico de aeropuertos Schengen vs no Schengen.
    def mostrar_grph_sch_nSch(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        try:
            self.configurar_tema_matplotlib()

            # Obtengo la figura
            lista_aeropuertos = LoadAirports('Airports.txt')
            fig = PlotAirports(lista_aeropuertos)

            # Lo integro en CustomTkinter
            canvas = FigureCanvasTkAgg(fig, master=self.principal_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side='top', fill='both', expand=True, padx=20, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error de Gráfico", f"No se pudo generar el gráfico: {e}")
    
    # Muestra el gráfico de frecuencia de llegadas por hora (usa self.all_flights).
    def mostrar_grph_arrv_frq(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        if not self.all_flights:
            messagebox.showerror("Error", "Primero debe cargar los vuelos (botón 'Cargar llegadas' + botón 'Cargar salidas + botón 'Fusionar llegadas y salidas')")
            return
        
        try:
            self.configurar_tema_matplotlib()

            # Obtengo la figura
            fig = PlotArrivals(self.all_flights)

            # Compruebo que fig no sea texto. De serlo es un mensaje de error y debo mostrarlo.
            if isinstance(fig, str):
                messagebox.showerror('Error de datos', fig)
            else:
                # Lo integro en CustomTkinter
                canvas = FigureCanvasTkAgg(fig, master=self.principal_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side='top', fill='both', expand=True, padx=20, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error de Gráfico", f"No se pudo generar el gráfico: {e}")
    
    # Muestra el gráfico de cantidad de vuelos por aerolínea.
    def mostrar_grph_airlns(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        if not self.all_flights:
            messagebox.showerror("Error", "Primero debe cargar los vuelos (botón 'Cargar llegadas' + botón 'Cargar salidas + botón 'Fusionar llegadas y salidas')")
            return
        
        try:
            self.configurar_tema_matplotlib()

            # Obtengo la figura
            fig = PlotAirlines(self.all_flights)

            # Compruebo que fig no sea texto. De serlo es un mensaje de error y debo mostrarlo.
            if isinstance(fig, str):
                messagebox.showerror('Error de datos', fig)
            else:
                # Lo integro en CustomTkinter
                canvas = FigureCanvasTkAgg(fig, master=self.principal_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side='top', fill='both', expand=True, padx=20, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error de Gráfico", f"No se pudo generar el gráfico: {e}")
    
    # Muestra el gráfico de vuelos Schengen vs no Schengen.
    def mostrar_grph_flights_type(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        if not self.all_flights:
            messagebox.showerror("Error", "Primero debe cargar los vuelos (botón 'Cargar llegadas' + botón 'Cargar salidas + botón 'Fusionar llegadas y salidas')")
            return
        
        try:
            self.configurar_tema_matplotlib()

            # Obtengo la figura
            fig = PlotFlightsType(self.all_flights)

            # Compruebo que fig no sea texto. De serlo es un mensaje de error y debo mostrarlo.
            if isinstance(fig, str):
                messagebox.showerror('Error de datos', fig)
            else:
                # Lo integro en CustomTkinter
                canvas = FigureCanvasTkAgg(fig, master=self.principal_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side='top', fill='both', expand=True, padx=20, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error de Gráfico", f"No se pudo generar el gráfico: {e}")

    def mostrar_horario_operaciones(self):
        """Muestra el horario de operaciones (llegadas/salidas) en el frame principal."""
        if not self.all_flights:
            messagebox.showerror("Error", "No hay vuelos cargados.")
            return

        # Limpiar frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()

        # Frame superior para filtros y botones
        filter_frame = ctk.CTkFrame(self.principal_frame)
        filter_frame.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(filter_frame, text="Filtrar por tipo:").pack(side="left", padx=5)
        tipo_var = ctk.StringVar(value="todos")
        radio_todos = ctk.CTkRadioButton(filter_frame, text="Todos", variable=tipo_var, value="todos")
        radio_todos.pack(side="left", padx=5)
        radio_llegadas = ctk.CTkRadioButton(filter_frame, text="Solo llegadas", variable=tipo_var, value="Llegada")
        radio_llegadas.pack(side="left", padx=5)
        radio_salidas = ctk.CTkRadioButton(filter_frame, text="Solo salidas", variable=tipo_var, value="Salida")
        radio_salidas.pack(side="left", padx=5)

        ctk.CTkLabel(filter_frame, text="Compañía (código ICAO):").pack(side="left", padx=5)
        company_var = ctk.StringVar(value="")
        company_entry = ctk.CTkEntry(filter_frame, textvariable=company_var, width=100)
        company_entry.pack(side="left", padx=5)

        btn_aplicar = ctk.CTkButton(filter_frame, text="Aplicar filtros", 
                                    command=lambda: self.actualizar_tabla_eventos(tipo_var.get(), company_var.get().strip().upper()))
        btn_aplicar.pack(side="left", padx=10)

        btn_exportar = ctk.CTkButton(filter_frame, text="Exportar a CSV", 
                                    command=lambda: self.exportar_eventos_csv(tipo_var.get(), company_var.get().strip().upper()))
        btn_exportar.pack(side="right", padx=10)

        # Área de texto para la tabla (mucho más eficiente que cientos de labels)
        self.textbox_eventos = ctk.CTkTextbox(self.principal_frame, font=("Courier New", 12))
        self.textbox_eventos.pack(fill="both", expand=True, padx=10, pady=10)

        # Mostrar datos iniciales
        self.actualizar_tabla_eventos(tipo_var.get(), company_var.get().strip().upper())

    def actualizar_tabla_eventos(self, tipo, company_filter):
        """Construye y muestra la tabla de eventos aplicando filtros correctamente."""
        # Precalcular diccionario de puertas asignadas (una sola vez)
        puertas_por_avion = {}
        if self.bcn:
            for t in self.bcn.terminals:
                for a in t.boardingAreas:
                    for g in a.gates:
                        if g.id:
                            puertas_por_avion[g.id] = g.name

        eventos = []
        for a in self.all_flights:
            # Para cada avión, generar eventos según los movimientos que tenga
            movimientos = []
            if a.land_time:
                movimientos.append(("Llegada", a.land_time, a.origin_airp))
            if a.departure_time:
                movimientos.append(("Salida", a.departure_time, a.destination_airp))

            for tipo_evento, hora, od in movimientos:
                # Aplicar filtros ANTES de añadir a la lista
                if tipo != "todos" and tipo_evento != tipo:
                    continue
                if company_filter and company_filter != a.company:
                    continue
                puerta = puertas_por_avion.get(a.id, "")
                eventos.append((tipo_evento, hora, a.id, a.company, od, puerta))

        # Ordenar por hora (formato hh:mm)
        eventos.sort(key=lambda x: x[1])

        # Preparar texto formateado (anchos fijos)
        header = f"{'Hora':<8} {'Tipo':<12} {'ID':<10} {'Aerolínea':<12} {'Origen/Destino':<15} {'Puerta':<10}\n"
        separator = "-" * 80 + "\n"
        lines = [header, separator]
        for ev in eventos:
            hora, tipo_ev, aid, comp, od, puerta = ev[1], ev[0], ev[2], ev[3], ev[4], ev[5]
            lines.append(f"{hora:<8} {tipo_ev:<12} {aid:<10} {comp:<12} {od:<15} {puerta:<10}\n")

        # Actualizar textbox
        self.textbox_eventos.delete("0.0", "end")
        self.textbox_eventos.insert("0.0", "".join(lines))

    def exportar_eventos_csv(self, tipo, company_filter):
        """Exporta los eventos actualmente filtrados a CSV."""
        puertas_por_avion = {}
        if self.bcn:
            for t in self.bcn.terminals:
                for a in t.boardingAreas:
                    for g in a.gates:
                        if g.id:
                            puertas_por_avion[g.id] = g.name

        eventos = []
        for a in self.all_flights:
            movimientos = []
            if a.land_time:
                movimientos.append(("Llegada", a.land_time, a.origin_airp))
            if a.departure_time:
                movimientos.append(("Salida", a.departure_time, a.destination_airp))

            for tipo_evento, hora, od in movimientos:
                if tipo != "todos" and tipo_evento != tipo:
                    continue
                if company_filter and company_filter != a.company:
                    continue
                puerta = puertas_por_avion.get(a.id, "")
                eventos.append((tipo_evento, hora, a.id, a.company, od, puerta))

        eventos.sort(key=lambda x: x[1])

        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if filename:
            import csv
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Hora", "Tipo", "ID", "Aerolínea", "Origen/Destino", "Puerta"])
                for ev in eventos:
                    writer.writerow([ev[1], ev[0], ev[2], ev[3], ev[4], ev[5]])
            messagebox.showinfo("Exportar", f"Eventos exportados a {filename}")

if __name__ == "__main__":
    app = InterfazPrincipal()
    app.mainloop()