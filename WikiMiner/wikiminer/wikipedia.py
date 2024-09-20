"""
Módulo que contiene la clase Wikipedia que hereda de WikiPage.
"""

from .wiki_page import WikiPage  # Importa la clase WikiPage del módulo wiki_page

class Wikipedia(WikiPage):
    def __init__(self, url):
        super().__init__(url)  
 
    def find_keyword(self, keywords):
        for paragraph in self.soup.select('p'):  # Selecciona todos los párrafos en la página
            # Comprobar si alguna de las palabras clave está en el texto del párrafo
            for keyword in keywords:
                if keyword in paragraph.text:  # Si se encuentra palabra clave está en el párrafo se imprime el párrafo
                    print(paragraph.text)  
                    print("-------------------------------------------------") 
                    break  # Salir del bucle de palabras clave si se encontró una coincidencia
