import requests  
from bs4 import BeautifulSoup  

from .wikipedia import Wikipedia  # Importa la clase WikiPage del módulo wiki_page

class WikiMovie(Wikipedia):
    def __init__(self, url):
        super().__init__(url)  # Inicializa la clase base
        
    def get_title(self):
        title_element = self.soup.find('th', class_='cabecera cine')
        return title_element.get_text(strip=True) if title_element else None
    
    def get_director(self):
        director_element = self.soup.find('th', string='Dirección')  # Cambiar 'text' por 'string'
        if director_element:
            return director_element.find_next_sibling('td').get_text(strip=True)
        return None

    def get_actors(self):
        actors_element = self.soup.find('th', string='Protagonistas')  # Cambiar 'text' por 'string'
        if actors_element:
            actors_list = actors_element.find_next_sibling('td').find_all('li')
            return [actor.get_text(strip=True) for actor in actors_list]
        return []

    def get_argument(self):
        # Busca la sección de argumento por el id
        argument_section = self.soup.find('h2', id='Argumento')
        if argument_section:
            argument_text = []
            for sibling in argument_section.find_all_next():
                if sibling.name == 'h2':  # Detener si encontramos un nuevo encabezado
                    break
                if sibling.name == 'p':  # Solo agregar párrafos
                    argument_text.append(sibling.get_text(strip=True))
            return ' '.join(argument_text).strip() if argument_text else None
        return None

    def get_movie_details(self):
        return {
            'title': self.get_title(),
            'director': self.get_director(),
            'actors': self.get_actors(),
            'argument': self.get_argument(),  # Añadir argumento aquí
        }

