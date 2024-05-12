import csv
try:
    import pandas as pd
except ImportError:
    pass

class Csv():
    def __init__(self, file) -> None:
        self.file: str = file
        self.matrix: list= self.read()


    def read(self, file=None) -> list:
        if file == None: file = self.file

        with open(file, 'r') as archivo_csv:
            lector = csv.reader(archivo_csv)
            return [list(fila) for fila in lector]

    def write(self, data, file=None, update_matrix=True) -> None:
        # Escribe una fila o una matriz en el archivo csv
        # Si el archivo ya tiene contenido, este se sobreescribe
        if file == None: file = self.file

        with open(file, 'w', newline='') as archivo_csv:
            escritor = csv.writer(archivo_csv)
            escritor.writerows(data)
        if update_matrix:
            self.matrix = self.read()

    def add(self, lista, file=None, update_matrix=True) -> None:
        # Agrega una fila o una matriz al final del archivo csv
        if file == None: file = self.file

        if lista == []:
            print('No hay datos para agregar')
            return None
        
        with open(file, 'a', newline='') as archivo_csv:
            escritor = csv.writer(archivo_csv)
            if isinstance(lista[0], list):
                escritor.writerows(lista)
            else:
                escritor.writerow(lista)
        if update_matrix:
            self.matrix = self.read()
        
    def add_column(self, column, file=None) -> None:
        #Añade una columna al archivo csv. La columna debe tener la misma longitud que la cantidad de filas
        if file == None:
            matrix = self.matrix
        else:
            matrix = self.read(file)
        matrix = [fila + [column[i]] for i, fila in enumerate(matrix)]
        self.write(matrix, file)
    
    def get_column(self, index) -> list:
        return [fila[index] for fila in self.matrix]
    
    def get_dataframe(self):
        data = pd.DataFrame(self.matrix[1:], columns=self.matrix[0])
        return data

    def __str__(self) -> str:
        return str(self.matrix)
    
    def __getitem__(self, index) -> list:
        return self.matrix[index]

    def __len__(self) -> int:
        return len(self.matrix)
    
