
from PySide6.QtWidgets import (QWidget, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout,
    QScrollArea, QLabel, QPushButton, QLineEdit, QComboBox, QSizePolicy, QStackedWidget
)
from PySide6.QtCore import QThread, Signal, Qt

from MarketMiner.reporter import ReportManager
from .grapher import Grapher


class ReportHeader(QWidget):
    def __init__(self, parent, reportsManager, reportList):
        super().__init__(parent)

        self.reportsManager = reportsManager # Referencia al reportManager
        self.reportList = reportList # Referencia a la lista de reportes

        # Título
        self.title = QLabel("Reportes")
        self.title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 10px 10px 10px 0px;
            """)

        # Edición de reporte
        self.nameEntry = QLineEdit(self)
        self.nameEntry.setPlaceholderText("Nombre")
        self.nameEntry.setStyleSheet("""
            background-color: #aaa;
            color: black;
            border-radius: 8px;
            padding: 5px;
            """)

        self.queryEntry = QLineEdit(self)
        self.queryEntry.setPlaceholderText("Búsqueda")
        self.queryEntry.setStyleSheet("""
            background-color: #aaa;
            color: black;
            border-radius: 8px;
            padding: 5px;
            """)
        
        self.classEntry = QComboBox(self)
        self.classEntry.addItems(["MercadoLibre", "Exito", "Linio"])
        self.classEntry.setStyleSheet("""
            background-color: #aaa;
            color: black;
            border-radius: 8px;
            padding: 5px;
            """)
        
        

        # Botón Añadir
        self.addBtn = QPushButton("Añadir")
        self.addBtn.setStyleSheet("""
            QPushButton {
                background-color: #999;
                color: Black;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #bbb;
            }
            QPushButton:pressed {
                background-color: #888;
            }
            """)
        self.addBtn.clicked.connect(self.addReport)



        layout = QGridLayout(self)
        layout.addWidget(self.title, 0, 0, 2, 1)
        layout.addWidget(self.nameEntry, 0, 1, 1, 1)
        layout.addWidget(self.queryEntry, 0, 2, 1, 1)
        layout.addWidget(self.classEntry, 1, 1, 1, 1)
        layout.addWidget(self.addBtn, 0, 3, 2, 1)


    def addReport(self):
        name = self.nameEntry.text()
        query = self.queryEntry.text()
        class_ = self.classEntry.currentText()
        if (name == "") or (query == ""):
            return
        
        # Añadir reporte en arhivo json
        data = {
            "name": name,
            "class": class_,
            "reportPath": f"./userReports/{name}.csv",
            "query": query,
            "product": None
        }
        self.reportsManager.add(data) # Añade el reporte al archivo json
        self.nameEntry.clear()
        self.queryEntry.clear()

        # Actualizar lista de reportes
        self.reportList.addCard(self.reportsManager.reports[-1]) # Añade el reporte a la lista de reportes



class ReportList(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("""
            border-radius: 8px;
            background-color: #595960;
            """)
        self.setFrameShape(QFrame.StyledPanel)
        self.setWidgetResizable(True)
        
        self.widget = QWidget(self)
        self.widget.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum))
        self.widget.setStyleSheet("""
            """)



        self.cards = []

        self.layout = QVBoxLayout(self.widget)
        self.layout.setSpacing(2)
        self.setWidget(self.widget)
    
    def updateCards(self, reports:list):
        self.clear()
        for i in range(len(reports)-1, -1, -1): # Recorrer del más reciente al más antiguo
            self.cards.append(ReportCard(self.widget, reports[i]))
            self.layout.addWidget(self.cards[-1])
    
    def addCard(self, report):
        card = ReportCard(self.widget, report)
        self.cards.insert(0, card) # Agragar al principio
        self.layout.insertWidget(0, card)


    def clear(self):
        for card in self.cards:
            self.layout.removeWidget(card)
            card.deleteLater()
        self.cards = []





class ReportCard(QFrame):
    def __init__(self, parent, report):
        super().__init__(parent)
        self.reportUi = parent.parent().parent().parent().parent() #Referencia la pestana de reportes

        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        self.setStyleSheet("""
        QFrame {
            background-color: #333;
            border-radius: 8px;
            padding: 2px;
            margin: 5px;
        }
        """
        )

        self.report = report

        self.title = QLabel(self)
        self.title.setText(report['name'])
        self.title.setWordWrap(True)
        self.title.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            background-color: #555;
            margin: 5px;
        """)

        self.query = QLabel(self)
        self.query.setText(report['query'])
        self.query.setStyleSheet("""
            color: white;
            font-size: 14px;
            background-color: #555;
            margin: 5px;
        """)

        self.class_ = QLabel(self)
        self.class_.setText(report['class'])
        self.class_.setStyleSheet("""
            color: white;
            font-size: 14px;
            background-color: #555;
            margin: 5px;
        """)

        self.path = QLabel(self)
        self.path.setText(report['reportPath'])
        self.path.setStyleSheet("""
            color: white;
            font-size: 12px;
            background-color: #555;
            margin: 5px;
        """)


        self.startbtn = QPushButton(self)
        self.startbtn.setText("Iniciar")
        self.startbtn.setStyleSheet("""
            QPushButton {
                background-color: #999;
                color: Black;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #bbb;
            }
            QPushButton:pressed {
                background-color: #888;
            }
            """)
        self.startbtn.clicked.connect(self.run)

        self.infobtn = QPushButton(self)
        self.infobtn.setText("Más info")
        self.infobtn.setStyleSheet("""
            QPushButton {
                background-color: #999;
                color: Black;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #bbb;
            }
            QPushButton:pressed {
                background-color: #888;
            }
            """)
        self.infobtn.clicked.connect(self.showInfo)
        


        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.title, 0, 0, 2, 1)

        self.layout.addWidget(self.query, 0, 1, 1, 1)
        self.layout.addWidget(self.path, 1, 1, 1, 2)

        self.layout.addWidget(self.class_, 0, 2, 1, 1)

        self.layout.addWidget(self.startbtn, 0, 3, 1, 1)
        self.layout.addWidget(self.infobtn, 1, 3, 1, 1)

    def run(self):
        self.startbtn.setEnabled(False)
        self.reportThread = ReportThread(self.report)
        self.reportThread.ready.connect(self.reportFinished)
        self.reportThread.start()

    def reportFinished(self, success):
        self.startbtn.setEnabled(True)
        self.reportThread.deleteLater()

    def showInfo(self):
        self.reportUi.info.set_report(self.report)
        self.reportUi.setCurrentIndex(1)



class ReportThread(QThread):
    ready = Signal(bool)
    def __init__(self, report):
        super().__init__()
        self.report = report

    def run(self):
        try:
            self.report.run()
            self.ready.emit(True)
        except Exception as e:
            print(f"Error en reporte de {self.report['name']}: {e}")
            self.ready.emit(False)


class ReportInfo(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.reportUi = parent # Referencia a la pestaña de reportes

        self.setStyleSheet("""
            background-color: #aaa;
            margin-left: 70px;
            position: absolute;

            """)


        self.report = None

        self.closebtn = QPushButton(self)
        self.closebtn.setText("X")
        self.closebtn.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 20px;
                background-color: #655;
                border-radius: 5px;
                margin: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #780b0b;
            }
            QPushButton:pressed {
                background-color: #433;
            }
            """)
        self.closebtn.clicked.connect(self.reportUi.hideReportInfo)

        self.title = QLabel(self)
        self.title.setWordWrap(True)
        self.title.setStyleSheet("""
            color: black;
            font-size: 24px;
            font-weight: bold;
            """)

        self.query = QLabel(self)
        self.query.setWordWrap(True)
        self.query.setStyleSheet("""
            color: black;
            font-size: 18px;
            """)

        self.list = ReportInfoList(self)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.closebtn, 0, 0, 1, 1)

        self.layout.addWidget(self.title, 0, 1, 1, 1)
        self.layout.addWidget(self.query, 1, 1, 1, 1)
        self.layout.addWidget(self.list, 2, 1, 1, 1)

        self.layout.setColumnStretch(0, 0)
        self.layout.setColumnStretch(1, 1)


    def set_report(self, report):
        self.report = report
        self.title.setText(report['name'])
        self.query.setText('Búsqueda: ' + report['query'])
        self.list.load_data(report['reportPath'])
        
    

    

class ReportInfoList(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWidgetResizable(True)
        self.setStyleSheet("""
            background-color: #aaa;
            border-radius: 8px;
            padding: 2px;
            """)

        self.data = None

        self.widget = QWidget(self)
        self.layout = QVBoxLayout(self.widget)
        self.setWidget(self.widget)

        self.cards = []

    # Lee un archivo csv, lo guarda como una matriz y actualiza las tarjetas
    def load_data(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            self.data = file.readlines() # Separar por lineas
        self.data = [line.strip().split(',') for line in self.data] # Separar por comas
        self.updateCards()

    def updateCards(self):
        self.clear()
        dates = self.data[0]
        for row in self.data[1:]:
            self.cards.append(ReportInfoCard(self.widget, dates, row))
            self.layout.addWidget(self.cards[-1])

    # Quita elementos del scrollArea
    def clear(self):
        for card in self.cards:
            self.layout.removeWidget(card)
            card.deleteLater()
        self.cards = []


class ReportInfoCard(QFrame):
    def __init__(self, parent, dates:list, data:list):
        super().__init__(parent)
        self.name = data[0]
        self.dates = dates[1:]
        try:
            self.data = [float(txt) for txt in data[1:]]
        except:
            self.data =['N/A' for txt in data[1:]]

        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        self.setStyleSheet("""
            QFrame {
                background-color: #333;
                border-radius: 8px;
                padding: 2px;
                margin: 5px;
            }
            """)


        self.nameLabel = QLabel(self)
        self.nameLabel.setText(self.name)
        self.nameLabel.setMaximumWidth(600)
        self.nameLabel.setWordWrap(True)
        self.nameLabel.setAlignment(Qt.AlignLeft)
        self.nameLabel.setStyleSheet("""
            color: white;
            font-size: 16px;
            background-color: #444;
            """)

        self.showbtn = QPushButton(self)
        self.showbtn.setText("Mostrar")
        self.showbtn.setFixedWidth(300)
        self.showbtn.setStyleSheet("""
            QPushButton {
                background-color: #999;
                color: Black;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #bbb;
            }
            QPushButton:pressed {
                background-color: #888;
            }
            """)
        self.showbtn.clicked.connect(self._graph)
        

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.showbtn)

    def _graph(self):
        graph = Grapher(self.data, self.dates)
        graph.graph(label=self.name)
        graph.show(block=False)

        
        


class ReportsTab(QStackedWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.reportManager = ReportManager('reportingData.json', 'userReports')

        self.mainWidget = QWidget(self)


        self.reportList = ReportList(self.mainWidget)
        self.header = ReportHeader(self.mainWidget, self.reportManager, self.reportList)

        self.info = ReportInfo(self)

        self.reportList.updateCards(self.reportManager.reports)


        mainLayout = QVBoxLayout(self.mainWidget)
        mainLayout.addWidget(self.header)
        mainLayout.addWidget(self.reportList)

        self.addWidget(self.mainWidget)
        self.addWidget(self.info)
        
    def hideReportInfo(self):
        self.setCurrentIndex(0)