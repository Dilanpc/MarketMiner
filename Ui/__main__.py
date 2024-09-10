import sys

from Ui.interface import Interface

from PySide6.QtWidgets import QApplication



def main():
    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()