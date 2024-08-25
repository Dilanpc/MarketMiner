import requests
from bs4 import BeautifulSoup

class WikiPage:
    def __init__(self, url):
        self.url = url
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
    
    def get_title(self):
        return self.soup.title.text
    
    # Método para obtener los párrafos de la página 
    def get_paragraph(self):
        for paragraph in self.soup.select('p'):
            print(paragraph.text)
            
class Wikipedia(WikiPage):
    def __init__(self, url):
        super().__init__(url)
        self.url = url
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
        
    def find_keyword(self, keywords):
        for paragraph in self.soup.select('p'):
            # Comprobar si alguna de las palabras clave está en el texto del párrafo
            for keyword in keywords:
                if keyword in paragraph.text:
                    print(paragraph.text)
                    print("-------------------------------------------------")
                    break 
                
                
if __name__ == "__main__":
    wikipedia_page = Wikipedia('https://es.wikipedia.org/wiki/Lionel_Messi')

    print(wikipedia_page.get_title())

    # Definir la lista de palabras clave a buscar
    keywords = ["Balón de Oro", "Balones de Oro"]

    # Llamar al método para encontrar párrafos que contengan las palabras clave
    wikipedia_page.find_keyword(keywords)
