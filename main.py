import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import heapq

# -----------------------------------
# 📐 TAMAÑO
# -----------------------------------
ANCHO_MAPA = 564
ALTO_MAPA = 744
ANCHO_PANEL = 260

# -----------------------------------
# 📍 CIUDADES
# -----------------------------------
ciudades = {
    "Bogotá": (300, 350),
    "Medellín": (200, 250),
    "Cali": (180, 450),
    "Barranquilla": (260, 120),
    "Cartagena": (240, 150),
    "Santa Marta": (280, 110),
    "Riohacha": (350, 90),
    "Valledupar": (350, 160),
    "Montería": (200, 200),
    "Sincelejo": (230, 180),
    "Bucaramanga": (350, 250),
    "Cúcuta": (420, 230),
    "Tunja": (320, 300),
    "Villavicencio": (350, 380),
    "Yopal": (450, 330),
    "Arauca": (500, 280),
    "Ibagué": (260, 380),
    "Neiva": (300, 500),
    "Florencia": (320, 600),
    "Pasto": (150, 650),
    "Popayán": (170, 550),
    "Quibdó": (120, 300),
    "Pereira": (210, 350),
    "Manizales": (220, 320),
    "Armenia": (200, 380),
    "Leticia": (550, 700),
    "Mitú": (600, 600),
    "Puerto Carreño": (550, 400),
    "San José del Guaviare": (400, 450),
    "Inírida": (500, 500),
    "Mocoa": (350, 650),
    "San Andrés": (100, 80)
}
# -----------------------------------
# 🔗 GRAFO CONECTADO
# -----------------------------------
grafo = {
    "Bogotá": [("Ibagué", 195), ("Villavicencio", 120), ("Tunja", 141)],
    
    "Ibagué": [("Bogotá", 195), ("Cali", 265), ("Armenia", 80), ("Neiva", 210)],
    
    "Armenia": [("Ibagué", 80), ("Pereira", 45)],
    
    "Pereira": [("Armenia", 45), ("Manizales", 50), ("Medellín", 215)],
    
    "Manizales": [("Pereira", 50)],
    
    "Medellín": [("Pereira", 215), ("Montería", 400)],
    
    "Montería": [("Medellín", 400), ("Sincelejo", 90)],
    
    "Sincelejo": [("Montería", 90), ("Cartagena", 180)],
    
    "Cartagena": [("Sincelejo", 180), ("Barranquilla", 120)],
    
    "Barranquilla": [("Cartagena", 120), ("Santa Marta", 105)],
    
    "Santa Marta": [("Barranquilla", 105), ("Riohacha", 170)],
    
    "Riohacha": [("Santa Marta", 170), ("Valledupar", 160)],
    
    "Valledupar": [("Riohacha", 160), ("Bucaramanga", 400)],
    
    "Bucaramanga": [("Valledupar", 400), ("Cúcuta", 195), ("Tunja", 280)],
    
    "Cúcuta": [("Bucaramanga", 195)],
    
    "Tunja": [("Bogotá", 141), ("Bucaramanga", 280)],
    
    "Villavicencio": [("Bogotá", 120), ("Yopal", 270)],
    
    "Yopal": [("Villavicencio", 270), ("Arauca", 430)],
    
    "Arauca": [("Yopal", 430)],
    
    "Neiva": [("Ibagué", 210), ("Florencia", 180)],
    
    "Florencia": [("Neiva", 180), ("Mocoa", 150)],
    
    "Mocoa": [("Florencia", 150), ("Pasto", 300)],
    
    "Pasto": [("Mocoa", 300), ("Popayán", 260)],
    
    "Popayán": [("Pasto", 260), ("Cali", 140)],
    
    "Cali": [("Popayán", 140)],
    
    "Quibdó": [("Medellín", 220)],
    
    # Zonas SIN conexión terrestre directa
    "Leticia": [],
    "Mitú": [],
    "Inírida": [],
    "Puerto Carreño": [],
    "San Andrés": []
}
# -----------------------------------
# 🔍 DFS
# -----------------------------------
def dfs(inicio, objetivo):
    pila = [(inicio, [inicio])]
    visitados = set()

    while pila:
        nodo, camino = pila.pop()

        if nodo == objetivo:
            return camino

        if nodo not in visitados:
            visitados.add(nodo)

            for vecino, _ in grafo.get(nodo, []):
                if vecino not in visitados:
                    pila.append((vecino, camino + [vecino]))

    return []

# -----------------------------------
# 🔍 UCS
# -----------------------------------
def ucs(inicio, objetivo):
    cola = []
    heapq.heappush(cola, (0, inicio, [inicio]))

    costos = {inicio: 0}

    while cola:
        costo, nodo, camino = heapq.heappop(cola)

        if nodo == objetivo:
            return camino

        for vecino, peso in grafo.get(nodo, []):
            nuevo_costo = costo + peso

            if vecino not in costos or nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                heapq.heappush(cola, (nuevo_costo, vecino, camino + [vecino]))

    return []

# -----------------------------------
# 🔍 A*
# -----------------------------------
def heuristica(nodo, objetivo):
    x1, y1 = ciudades[nodo]
    x2, y2 = ciudades[objetivo]
    return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

def astar(inicio, objetivo):
    cola = []
    heapq.heappush(cola, (0, 0, inicio, [inicio]))

    costos = {inicio: 0}

    while cola:
        f, g, nodo, camino = heapq.heappop(cola)

        if nodo == objetivo:
            return camino

        for vecino, peso in grafo.get(nodo, []):
            nuevo_g = g + peso

            if vecino not in costos or nuevo_g < costos[vecino]:
                costos[vecino] = nuevo_g
                h = heuristica(vecino, objetivo)
                heapq.heappush(cola, (nuevo_g + h, nuevo_g, vecino, camino + [vecino]))

    return []

# -----------------------------------
# 🪟 VENTANA
# -----------------------------------
ventana = tk.Tk()
ventana.title("Rutas por Colombia - IA")
ventana.geometry(f"{ANCHO_MAPA + ANCHO_PANEL}x{ALTO_MAPA}")
ventana.resizable(False, False)
ventana.configure(bg="#0f172a")

# PANEL
frame = tk.Frame(ventana, bg="#0f172a", width=ANCHO_PANEL, height=ALTO_MAPA)
frame.pack(side=tk.LEFT, fill=tk.Y)
frame.pack_propagate(False)

tk.Label(frame, text="RUTAS IA", fg="#38bdf8", bg="#0f172a",
         font=("Arial", 16, "bold")).pack(pady=20)

# COMBOS
def combo(lbl, values):
    tk.Label(frame, text=lbl, fg="white", bg="#0f172a").pack()
    c = ttk.Combobox(frame, values=values, state="readonly")
    c.pack(pady=5)
    return c

metodo = combo("Método", ["DFS", "Costo Uniforme", "A*"])
metodo.current(1)

origen = combo("Origen", list(ciudades.keys()))
destino = combo("Destino", list(ciudades.keys()))

resultado = tk.StringVar(value="Seleccione ciudades")

tk.Label(frame, textvariable=resultado, wraplength=220,
         justify="left", fg="#22c55e", bg="#0f172a",
         font=("Consolas", 10)).pack(pady=15)

# CANVAS
canvas = tk.Canvas(ventana, width=ANCHO_MAPA, height=ALTO_MAPA, highlightthickness=0)
canvas.pack(side=tk.RIGHT)

imagen = Image.open("mapa_colombia.jpg")
mapa = ImageTk.PhotoImage(imagen)
canvas.create_image(0, 0, anchor=tk.NW, image=mapa)

# DIBUJAR CIUDADES
for ciudad, (x, y) in ciudades.items():
    canvas.create_oval(x-4, y-4, x+4, y+4, fill="red")
    canvas.create_text(x+8, y, text=ciudad, font=("Arial", 8))

# ANIMACIÓN
def animar(camino, color):
    canvas.delete("ruta")
    for i in range(len(camino)-1):
        x1, y1 = ciudades[camino[i]]
        x2, y2 = ciudades[camino[i+1]]
        canvas.create_line(x1, y1, x2, y2, width=4, fill=color, tags="ruta")
        ventana.update()
        ventana.after(300)

# CALCULAR
def calcular():
    ini = origen.get()
    fin = destino.get()
    met = metodo.get()

    if not ini or not fin:
        resultado.set("Selecciona origen y destino")
        return

    if met == "DFS":
        camino = dfs(ini, fin)
        color = "orange"
    elif met == "Costo Uniforme":
        camino = ucs(ini, fin)
        color = "blue"
    else:
        camino = astar(ini, fin)
        color = "green"

    if not camino:
        resultado.set("No hay ruta")
        return

    texto = ""
    total = 0

    for i in range(len(camino)-1):
        c1 = camino[i]
        c2 = camino[i+1]
        for vecino, peso in grafo[c1]:
            if vecino == c2:
                texto += f"{c1} → {c2}: {peso} km\n"
                total += peso

    texto += f"\nTOTAL: {total} km"
    resultado.set(texto)

    animar(camino, color)

# BOTÓN
tk.Button(frame, text="CALCULAR RUTA",
          bg="#22c55e", fg="white",
          font=("Arial", 11, "bold"),
          command=calcular).pack(pady=20)

ventana.mainloop()