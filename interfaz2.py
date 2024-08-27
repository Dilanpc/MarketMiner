import tkinter as tk
import threading
import time
import webbrowser
import scrape

# Ventana principal, contiene un FrameHome y un FrameShops
class Interface(tk.Tk):
    windowWidth = 800
    windowHeight = 600

    def __init__(self):
        super().__init__()
        self.title("Comparador de tiendas")
        self.geometry(f"{Interface.windowWidth}x{Interface.windowHeight}")

        # Crear instancia de FrameHome
        self.frameTitle = FrameTitle(master=self)
        self.frameTitle.pack()

        # Crear instancia de FrameShops
        self.frameShops = FrameShops(master=self)
        self.frameShops.pack(expand=True, fill=tk.BOTH)


# Frame ubicado en la parte superior de la ventana, contiene el cuadro de busqueda
class FrameTitle(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        # Crear un cuadro de texto y un botón para buscar
        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text="Buscar", command=lambda : self.__buscar(self.entry.get()))
        self.button.pack()


    def __buscar(self, text):
        print("buscar", text)



# Frame que agrupa los resultados de las tiendas
class FrameShops(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)


        # Crear instancias de FrameResults
        self.shop1 = FrameResults(master=self, bg="yellow")
        self.shop2 = FrameResults(master=self, bg="red")
        self.shop3 = FrameResults(master=self, bg="green")

        # Colocar los FrameResults usando grid
        self.shop1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.shop2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.shop3.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)



# Frame que contiene los resultados de solo una tienda
class FrameResults(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.config(width=Interface.windowWidth/3, height=Interface.windowHeight-100)

        self.label = tk.Label(self, text="Tienda 1", bg=self['bg'])
        self.label.pack()


if __name__ == "__main__":
    interface = Interface()
    interface.mainloop()