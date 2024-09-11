from PySide6.QtWidgets import (QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt, QThread, Signal


from MarketMiner.scrape import MercadoLibre, Exito, Linio



class Header(QFrame):
    def __init__(self, parent):    
        super().__init__(parent)
        
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum))
        self.setStyleSheet(
            "background-color: #aaa;"
        )

        # Título
        self.title = QLabel(self)
        self.title.setText("Market Miner")
        self.title.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(
            """color: #222222;
            font-size: 24px;"""
        )

        # Cuadro de búsqueda
        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText("Buscar")
        self.entry.setMaximumWidth(600)
        self.entry.setMinimumWidth(300)
        self.entry.setStyleSheet(
            """border-radius: 5px;
            background-color: #505059;
            padding: 4px 10px;
            
            color: #eee;
            """
        )
        self.entry.returnPressed.connect(self.search)



        # Botón
        self.button = QPushButton(self)
        self.button.setText("Buscar")
        self.button.setMaximumWidth(100)
        self.button.setMinimumWidth(150)
        self.button.setStyleSheet(
            """
            QPushButton {
                color: #eeeeee;

                background-color: #444;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #333;
            }
            """
        )
        self.button.clicked.connect(self.search)



        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.entry, 0, Qt.AlignHCenter)
        layout.addWidget(self.button, 0, Qt.AlignHCenter)

        self.setLayout(layout)

    def search(self): # enviar la búsqueda a frameShops, se ejecuta al presionar el botón o al presionar enter en el cuadro de búsqueda
        self.button.setEnabled(False)
        self.parent().frameShops.search(self.entry.text())

        





class FrameShops(QFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.setStyleSheet(
            """
            background-color: #bbb;
            """
        )


        self.mercadoShop = Shop(self)
        self.exitoShop = Shop(self)
        self.linioShop = Shop(self)

        self.mercadoShop.setTitle("Mercado Libre")
        self.mercadoShop.setEcommerce(MercadoLibre)
        self.exitoShop.setTitle("Exito")
        self.exitoShop.setEcommerce(Exito)
        self.linioShop.setTitle("Linio")
        self.linioShop.setEcommerce(Linio)

        self.shops = [self.mercadoShop, self.exitoShop, self.linioShop]

        # Layout
        layout = QHBoxLayout(self)
        layout.addWidget(self.mercadoShop)
        layout.addWidget(self.exitoShop)
        layout.addWidget(self.linioShop)

    def search(self, query):
        for shop in self.shops:
            shop.search_products(query)
    
    def reactivateButton(self):
        if all((not shop._loading) for shop in self.shops):
            self.parent().searchButtonState(True)




class Shop(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setStyleSheet(
            """
            """
        )

        # Título
        self.title = QLabel(self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(
            """
            color: black;
            font-size: 16px;
            font-weight: bold;
            """
        )

        # Ecommerce
        self.ecommerce = None
        self._loading = False

        # Scroll Area / Results
        self.results = Results(self)
        self.last_query = ""

        # Botones o demás widgets dentro
        self.buttons: list = []

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.results)



    def setTitle(self, title):
        self.title.setText(title)
    def setEcommerce(self, ecommerce):
        self.ecommerce = ecommerce()

    def updateProducts(self, products=None):
        if products is None:
            products = self.ecommerce.products

        
        if len(products) == 0:
            print("No se encontraron productos")
            self.results.noResults()
        else:
            self.results.updateButtons(products)

        self._loading = False
        self.parent().reactivateButton() # Intentar reactivar el botón de búsqueda
    
    
    def print_products(self):
        self.ecommerce.print_products()
    def getProducts(self):
        return self.ecommerce.products
    
    def search_products(self, query): # Buscar productos en un hilo
        self.last_query = query
        self._loading = True
        self.parent().parent().searchButtonState(False)
        self.results.clear()
        self.thread = SearchThread(self, query)
        self.thread.ready.connect(self.updateProducts) # Actualizar interfaz al terminar
        self.thread.start()


    

        

class SearchThread(QThread):
    ready = Signal()
    def __init__(self, parent, query) -> None:
        super().__init__(parent)

        self.query = query

    def run(self):
        self.parent().ecommerce.search_products(self.query)
        self.ready.emit()



class Results(QScrollArea):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Panel)
        self.setStyleSheet("""
        QScrollBar:vertical {
            border: none;
            background: transparent;
            width: 12px;
            margin: 0px 0px 0px 0px;
            padding: 0px 4px;
        }
        QScrollBar::vertical:hover {
            padding: 0px 2px;
        }

        QScrollBar::handle:vertical {
            background: #ccc;
            min-height: 20px;
            border-radius: 2px;
        }
        QScrollBar::handle:vertical:hover {
            border-radius: 4px;
        }
        QScrollBar::handle:vertical:pressed {
            background: #ddd;
        }
                           
                           
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: #aaa;
            }
                           
        QScrollBar:horizontal {
            border: none;
            background: transparent;
            height: 12px;
            margin: 0px 0px 0px 0px;
            padding: 4px 0px;
        }
        QScrollBar::horizontal:hover {
            padding: 2px 0px;
        }
        
        QScrollBar::handle:horizontal {
            background: #ccc;
            min-width: 20px;
            border-radius: 2px;
        }
        QScrollBar::handle:horizontal:hover {
            border-radius: 4px;
        }
        QScrollBar::handle:horizontal:pressed {
            background: #ddd;
        }

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            background: none;
            width: 0px;
        }
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
            background: #aaa;
        }
        """)

        self.buttons = []

        self.widget = QWidget(self)
        self.widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum))
        self.layout = QVBoxLayout(self.widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(5, 5, 5, 5)


        self.setWidget(self.widget)


    # Elimina botones actuales, y crea nuevos botones con los productos
    def updateButtons(self, products):
        self.clear()

        # Crear nuevos botones y agregarlos al layout
        for product in products:
            self.buttons.append(ProductButton(self.widget, product))
            self.layout.addWidget(self.buttons[-1])

    # Limpia layout
    def clear(self):
        self.parent().ecommerce.clean_up()
        for button in self.buttons:
            self.layout.removeWidget(button)
            button.deleteLater()
        self.buttons = []

    def noResults(self):
        self.buttons.append(QLabel(self.widget))
        self.buttons[-1].setText("No se encontraron resultados.\n¿Intentar de nuevo?")
        self.buttons[-1].setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.buttons[-1])

        self.buttons.append(QPushButton(self.widget))
        self.buttons[-1].setText("Reintentar busqueda")
        self.buttons[-1].clicked.connect(lambda: self.parent().search_products(self.parent().last_query))
        self.layout.addWidget(self.buttons[-1])





class ProductButton(QPushButton):
    def __init__(self, parent, product) -> None:
        super().__init__(parent)

        self.setStyleSheet(
            """
            QPushButton {
                color: white;
                text-align: left;
                background-color: #444;
                padding: 8px;
                border-radius: 5px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #555;
                margin: 0;
            }
            QPushButton:pressed {
                background-color: #333;
            }
            """
        )

        self.product = product
        self.setText(product.name + " \n$" + str(product.price))
        self.clicked.connect(self.showProduct)

    def showProduct(self):
        pass



class MarketMinerTab(QWidget):
    def __init__(self, parent = None,) -> None:
        super().__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)

        self.header = Header(self)
        self.frameShops = FrameShops(self)


        # Layout
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.header)
        layout.addWidget(self.frameShops)

        self.setLayout(layout)

    def searchButtonState(self, state: bool):
        self.header.button.setEnabled(state)
