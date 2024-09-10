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

    def search(self): # enviar la búsqueda a frameShops
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
            self.parent().header.button.setEnabled(True)




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

        # Ecommerce
        self.ecommerce = None
        self._thread = None
        self._loading = False

        # Scroll Area / Results
        self.results = Results(self)

        # Botones
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
        self.results.updateButtons(products)

        self._loading = False
        self.parent().reactivateButton() # Intentar reactivar el botón de búsqueda
    
    
    def print_products(self):
        self.ecommerce.print_products()
    def getProducts(self):
        return self.ecommerce.products
    
    def search_products(self, query): # Buscar productos en un hilo
        self._loading = True
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
        self.setStyleSheet(
            """
            background-color: #444,
            """
        )

        self.buttons = []

        self.widget = QWidget(self)
        self.widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum))
        self.layout = QVBoxLayout(self.widget)
        self.layout.setSpacing(2)


        self.setWidget(self.widget)



    def updateButtons(self, products):
        self.clear()

        # Crear nuevos botones y agregarlos al layout
        for product in products:
            self.buttons.append(ProductButton(self.widget, product))
            self.layout.addWidget(self.buttons[-1])

    def clear(self):
        self.parent().ecommerce.clean_up()
        for button in self.buttons:
            self.layout.removeWidget(button)
            button.deleteLater()  # Elimina los botones antiguos de la interfaz
        self.buttons = []




class ProductButton(QPushButton):
    def __init__(self, parent, product) -> None:
        super().__init__(parent)

        self.setStyleSheet(
            """
            background-color: #444;
            color: white;
            text-align: left;

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

