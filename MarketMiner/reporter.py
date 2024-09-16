import json

import MarketMiner.scrape as scrape


""" Guarda y lee archivos json para ejecutar reports de
según los datos del archivo json
"""
class ReportsManager:
    def __init__(self, ruta:str):
        self.ruta = ruta # Ruta del archivo json
        self.data:list[dict] = None # Datos del archivo json
        self.reports:list[Report] = []
        self.read()
    

    def read(self):
        try:
            with open(self.ruta, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
            self._update_reports()
            return self.data
        except FileNotFoundError:
            print("Creando archivo")
            with open(self.ruta, 'w', encoding='utf-8') as file:
                json.dump([], file, indent=4)
            return None

        except Exception as e:
            print(f'Error al leer el archivo: {e}')
            return None

    def write(self, data:list[dict], update=True):
        try:
            with open(self.ruta, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            if update:
                self.data = data
                self._update_reports()
            return True
        except Exception as e:
            print(f'Error al escribir el archivo: {e}')
            return False
        
    def _update_reports(self):
        self.reports = []
        for item in self.data:
            self.reports.append(Report(item))
    
    def add(self, data):
        self.data.append(data)
        self.write(self.data, update=False)
        self._update_reports()

    def clear_file(self):
        self.write([])
        self.data = []
        self.reports = []

    def run(self):
        # se pueden implementar hilos para ejecutar los reportes más rápido
        for report in self.reports:
            report.run()
            
        
    def __getitem__(self, index:int):
        return self.reports[index]
    def get(self, index:int, key:str=None):
        if key:
            return self.reports[index][key]
        return self.reports[index]


    def print(self):
        print(json.dumps(self.data, indent=4))



class Report:
    def __init__(self, data:dict):
        self.data = data
        self.ecommerce = None
        self.set_data(data)

    # Actualiza los datos del reporte, si no se ingresan los datos, se reutilizan los datos anteriores
    def set_data(self, data:dict=None):
        self.data = data
        self.compute()

    def compute(self):
        self.set_ecommerce()
        self.query = self.data['query']
        self.product = self.data['product']
        self.reportPath = self.data['reportPath']

        
    def set_ecommerce(self):
        try:
            self.ecommerce = getattr(scrape, self.data['clase'])() # Instancia de la clase

        except Exception as e:
            print(f'Error al crear el ecommerce: {e}')
            return False
    
    def run(self):
        if self.query:
            self.ecommerce.search_products(self.query)
        elif self.product:
            self.ecommerce.get_product_by_link(self.product)
        else:
            print("No hay datos para ejecutar el reporte")
            return False
        self.ecommerce.make_report(self.reportPath)
        self.ecommerce.clean_up()
        return True
        
    def __getitem__(self, key:str):
        return self.data[key]