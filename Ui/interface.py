from PySide6.QtWidgets import QWidget, QTabWidget, QHBoxLayout

from .MarketMinerUi import MarketMinerTab




class Interface(QWidget):
    def __init__(self):
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
        self.tabs.addTab(MarketMinerTab(), "Market Miner")
        self.tabs.addTab(QWidget(), "Wiki Miner")


        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tabs)


        self.setLayout(layout)

