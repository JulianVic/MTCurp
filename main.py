import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime
from tkinter import ttk

# Estados permitidos según la máquina de Turing
estados_validos = {
    "AS", "BC", "BS", "CC", "CL", "CM", "CS", "CH", "DF", "DG", "GT", "GR",
    "HG", "JC", "MC", "MN", "MS", "NT", "NL", "OC", "PL", "QT", "QR", "SP",
    "SL", "SR", "TC", "TS", "TL", "VZ", "YN", "ZS", "NE"
}

# Diccionario para mapear nombres de estados a claves
estados_nombres = {
    "BAJA CALIFORNIA": "BC",
    "BAJA CALIFORNIA SUR": "BS",
    "CAMPECHE": "CC",
    "COAHUILA": "CL",
    "COLIMA": "CM",
    "CHIAPAS": "CS",
    "CHIHUAHUA": "CH",
    "DISTRITO FEDERAL": "DF",
    "DURANGO": "DG",
    "GUANAJUATO": "GT",
    "GUERRERO": "GR",
    "HIDALGO": "HG",
    "JALISCO": "JC",
    "MÉXICO": "MC",
    "MICHOACÁN": "MN",
    "MORELOS": "MS",
    "NAYARIT": "NT",
    "NUEVO LEÓN": "NL",
    "OAXACA": "OC",
    "PUEBLA": "PL",
    "QUERÉTARO": "QT",
    "QUINTANA ROO": "QR",
    "SAN LUIS POTOSÍ": "SP",
    "SINALOA": "SL",
    "SONORA": "SR",
    "TABASCO": "TC",
    "TAMAULIPAS": "TS",
    "TLAXCALA": "TL",
    "VERACRUZ": "VZ",
    "YUCATÁN": "YN",
    "ZACATECAS": "ZS",
    "NACIDO EN EL EXTRANJERO": "NE"
}

# Funciones auxiliares para obtener la primera vocal y consonante interna
def primer_vocal_interna(texto):
    for letra in texto[1:]:
        if letra in 'AEIOU':
            return letra
    return 'X'

def primer_consonante_interna(texto):
    for letra in texto[1:]:
        if letra in 'BCDFGHJKLMNÑPQRSTVWXYZ':
            return letra
    return 'X'

# Verificación de año bisiesto
def es_bisiesto(año):
    return año % 4 == 0 and (año % 100 != 0 or año % 400 == 0)

# Función principal para generar la CURP
def generar_curp():
    # Obtener valores de los campos
    nombre = entry_nombre.get().upper()
    apellido_paterno = entry_apellido_paterno.get().upper()
    apellido_materno = entry_apellido_materno.get().upper()
    fecha_nacimiento = entry_fecha_nacimiento.get()  # Formato: dd/mm/yyyy
    sexo = entry_sexo.get().upper()
    estado = entry_estado.get().upper()
    
    # Validación de la fecha de nacimiento
    try:
        dia, mes, año = map(int, fecha_nacimiento.split('/'))
        # Verificar año bisiesto para 29 de febrero
        if dia == 29 and mes == 2 and not es_bisiesto(año):
            messagebox.showerror("Error", "29 de febrero solo es válido en años bisiestos.")
            return
        # Validar si la fecha es válida en general
        datetime(año, mes, dia)
    except ValueError:
        messagebox.showerror("Error", "Fecha de nacimiento debe estar en formato válido dd/mm/yyyy")
        return
    
    # Validación de género
    if sexo not in {"H", "M"}:
        messagebox.showerror("Error", "Género debe ser 'H' para hombre o 'M' para mujer")
        return
    
    # Validación del estado
    nombre_estado = entry_estado.get()
    estado = estados_nombres.get(nombre_estado, "")
    if not estado or estado not in estados_validos:
        messagebox.showerror("Error", f"Estado '{nombre_estado}' no es válido.")
        return
    
    # Construcción de la CURP
    año = str(año)[-2:]  # Últimos dos dígitos del año
    mes = f"{mes:02}"  # Mes en dos dígitos
    dia = f"{dia:02}"  # Día en dos dígitos
    
    curp = (
        apellido_paterno[0] +
        primer_vocal_interna(apellido_paterno) +
        apellido_materno[0] +
        nombre[0] +
        año + mes + dia +
        sexo +
        estado +
        primer_consonante_interna(apellido_paterno) +
        primer_consonante_interna(apellido_materno) +
        primer_consonante_interna(nombre) +
        str(random.randint(10, 99))
    )

    # Mostrar CURP generada
    label_resultado.config(text=f"CURP Generada: {curp}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Generador de CURP")

# Crear y organizar los campos de entrada
tk.Label(root, text="Nombre").grid(row=0, column=0)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1)

tk.Label(root, text="Apellido Paterno").grid(row=1, column=0)
entry_apellido_paterno = tk.Entry(root)
entry_apellido_paterno.grid(row=1, column=1)

tk.Label(root, text="Apellido Materno").grid(row=2, column=0)
entry_apellido_materno = tk.Entry(root)
entry_apellido_materno.grid(row=2, column=1)

tk.Label(root, text="Fecha de Nacimiento (dd/mm/yyyy)").grid(row=3, column=0)
entry_fecha_nacimiento = tk.Entry(root)
entry_fecha_nacimiento.grid(row=3, column=1)

tk.Label(root, text="Sexo (H/M)").grid(row=4, column=0)
entry_sexo = tk.Entry(root)
entry_sexo.grid(row=4, column=1)

tk.Label(root, text="Estado").grid(row=5, column=0)
entry_estado = ttk.Combobox(root, values=list(estados_nombres.keys()), state="readonly")
entry_estado.grid(row=5, column=1)

# Botón para generar la CURP
btn_generar = tk.Button(root, text="Generar CURP", command=generar_curp)
btn_generar.grid(row=6, column=0, columnspan=2)

# Etiqueta para el resultado de CURP
label_resultado = tk.Label(root, text="")
label_resultado.grid(row=7, column=0, columnspan=2)

# Iniciar interfaz gráfica
root.mainloop()
