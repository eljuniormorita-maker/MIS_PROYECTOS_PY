import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import math

class Usuario:
    def __init__(self):
        self._usuario = 'programacion'
        self._password = 'programacion'
    def validar(self, usuario_ingresado, password_ingresada):
        return usuario_ingresado == self._usuario and password_ingresada == self._password

class Vehiculo:
    def __init__(self, placa, marca, servicio, tarifa):
        self._placa = placa
        self._marca = marca
        self._servicio = servicio
        self._tarifa = tarifa
        self._hora_entrada = datetime.now()

lista_vehiculos = []
TARIFAS = {'Basic': 8000, 'Standard': 12000, 'Premium': 20000}
total_ganado_dia = 0

def crear_ventana_principal():
    global entry_ganado_dia
    root = tk.Tk()
    root.geometry('700x600')
    root.title('ChronoWash System - Main Module')


    fecha_label = tk.Label(root, text="", font=('Arial', 9, 'bold'))
    fecha_label.pack(pady=5)
    def actualizar_fecha():
        fecha_label.config(text=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        root.after(1000, actualizar_fecha)
    actualizar_fecha()

    tk.Label(root, text='Vehicle Plate:').pack()
    entry_placa = tk.Entry(root,font=('Arial', 12))
    entry_placa.pack()
    entry_placa.focus_set()

    tk.Label(root, text='Brand / Model:').pack()
    entry_marca = tk.Entry(root, font=('Arial', 12))
    entry_marca.pack()

    tk.Label(root, text='Service (Client choice):').pack()
    combo_servicio = ttk.Combobox(root, values=list(TARIFAS.keys()), state='readonly')
    combo_servicio.pack()
    combo_servicio.set('Basic')

    label_precio = tk.Label(root, text="", font=('Arial', 11, 'bold'), fg='darkgreen')
    label_precio.pack(pady=3)

    def actualizar_precio(event=None):
        servicio_actual = combo_servicio.get()
        precio_actual = TARIFAS[servicio_actual]
        label_precio.config(text=f"Price per hour: ${precio_actual} COP - Service: {servicio_actual}")

    combo_servicio.bind("<<ComboboxSelected>>", actualizar_precio)
    actualizar_precio()

    tabla = ttk.Treeview(root, columns=('Plate','Brand','Service','Entry'), show='headings')
    tabla.heading('Plate', text='Plate', anchor='center')
    tabla.column('Plate', anchor='center', width=130)
    tabla.heading('Brand', text='Brand', anchor='center')
    tabla.column('Brand', anchor='center', width=130)
    tabla.heading('Service', text='Service', anchor='center')
    tabla.column('Service', anchor='center', width=100)
    tabla.heading('Entry', text='Entry Time', anchor='center')
    tabla.column('Entry', anchor='center', width=170)
    tabla.pack(fill='both', expand=True, padx=10, pady=10)

    frame_stats = tk.Frame(root)
    frame_stats.pack()
    label_contador = tk.Label(frame_stats, text="Vehicles inside: 0", font=('Arial', 10, 'bold'), fg='blue')
    label_contador.pack(side=tk.LEFT, padx=20)
    label_ganancias = tk.Label(frame_stats, text="Total earnings today: $0", font=('Arial', 10, 'bold'), fg='green')
    label_ganancias.pack(side=tk.LEFT, padx=20)

    def actualizar_tabla():
        for i in tabla.get_children(): 
            tabla.delete(i)
        for v in lista_vehiculos:
            tabla.insert('', 'end', values=(v._placa, v._marca, v._servicio, v._hora_entrada.strftime('%Y-%m-%d %H:%M:%S')))
        label_contador.config(text=f"Vehicles inside: {len(lista_vehiculos)}")
        label_ganancias.config(text=f"Total earnings today: ${total_ganado_dia}")

    def registrar_entrada():
        placa = entry_placa.get().strip().upper()
        marca = entry_marca.get().strip()
        if not placa: 
           messagebox.showwarning("Warning", "Plate cannot be empty")
           return
        if any(v._placa == placa for v in lista_vehiculos):
           messagebox.showerror("Error", f"Vehicle {placa} is already inside")
           return
        nuevo = Vehiculo(placa, marca, combo_servicio.get(), TARIFAS.get(combo_servicio.get()))
        lista_vehiculos.append(nuevo)
        entry_placa.delete(0, tk.END)
        entry_marca.delete(0, tk.END)
        entry_placa.focus_set()
        actualizar_tabla()
        
    def registrar_salida():
        global total_ganado_dia
        sel = tabla.selection()
        if not sel: 
            messagebox.showwarning("Warning", "Select a vehicle from table")
            return
        placa = tabla.item(sel[0])['values'][0]
        vehiculo = next((x for x in lista_vehiculos if x._placa == placa), None)
        horas = math.ceil((datetime.now() - vehiculo._hora_entrada).total_seconds() / 3600)
        if horas == 0: horas = 1
        total = horas * vehiculo._tarifa

        hora_entrada_str = vehiculo._hora_entrada.strftime('%H:%M:%S - %Y-%m-%d')
        hora_salida_str = datetime.now().strftime('%H:%M:%S - %Y-%m-%d')


        messagebox.showinfo('Invoice',
            f'Plate: {vehiculo._placa}\n'
            f'Service: {vehiculo._servicio}\n\n'
            f'Entry Time: {hora_entrada_str}\n'
            f'Exit Time: {hora_salida_str}\n\n'
            f'Hours: {horas}\n'
            f'TOTAL: ${total}')

        total_ganado_dia += total
        lista_vehiculos.remove(vehiculo)
        actualizar_tabla()
        

    tk.Button(root, text='Register Entry', command=registrar_entrada, bg='green', fg='white', font=('Arial', 11,'bold')).pack(pady=5)
    tk.Button(root, text='Register Exit and Calculate Cost', command=registrar_salida, bg='red', fg='white').pack(pady=5)

    root.mainloop()

def intentar_login():
    if Usuario().validar(entry_user.get().strip(), entry_pwd.get().strip()):
        login_window.destroy()
        crear_ventana_principal()
    else:
        messagebox.showerror('Access Denied', 'Invalid credentials')

login_window = tk.Tk()
login_window.title('Login - ChronoWash')
login_window.geometry('300x200')
tk.Label(login_window, text='Username:').pack(pady=5)
entry_user = tk.Entry(login_window); entry_user.pack(); entry_user.insert(0, 'programacion')
tk.Label(login_window, text='Password:').pack(pady=5)
entry_pwd = tk.Entry(login_window, show="*"); entry_pwd.pack(); entry_pwd.insert(0, 'programacion')
tk.Button(login_window, text='Login', command=intentar_login).pack(pady=20)
login_window.mainloop()