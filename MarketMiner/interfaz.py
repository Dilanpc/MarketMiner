import tkinter as tk
import threading
import time
import webbrowser
import MarketMiner.scrape as scrape






class Interfaz(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Comparador de tiendas")
        self.geometry("800x600")
        self.frame = FrameHome(self)
        self.frame.pack(fill="both", expand=True)



class FrameHome(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.frame_menu = FrameMenuShops(self)
        self.frame_menu.config(bg="white")
        self.frame_menu.grid(row=0, column=0, sticky="nsew")

        self.frame_info = tk.Frame(self)

    def show_info(self, page_name, color="white"):
        self.frame_info.destroy()
        self.frame_info = FrameInfoShop(self, page_name, color)
        self.frame_info.grid(row=0, column=1, sticky="nsew")



class FrameMenuShops(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.label = tk.Label(self, text="Tiendas")
        self.label.pack()
        
        self.buttons = []

        self.info = None

        self.buttons.append(tk.Button(self, text="Mercado libre", command=lambda : master.show_info("MercadoLibre", "yellow")))
        self.buttons.append(tk.Button(self, text="Exito", command=lambda : master.show_info("Exito", "yellow")))
        self.buttons.append(tk.Button(self, text="Linio", command=lambda : master.show_info("Linio", "#e4334a")))

        self._show_buttons()

    def _show_buttons(self):
        for button in self.buttons:
            button.pack()


class FrameInfoShop(tk.Frame):
    def __init__(self, master, page_name, color):
        super().__init__(master)
        self.master = master
        self.result = None

        self.__BG = color

        self.page = None
        self.__search_web(page_name)

        self.config(bg = self.__BG)
        self.label = tk.Label(self, text=page_name, bg=self.__BG)
        self.label.pack()

        self.search_input = tk.Entry(self)
        self.search_input.pack()

        self.load_label = tk.Label(self, bg=self.__BG)

        self.button_search = tk.Button(self, text="Buscar", command=self.search)
        self.button_search.pack()

    def __search_web(self, class_name):
        class_ = getattr(scrape, class_name)
        self.page = class_()

    def search(self):
        if self.result != None:
            self.result.destroy()
            del self.result
        # Continuar función en un hilo
        t = threading.Thread(target=self.__search_thread)
        t.start()

    def __search_thread(self): # función que se ejecuta en un hilo para no detener mainloop
        self.__finished = False
        loading_thread = threading.Thread(target=self.__loading)
        loading_thread.start()
        txt = self.search_input.get()
        self.page.clean_up()
        print("Buscando...")
        self.page.search_products(txt)
        self.__finished = True
        self.result = FrameResult(self, self.page.get_dataframe())
        self.result.pack(fill=tk.BOTH, padx=10, expand=True)
    
    def __loading(self):
        self.load_label.pack()
        while not self.__finished:
            self.load_label.config(text="Cargando")
            time.sleep(0.4)
            if self.__finished:
                break
            self.load_label.config(text="Cargando.")
            time.sleep(0.4)
            if self.__finished:
                break
            self.load_label.config(text="Cargando..")
            time.sleep(0.4)
            if self.__finished:
                break
            self.load_label.config(text="Cargando...")
            time.sleep(0.4)
        self.load_label.pack_forget()
    
    

class FrameResult(tk.Frame):
    def __init__(self, master, data): # 'data' es un dataframe de pandas
        super().__init__(master)
        self.master = master
        self.data = data

        self.label = tk.Label(self, text="Resultados de busqueda")
        self.label.pack()

        #Objeto canvas, para que se pueda scrollear
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # En inner_frame se colocarán los elementos para scrollear (está dento del canvas)
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)

        self.buttons = []
        self._calculate_buttons()

        self._show_buttons()

        self.inner_frame.bind('<Configure>', self.__on_frame_configure)
        self.canvas.bind('<Configure>', self.__on_canvas_configure)
    
    # Actualiza el tamaño del área scrolleable, el 'event' es necesario
    def __on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    # Actualiza el ancho del frame dentro del canvas
    def __on_canvas_configure(self, event=None):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)


    def _calculate_buttons(self):
        for i in range(len(self.data)):
            button_text = str(self.data["Nombres"][i]) + " $" + str(self.data["Precios"][i])
            button_command = lambda index=i: self._go_to_link(self.data["Links"][index])
            button = tk.Button(self.inner_frame, text=button_text, command=button_command, anchor="w", justify="left")
            self.buttons.append(button)

    def _show_buttons(self):
        for button in self.buttons:
            button.pack(fill=tk.X, expand=True, padx=10, pady=1)
        self.__on_frame_configure()


    def _go_to_link(self, link):
        webbrowser.open(link)


if __name__ == "__main__":
    interfaz = Interfaz()
    interfaz.mainloop()