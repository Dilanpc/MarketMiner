"""
Módulo que contiene la clase WikiPage e importa las bibliotecas necesarias.

"""

import requests  # Importa la biblioteca requests para realizar peticiones HTTP
from bs4 import BeautifulSoup  # Importa BeautifulSoup para el análisis de HTML

# Clase Padre que representa una página tipo Wiki y define atributos y métodos comunes
class WikiPage:
    def __init__(self, url):  # Constructor que inicializa la URL y realiza la petición a la página
        self.url = url  # Asignar la URL proporcionada a la instancia
        self.page = requests.get(url)  # Hacer la solicitud HTTP para obtener el contenido de la página
        # Parsear el contenido HTML de la página utilizando BeautifulSoup
        self.soup = BeautifulSoup(self.page.text, 'html.parser') 
    
    # Método que obtiene el título de la página web    
    def get_title(self):
        return self.soup.title.text  # Retorna el texto del título de la página
    