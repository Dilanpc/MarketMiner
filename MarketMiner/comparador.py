import tkinter as tk
import threading
import webbrowser
from MarketMiner.scrape import MercadoLibre, Exito, Linio

# Ventana principal, contiene un FrameHome y un FrameShops
class Interface(tk.Tk):
    windowWidth = 1300
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
        self.frameShops.search_in_shops(text)




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

    def search_in_shops(self, text):
        print("buscando en cada tienda", text)

        # Llamar a la función de búsqueda de cada tienda en hilos
        threads = []
        threads.append(threading.Thread(target=lambda : self.shop1.search(text)))
        threads.append(threading.Thread(target=lambda : self.shop2.search(text)))
        threads.append(threading.Thread(target=lambda : self.shop3.search(text)))
        for t in threads:
            t.start()

        # Esperar a que los hilos terminen
        threading.Thread(target=lambda : self.__wait_for_search(threads)).start()

    # Muestra la información de cada tienda cuando estén todas las búsquedas completadas
    def __wait_for_search(self, threads):
        for t in threads:
            t.join()

        for shop in [self.shop1, self.shop2, self.shop3]:
            shop.show_info()
        


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
                self.clean_results()
                self.shop.search_products(text)
                print(f"Busqueda en {self.title} completada")
            except Exception as e:
                print(f"\nERROR AL BUSCAR PRODUCTO EN {self.title}: {e}")
        else:
            print(f"No se puede buscar en {self.title}, self.shop es None")

    def show_info(self):
        self.results.add_buttons(self.shop.products)
        self.results.pack(fill=tk.BOTH, expand=True)

    def clean_results(self):
        self.results.pack_forget()
        self.results.clean_buttons()
        self.shop.clean_up()




# Lista de los productos encontrados
class SearchResult(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.config(padx=5, pady=5, bg=master['bg'])

        self.data = []
        self.buttons = []

        # Crear Canvas y Scrollbar
        self.__create_canvas_scrollbar()
        

    def __create_canvas_scrollbar(self):
        # Crear Canvas y Scrollbar
        self.canvas = tk.Canvas(self, bg=self['bg'])
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")

        # Configurar el canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Frame interno para colocar los resultados
        self.inner_frame = tk.Frame(self.canvas, bg=self['bg'])
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def add_buttons(self, products: list):
        self.data += products
        for i in range(len(self.data) - len(self.buttons)):
            self.buttons.append(tk.Button(
                self.inner_frame,
                anchor="w",
                text=self.data[i].name + "  $" + str(self.data[i].price),
                command=lambda link=self.data[i].link : self._go_to_link(link))
                )

        for button, i in zip(self.buttons, range(len(self.buttons))):
            button.grid(row=i, column=0, sticky="ew")

    def clean_buttons(self):
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        self.data = []

    def _go_to_link(self, link):
        webbrowser.open(link)

if __name__ == "__main__":
    interface = Interface()
    interface.mainloop()