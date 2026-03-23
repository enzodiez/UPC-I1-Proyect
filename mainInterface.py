import customtkinter as ctk
from tkinter import messagebox
import FigureCanvasTkAgg
from airport import *

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

        self.create_airp = ctk.CTkButton(self.options_frame, text="Crear Aeropuerto", corner_radius=5, border_width=2, command=self.ejecutar_create_airp)
        self.create_airp.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
        self.visz_airp_data = ctk.CTkButton(self.options_frame, text="Ver información aeropuerto/s", corner_radius=5, border_width=2)
        self.visz_airp_data.grid(row=1, column=0, sticky='nsew', padx=15, pady=15)
        self.gr_Sch_NSch = ctk.CTkButton(self.options_frame, text="Gráfico aeropuertos Schengen/No-Schengen", corner_radius=5, border_width=2, command=self.mostrar_gra_sch_nSch)
        self.gr_Sch_NSch.grid(row=2, column=0, sticky='nsew', padx=15, pady=15)
        self.map_airp = ctk.CTkButton(self.options_frame, text="Crear Aeropuerto", corner_radius=5, border_width=2)
        self.map_airp.grid(row=3, column=0, sticky='nsew', padx=15, pady=15)
        self.switch_appear = ctk.StringVar(value="on")
        self.appearance = ctk.CTkSwitch(self.options_frame, text='Modo Oscuro', onvalue='on', offvalue='off', variable=self.switch_appear, command=self.cambiar_modo_toggle)
        self.appearance.grid(row=4, column=0, sticky='nsew', padx=15, pady=15)

        self.principal_frame = ctk.CTkFrame(self)
        self.principal_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    
    def cambiar_modo_toggle(self):
        if self.switch_appear.get() == "on":
            ctk.set_appearance_mode("dark")
            self.appearance.configure(text="Modo Oscuro")
        else:
            ctk.set_appearance_mode("light")
            self.appearance.configure(text="Modo Claro")
    
    def ejecutar_create_airp(self):
        # Vaciar frame principal
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
    
    def procesar_create_airp(self):
        codICAO = self.input_ic.get()
        latitud = self.input_lat.get()
        longitud = self.input_lon.get()

        # Valido que las casillas no estén vacías
        if not codICAO or not latitud or not longitud:
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
        
        nuevo_aeropuerto = Airport(ic=codICAO, lat=latitud, lon=longitud)
        save_new_airport(nuevo_aeropuerto)

        # Limpio las casillas
        self.input_ic.delete(0, 'end')
        self.input_lat.delete(0, 'end')
        self.input_lon.delete(0, 'end')

        # El cursor vuelve a la primera casilla
        self.input_ic.focus()

        messagebox.showinfo('Creado!', f'Aeropuerto {codICAO} creado exitosamente!')

    def mostrar_gra_sch_nSch(self):
        # Vaciar frame principal
        for widget in self.principal_frame.winfo_children():
            widget.destroy()

        fig = PlotAirports(LoadAirports('Airports.txt'))

        canvas = FigureCanvasTkAgg(fig, master=self.principal_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True, padx=20, pady=20)

        plt.rcParams.update({'figure.facecolor': '#2b2b2b', 'axes.facecolor': '#2b2b2b', 'text.color': 'white', 'axes.labelcolor': 'white', 'xtick.color': 'white', 'ytick.color': 'white'})

if __name__ == "__main__":
    app = InterfazPrincipal()
    app.mainloop()
