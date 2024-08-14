import tkinter as tk
import threading
import time
import webbrowser
import scrape

windowWidth = 800
windowHeight = 600

class Interfaz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Comparador de tiendas")
        self.geometry(f"{windowWidth}x{windowHeight}")
        self.frameTitle = FrameTitle()
        self.frameTitle.pack()
        self.frameShops = FrameShops()
        self.frameShops.pack(expand=True, fill=tk.BOTH)


class FrameTitle(tk.Frame):
    def __init__(self):
        super().__init__()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text="Buscar", command=lambda : self.__buscar(self.entry.get()))
        self.button.pack()





    def __buscar(self, text):
        print("buscar")




class FrameShops(tk.Frame):
    def __init__(self):
        super().__init__()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Crear instancias de FrameResults
        self.shop1 = FrameResults(self, bg="yellow")
        self.shop2 = FrameResults(self, bg="red")
        self.shop3 = FrameResults(self, bg="green")

        # Colocar los FrameResults usando grid
        self.shop1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.shop2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.shop3.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        # Asegurarse de que las columnas y filas se expandan
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)




class FrameResults(tk.Frame):
    def __init__(self, bg):
        super().__init__()

        self.config(bg=bg, width=windowWidth/3, height=windowHeight-100)

        self.label = tk.Label(self, text="Tienda 1", bg=bg)
        self.label.pack()


