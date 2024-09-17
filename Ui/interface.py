from PySide6.QtWidgets import QApplication, QWidget, QTabWidget, QHBoxLayout

from .MarketMinerUi import MarketMinerTab
from .ReportsUi import ReportsTab




class Interface(QWidget):
    def __init__(self):
        self.app = QApplication([])

        super().__init__()
        self.setWindowTitle("MarketMiner")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(
            """
            background-color: #494950;
            """
        )

        # Tab
        self.tabs = QTabWidget()
        self.tabs.setContentsMargins(0, 0, 0, 0)
        self.tabs.setStyleSheet(
            """
            
            QTabBar::tab {
                background-color: #333;
                color: white;
                padding: 10px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }

            QTabBar::tab:selected {
                background-color: #555;
            }

            QTabWidget::pane {
            }

            """
        )
        self.tab1 = MarketMinerTab(self)
        self.tab2 = ReportsTab(self)
        self.tab3 = QWidget(self)
        self.tabs.addTab(self.tab1, "Market Miner")
        self.tabs.addTab(self.tab2, "Reports")
        self.tabs.addTab(self.tab3, "Wiki Miner")

        self.reportManager = self.tab2.reportManager # referencia al reportManager


        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tabs)


        self.setLayout(layout)

    def exec(self):
        self.show()
        return self.app.exec()