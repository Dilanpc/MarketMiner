import tkinter as tk
import threading
from scrape import MercadoLibre, Exito, Linio

# Ventana principal, contiene un FrameHome y un FrameShops
class Interface(tk.Tk):
    windowWidth = 800
    windowHeight = 600

    def __init__(self):
        super().__init__()
        self.title("Comparador de tiendas")
        self.geometry(f"{Interface.windowWidth}x{Interface.windowHeight}")

        # Crear instancia de FrameShops
        self.frameShops = FrameShops(master=self)
        # Crear instancia de FrameHome
        self.header = Header(master=self)

        # Colocar los frames en la ventana
        self.header.pack()
        self.frameShops.pack(expand=True, fill=tk.BOTH)

        
    


# Frame ubicado en la parte superior de la ventana, contiene el cuadro de busqueda
class Header(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.frameShops = master.frameShops # Referencia al FrameShops para poder buscar en las tiendas

        # Crear un cuadro de texto y un botón para buscar
        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text="Buscar", command=lambda : self.__buscar(self.entry.get()))
        self.button.pack()


    def __buscar(self, text): # Llama a la función de búsqueda de FrameShops
        self.frameShops.buscar_en_cada_tienda(text)




# Frame que agrupa los resultados de las tiendas
class FrameShops(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


        # Crear instancias de Shop
        self.shop1 = Shop(master=self, title="Mercado Libre", shop_class=MercadoLibre, bg="yellow")
        self.shop2 = Shop(master=self, title="    Éxito    ", shop_class=Exito, bg="red")
        self.shop3 = Shop(master=self, title="    Linio    ", shop_class=Linio, bg="green")

        # Colocar los Shop en columnas usando grid
        self.shop1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.shop2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.shop3.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

    def buscar_en_cada_tienda(self, text):
        print("buscando en cada tienda", text)

        # Llamar a la función de búsqueda de cada tienda en hilos
        threading.Thread(target=lambda : self.shop1.search(text)).start()
        threading.Thread(target=lambda : self.shop2.search(text)).start()
        threading.Thread(target=lambda : self.shop3.search(text)).start()


# Frame que contiene los resultados de solo una tienda
class Shop(tk.Frame):
    def __init__(self, master, title="Nombre", shop_class=None, **kwargs):
        super().__init__(master, **kwargs)
        self.title = title
        # Crear una instancia de la tienda
        try:
            self.shop = shop_class()
        except Exception as e:
            print(e)
            self.shop = None
            self.title = f"Error al cargar {title}"

        # Título de la tienda
        self.label = tk.Label(self, text=self.title, font=("consolas", 12), bg=self['bg'])
        self.label.pack(fill=tk.X)

        # Frame para mostrar los resultados
        self.results = SearchResult(self)

    def search(self, text): # Se recomienda llamar con un hilo
        if self.shop:
            try:
                self.shop.search_products(text)
                self.shop.print_products()
                print(f"Busqueda en {self.title} completada")
                self.results.pack(fill=tk.BOTH, expand=True)
            except Exception as e:
                print(f"\nERROR AL BUSCAR PRODUCTO EN {self.title}: {e}")
        else:
            print(f"No se puede buscar en {self.title}, self.shop es None")


class SearchResult(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.config(padx=5, pady=5, bg=master['bg'])

        self.scrollbar = tk.Scrollbar(self)




if __name__ == "__main__":
    interface = Interface()
    interface.mainloop()