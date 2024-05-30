import tkinter as tk
import threading
import webbrowser
import scrape






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

    def show_info(self, page_name):
        self.frame_info = FrameInfoShop(self, page_name)
        self.frame_info.grid(row=0, column=1, sticky="nsew")



class FrameMenuShops(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.label = tk.Label(self, text="Tiendas")
        self.label.pack()
        
        self.buttons = []

        self.info = None

        self.buttons.append(tk.Button(self, text="Mercado libre", command=lambda : master.show_info("MercadoLibre")))

        self._show_buttons()

    def _show_buttons(self):
        for button in self.buttons:
            button.pack()


class FrameInfoShop(tk.Frame):
    def __init__(self, master, page_name):
        super().__init__(master)
        self.master = master
        self.result = None

        self.page = None
        self.__search_web(page_name)

        self.config(bg="gray")
        self.label = tk.Label(self, text=page_name)
        self.label.pack()

        self.search_input = tk.Entry(self)
        self.search_input.pack()

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
        txt = self.search_input.get()
        self.page.clean_up()
        print("Buscando...")
        self.page.search_products(txt)
        self.result = FrameResult(self, self.page.get_dataframe())
        self.result.pack(fill=tk.Y, expand=True)
    
    

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
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor=tk.NW)

        self.buttons = []
        self._calculate_buttons()

        self._show_buttons()

        self.inner_frame.bind('<Configure>', self.__on_frame_configure)
    
    # Actualiza el tamaño del área scrolleable, el 'event' es necesario
    def __on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def _calculate_buttons(self):
        for i in range(len(self.data)):
            button_text = str(self.data["Nombres"][i]) + " $" + str(self.data["Precios"][i])
            button_command = lambda index=i: self._go_to_link(self.data["Links"][index])
            button = tk.Button(self.inner_frame, text=button_text, command=button_command, anchor="w", justify="left")
            self.buttons.append(button)

    def _show_buttons(self):
        for button in self.buttons:
            button.pack(fill="x", expand=True)


    def _go_to_link(self, link):
        webbrowser.open(link)


if __name__ == "__main__":
    interfaz = Interfaz()
    interfaz.mainloop()