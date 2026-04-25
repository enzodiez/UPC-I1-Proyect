import customtkinter as ctk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from airport import *
from aircraft import *

# Configuración de apariencia
ctk.set_appearance_mode("dark")  # Modos: "system" (standard), "dark", "light"
ctk.set_default_color_theme("blue")  # Temas: "blue" (standard), "green", "dark-blue"

class InterfazPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        
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

        self.registros = ctk.CTkButton(self.options_frame, text="Registros", corner_radius=5, border_width=2, command=self.ejecutar_registros)
        self.registros.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)

        self.visz_data = ctk.CTkButton(self.options_frame, text="Información técnica", corner_radius=5, border_width=2, command=self.ejecutar_info_tecn)
        self.visz_data.grid(row=1, column=0, sticky='nsew', padx=15, pady=15)

        self.graphs = ctk.CTkButton(self.options_frame, text="Gráficos", corner_radius=5, border_width=2, command=self.ejecutar_graficos)
        self.graphs.grid(row=2, column=0, sticky='nsew', padx=15, pady=15)

        self.maps = ctk.CTkButton(self.options_frame, text="Mapas con Google Earth", corner_radius=5, border_width=2, command=self.ejecutar_google_earth)
        self.maps.grid(row=3, column=0, sticky='nsew', padx=15, pady=15)

        self.switch_appear = ctk.StringVar(value="on")
        self.appearance = ctk.CTkSwitch(self.options_frame, text='Modo Oscuro', onvalue='on', offvalue='off', variable=self.switch_appear, command=self.cambiar_modo_toggle)
        self.appearance.grid(row=4, column=0, sticky='nsew', padx=15, pady=15)

        self.principal_frame = ctk.CTkFrame(self)
        self.principal_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Sirve para poder cerrar bien la interfaz
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    # Este método me lo ha explicado la IA DeepSeek
    # Sirve para poder cerrar bien todos los gráficos y evitar que aparezcan errores en la terminal si se cierra la aplicación con gráficos abiertos.
    def on_closing(self):
        # Cerrar todas las figuras de matplotlib
        plt.close('all')
        # Destruir la ventana principal
        self.quit()
        self.destroy()

    def cambiar_modo_toggle(self):
        if self.switch_appear.get() == "on":
            ctk.set_appearance_mode("dark")
            self.appearance.configure(text="Modo Oscuro")
        else:
            ctk.set_appearance_mode("light")
            self.appearance.configure(text="Modo Claro")
    
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
        btn_map_airp.pack(pady=30)

        btn_lebl_arrivals = ctk.CTkButton(btn_frame, text='Guardar llegadas hoy a LEBL', command=self.procesar_save_flights)
        btn_lebl_arrivals.pack(pady=30)

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

        btn_lebl_arrivals = ctk.CTkButton(btn_frame, text='Vuelos a LEBL hoy', command=lambda: MapFlights(LoadArrivals('Arrivals.txt'), filename='LEBL_Arrivals.kml'))
        btn_lebl_arrivals.pack(pady=30)

        btn_long_dist_arrv = ctk.CTkButton(btn_frame, text='Llegadas a LEBL de vuelos de larga distancia', command=self.procesar_long_dist_arrv)
        btn_long_dist_arrv.pack(pady=30)

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
    
    def ejecutar_eliminate_airp(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        label = ctk.CTkLabel(self.principal_frame, text="introduce el código ICAO del aeropuerto", font=("Arial", 20))
        label.pack(pady=20)

        self.input_ic = ctk.CTkEntry(self.principal_frame, placeholder_text='Código ICAO')
        self.input_ic.pack(pady=100)

        btn_elim = ctk.CTkButton(self.principal_frame, text='Eliminar', fg_color='red', command=self.procesar_eliminate_airp)
        btn_elim.pack(pady=100)
    
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
    
    def procesar_long_dist_arrv(self):
        long_distance_arrivals_aircrafts = MapFlights(LongDistanceArrivals(LoadArrivals('Arrivals.txt')), filename='LEBL_Arrivals_MIN2000.kml')

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
        btn_grph_sch_nSch.pack(pady=30)

        btn_grph_arrv_frq = ctk.CTkButton(btn_frame, text='Frecuencias de llegadas a LEBL hoy', command=self.mostrar_grph_arrv_frq)
        btn_grph_arrv_frq.pack(pady=30)

        btn_grph_airlns = ctk.CTkButton(btn_frame, text='Cantidad de llegadas a LEBL hoy por aerolínea', command=self.mostrar_grph_airlns)
        btn_grph_airlns.pack(pady=30)

        btn_grph_flights_type = ctk.CTkButton(btn_frame, text='Llegadas a LEBL hoy desde zona Schengen VS No Schengen', command=self.mostrar_grph_flights_type)
        btn_grph_flights_type.pack(pady=30)

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
    
    def procesar_save_flights(self):
        type, txt = SaveFlights(LoadArrivals('Arrivals.txt'), 'ArrivalsToLEBL.txt')
        
        if type == 'ERROR':
            messagebox.showerror('Error', txt)
        elif type == 'INFO':
            messagebox.showinfo('Información', txt)

    def mostrar_grph_sch_nSch(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        try:
            # Configuro el estilo ANTES de crear la figura
            plt.rcParams.update({
                'figure.facecolor': '#2b2b2b', 
                'axes.facecolor': '#2b2b2b', 
                'text.color': 'white', 
                'axes.labelcolor': 'white', 
                'xtick.color': 'white', 
                'ytick.color': 'white'
            })

            # Obtengo la figura
            lista_aeropuertos = LoadAirports('Airports.txt')
            fig = PlotAirports(lista_aeropuertos)

            # Lo integro en CustomTkinter
            canvas = FigureCanvasTkAgg(fig, master=self.principal_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side='top', fill='both', expand=True, padx=20, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error de Gráfico", f"No se pudo generar el gráfico: {e}")
    
    def mostrar_grph_arrv_frq(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        try:
            # Configuro el estilo ANTES de crear la figura
            plt.rcParams.update({
                'figure.facecolor': "#2b2b2b", 
                'axes.facecolor': "#2b2b2b", 
                'text.color': 'white', 
                'axes.labelcolor': 'white', 
                'xtick.color': 'white', 
                'ytick.color': 'white'
            })

            # Obtengo la figura
            lista_aircrafts = LoadArrivals('Arrivals.txt')
            fig = PlotArrivals(lista_aircrafts)

            # Compruebo que fig no sea texto. De serlo es un mensaje de error y debo mostrarlo.
            if type(fig) == str:
                messagebox.showerror('Error de datos', fig)
            else:
                # Lo integro en CustomTkinter
                canvas = FigureCanvasTkAgg(fig, master=self.principal_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side='top', fill='both', expand=True, padx=20, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error de Gráfico", f"No se pudo generar el gráfico: {e}")
    
    def mostrar_grph_airlns(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        try:
            # Configuro el estilo ANTES de crear la figura
            plt.rcParams.update({
                'figure.facecolor': '#2b2b2b', 
                'axes.facecolor': '#2b2b2b', 
                'text.color': 'white', 
                'axes.labelcolor': 'white', 
                'xtick.color': 'white', 
                'ytick.color': 'white'
            })

            # Obtengo la figura
            lista_aircrafts = LoadArrivals('Arrivals.txt')
            fig = PlotAirlines(lista_aircrafts)

            # Compruebo que fig no sea texto. De serlo es un mensaje de error y debo mostrarlo.
            if type(fig) == str:
                messagebox.showerror('Error de datos', fig)
            else:
                # Lo integro en CustomTkinter
                canvas = FigureCanvasTkAgg(fig, master=self.principal_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side='top', fill='both', expand=True, padx=20, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error de Gráfico", f"No se pudo generar el gráfico: {e}")
    
    def mostrar_grph_flights_type(self):
        # Vaciar el frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()
        
        try:
            # Configuro el estilo ANTES de crear la figura
            plt.rcParams.update({
                'figure.facecolor': '#2b2b2b', 
                'axes.facecolor': '#2b2b2b', 
                'text.color': 'white', 
                'axes.labelcolor': 'white', 
                'xtick.color': 'white', 
                'ytick.color': 'white'
            })

            # Obtengo la figura
            lista_aircrafts = LoadArrivals('Arrivals.txt')
            fig = PlotFlightsType(lista_aircrafts)

            # Compruebo que fig no sea texto. De serlo es un mensaje de error y debo mostrarlo.
            if type(fig) == str:
                messagebox.showerror('Error de datos', fig)
            else:
                # Lo integro en CustomTkinter
                canvas = FigureCanvasTkAgg(fig, master=self.principal_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(side='top', fill='both', expand=True, padx=20, pady=20)
            
        except Exception as e:
            messagebox.showerror("Error de Gráfico", f"No se pudo generar el gráfico: {e}")

if __name__ == "__main__":
    app = InterfazPrincipal()
    app.mainloop()