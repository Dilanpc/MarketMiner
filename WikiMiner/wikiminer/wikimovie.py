import requests  
from bs4 import BeautifulSoup  

from .wikipedia import Wikipedia  # Importa la clase WikiPage del módulo wiki_page

class WikiMovie(Wikipedia):
    def __init__(self, url):
        super().__init__(url)
    
    def get_title(self, custom_soup=None):
        # Usar el `soup` proporcionado si se pasa, o el `soup` de la instancia
        soup = custom_soup if custom_soup else self.soup
        title_element = soup.find('th', class_='cabecera cine')
        return title_element.get_text(strip=True) if title_element else None
    
    def get_director(self, custom_soup=None):
        soup = custom_soup if custom_soup else self.soup
        director_element = soup.find('th', string='Dirección')
        if director_element:
            return director_element.find_next_sibling('td').get_text(strip=True)
        return None

    def get_actors(self, custom_soup=None):
        soup = custom_soup if custom_soup else self.soup
        actors_element = soup.find('th', string='Protagonistas')
        if actors_element:
            actors_list = actors_element.find_next_sibling('td').find_all('li')
            return [actor.get_text(strip=True) for actor in actors_list]
        return []

    def get_argument(self, custom_soup=None):
        soup = custom_soup if custom_soup else self.soup
        argument_section = soup.find('h2', id='Argumento')
        if argument_section:
            argument_text = []
            for sibling in argument_section.find_all_next():
                if sibling.name == 'h2':
                    break
                if sibling.name == 'p':
                    argument_text.append(sibling.get_text(strip=True))
            return ' '.join(argument_text).strip() if argument_text else None
        return None

    def get_movie_details(self, custom_url=None):
        if custom_url:
            response = requests.get(custom_url)
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            soup = self.soup
        
        return {
            'title': self.get_title(soup),
            'director': self.get_director(soup),
            'actors': self.get_actors(soup),
            'argument': self.get_argument(soup),
        }
