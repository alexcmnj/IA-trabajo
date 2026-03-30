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
# 📏 ESCALA
# -----------------------------------
ESCALA_KM = 1200 / ANCHO_MAPA

# -----------------------------------
# 📍 CIUDADES
# -----------------------------------
ciudades = {

    "Bogotá": (250, 350),

    "Medellín": (172, 270),

    "Cali": (129, 400),

    "Barranquilla": (203, 70),

    "Cartagena": (176, 91),

    "Santa Marta": (233, 65),

    "Riohacha": (300, 50),

    "Valledupar": (273, 97),

    "Montería": (160, 171),

    "Sincelejo": (185, 150),

    "Bucaramanga": (280, 243),

    "Cúcuta": (300, 210),

    "Tunja": (263, 310),

    "Villavicencio": (255, 369),

    "Yopal": (309, 319),

    "Arauca": (380, 248),

    "Ibagué": (185, 360),

    "Neiva": (179, 420),

    "Florencia": (172, 480),

    "Pasto": (95, 495),

    "Popayán": (126, 450),

    "Quibdó": (120, 300),

    "Pereira": (210, 350),

    "Manizales": (174, 320),

    "Armenia": (168, 353),

    "Leticia": (415, 720),

    "Mitú": (400, 498),

    "Puerto Carreño": (515, 288),

    "San José del Guaviare": (315, 435),

    "Inírida": (500, 388),

    "Mocoa": (120, 495),

    "San Andrés": (85, 70)

}


# -----------------------------------
# 🔗 GRAFO
# -----------------------------------
grafo = {
    "Bogotá": [("Ibagué", 195), ("Villavicencio", 120), ("Tunja", 141)],
    "Ibagué": [("Bogotá", 195), ("Cali", 265), ("Armenia", 80), ("Neiva", 210)],
    "Armenia": [("Ibagué", 80), ("Pereira", 45)],
    "Pereira": [("Armenia", 45), ("Manizales", 50), ("Medellín", 215)],
    "Manizales": [("Pereira", 50)],
    "Medellín": [("Pereira", 215), ("Montería", 400), ("Quibdó", 220)],
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
    "Villavicencio": [("Bogotá", 120), ("Yopal", 270), ("San José del Guaviare", 300)],
    "Yopal": [("Villavicencio", 270), ("Arauca", 430)],
    "Arauca": [("Yopal", 430)],
    "Neiva": [("Ibagué", 210), ("Florencia", 180)],
    "Florencia": [("Neiva", 180), ("Mocoa", 150)],
    "Mocoa": [("Florencia", 150), ("Pasto", 300)],
    "Pasto": [("Mocoa", 300), ("Popayán", 260)],
    "Popayán": [("Pasto", 260), ("Cali", 140)],
    "Cali": [("Popayán", 140), ("Ibagué", 265)],
    "Quibdó": [("Medellín", 220)],

    "San José del Guaviare": [("Villavicencio", 300), ("Inírida", 400)],
    "Inírida": [("San José del Guaviare", 400), ("Mitú", 350)],
    "Mitú": [("Inírida", 350), ("Leticia", 600)],
    "Leticia": [("Mitú", 600)],

    "Puerto Carreño": [],
    "San Andrés": []
}


# -----------------------------------
# 🔍 ALGORITMOS
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
                pila.append((vecino, camino + [vecino]))
    return []

def ucs(inicio, objetivo):
    cola = [(0, inicio, [inicio])]
    costos = {inicio: 0}
    while cola:
        costo, nodo, camino = heapq.heappop(cola)
        if nodo == objetivo:
            return camino
        for vecino, peso in grafo.get(nodo, []):
            nuevo = costo + peso
            if vecino not in costos or nuevo < costos[vecino]:
                costos[vecino] = nuevo
                heapq.heappush(cola, (nuevo, vecino, camino + [vecino]))
    return []

def heuristica(nodo, objetivo):
    x1, y1 = ciudades[nodo]
    x2, y2 = ciudades[objetivo]
    dist_px = ((x1-x2)**2 + (y1-y2)**2)**0.5
    return round(dist_px * ESCALA_KM)

def astar(inicio, objetivo):
    cola = [(0, 0, inicio, [inicio])]
    costos = {inicio: 0}
    visitados = set()

    while cola:
        f, g, nodo, camino = heapq.heappop(cola)

        if nodo in visitados:
            continue
        visitados.add(nodo)

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
# 🪟 INTERFAZ BONITA
# -----------------------------------
ventana = tk.Tk()
ventana.title("Rutas por Colombia - IA")
ventana.geometry(f"{ANCHO_MAPA + ANCHO_PANEL}x{ALTO_MAPA}")
ventana.resizable(False, False)
ventana.configure(bg="#0f172a")

frame = tk.Frame(ventana, bg="#0f172a", width=ANCHO_PANEL)
frame.pack(side=tk.LEFT, fill=tk.Y)
frame.pack_propagate(False)

tk.Label(frame, text="RUTAS IA", fg="#38bdf8",
         bg="#0f172a", font=("Arial", 18, "bold")).pack(pady=20)

def combo(lbl, values):
    tk.Label(frame, text=lbl, fg="white",
             bg="#0f172a", font=("Arial", 10, "bold")).pack()
    c = ttk.Combobox(frame, values=values, state="readonly")
    c.pack(pady=6)
    return c

metodo = combo("Método", ["DFS", "Costo Uniforme", "A*"])
metodo.current(1)

origen = combo("Origen", list(ciudades.keys()))
destino = combo("Destino", list(ciudades.keys()))

resultado = tk.StringVar(value="Seleccione ciudades")

tk.Label(frame, textvariable=resultado,
         fg="#22c55e", bg="#0f172a",
         font=("Consolas", 10), wraplength=220,
         justify="left").pack(pady=15)

# -----------------------------------
# 🗺️ MAPA
# -----------------------------------
canvas = tk.Canvas(ventana, width=ANCHO_MAPA, height=ALTO_MAPA, highlightthickness=0)
canvas.pack(side=tk.RIGHT)

imagen = Image.open("mapa_colombia.jpg")
imagen = imagen.resize((ANCHO_MAPA, ALTO_MAPA))
mapa = ImageTk.PhotoImage(imagen)

canvas.create_image(0, 0, anchor=tk.NW, image=mapa)

puntos = {}

for ciudad, (x, y) in ciudades.items():
    punto = canvas.create_oval(
        x-4, y-4, x+4, y+4,
        fill="red",
        outline="black"
    )
    
    puntos[ciudad] = punto

    canvas.create_text(
        x - 10,
        y,
        text=ciudad,
        anchor="s",
        font=("Arial", 9, "bold"),
        fill="black"
    )

def actualizar_colores():
    # resetear todos a rojo
    for ciudad in puntos:
        canvas.itemconfig(puntos[ciudad], fill="red")

    # origen en verde
    if origen.get():
        canvas.itemconfig(puntos[origen.get()], fill="green")

    # destino en azul
    if destino.get():
        canvas.itemconfig(puntos[destino.get()], fill="blue")

origen.bind("<<ComboboxSelected>>", lambda e: actualizar_colores())
destino.bind("<<ComboboxSelected>>", lambda e: actualizar_colores())

# -----------------------------------
# 🎬 ANIMACIÓN
# -----------------------------------
def animar(camino, color, i=0):
    if i >= len(camino)-1:
        return

    x1, y1 = ciudades[camino[i]]
    x2, y2 = ciudades[camino[i+1]]

    canvas.create_line(x1, y1, x2, y2,
                       width=4, fill=color, tags="ruta")

    ventana.after(300, lambda: animar(camino, color, i+1))

# -----------------------------------
# CALCULAR
# -----------------------------------
def calcular():
    canvas.delete("ruta")

    ini = origen.get()
    fin = destino.get()

    if not ini or not fin:
        resultado.set("Seleccione ciudades")
        return

    if metodo.get() == "DFS":
        camino = dfs(ini, fin)
        color = "orange"
    elif metodo.get() == "Costo Uniforme":
        camino = ucs(ini, fin)
        color = "blue"
    else:
        camino = astar(ini, fin)
        color = "green"

    if not camino:
        resultado.set("No hay ruta")
        return

    total = 0
    texto = ""

    for i in range(len(camino)-1):
        c1, c2 = camino[i], camino[i+1]
        for v, p in grafo[c1]:
            if v == c2:
                texto += f"{c1} → {c2}: {p} km\n"
                total += p

    texto += f"\nTOTAL: {total} km"
    resultado.set(texto)

    animar(camino, color)

# BOTÓN
tk.Button(frame, text="CALCULAR RUTA",
          bg="#22c55e", fg="white",
          font=("Arial", 11, "bold"),
          relief="flat",
          command=calcular).pack(pady=20)

ventana.mainloop()