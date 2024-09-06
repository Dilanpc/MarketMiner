"""
    Este archivo es el punto de entrada de la aplicación.
    Redirige la ejecución al módulo MarketMiner/__main__.py
"""

from MarketMiner import __main__ as marketminer
def main():
    return marketminer.main()



if __name__ == "__main__":
    main()