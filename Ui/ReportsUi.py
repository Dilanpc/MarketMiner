
from PySide6.QtWidgets import (QWidget, QFrame, QVBoxLayout, QGridLayout, QScrollArea, QLabel,
QPushButton, QLineEdit, QComboBox, QSizePolicy
)
from PySide6.QtCore import QThread, Signal

from MarketMiner.reporter import ReportManager


import time

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


        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.title, 0, 0, 2, 1)
        self.layout.addWidget(self.query, 0, 1, 1, 1)
        self.layout.addWidget(self.class_, 0, 2, 1, 1)
        self.layout.addWidget(self.path, 1, 1, 1, 2)

        self.layout.addWidget(self.startbtn, 0, 3, 2, 1)

    def run(self):
        self.startbtn.setEnabled(False)
        self.reportThread = ReportThread(self.report)
        self.reportThread.ready.connect(self.reportFinished)
        self.reportThread.start()

    def reportFinished(self, success):
        self.startbtn.setEnabled(True)
        self.reportThread.deleteLater()


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



class ReportsTab(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.reportManager = ReportManager('reportingData.json', 'userReports')


        self.reportList = ReportList(self)
        self.header = ReportHeader(self, self.reportManager, self.reportList)

        self.reportList.updateCards(self.reportManager.reports)


        layout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.reportList)