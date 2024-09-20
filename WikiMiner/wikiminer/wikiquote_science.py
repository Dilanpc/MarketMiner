"""
Módulo que contiene la clase WikiQuoteScience que hereda de WikiPage.
"""

from .wiki_page import WikiPage  # Importa la clase WikiPage del módulo wiki_page

# Clase que hereda de WikiPage y representa una página de WikiQuote sobre ciencia.
class WikiQuoteScience(WikiPage):
    def __init__(self, url):
        super().__init__(url)  # Se heredan los atributos de la clase padre

    # Método que filtra las secciones no deseadas y encuentra la sección de citas.
    # Se usa solo dentro de la clase WikiQuoteScience.
    def _filter_relevant_sections(self):
        """
        Encuentra la sección de citas y filtra secciones no deseadas como
        'Refranes', 'Dichos populares', etc.
        """
        # Encontrar la sección principal que contiene las citas
        main_content = self.soup.find('div', {'class': 'mw-parser-output'})  # Selecciona el div principal que contiene el contenido
        sections = main_content.find_all(['h2', 'ul'])  # Encuentra todos los encabezados y listas en el contenido

        filtered_sections = []  # Lista para almacenar las secciones relevantes
        in_relevant_section = False  # Bandera para determinar si se encuentra en una sección relevante
        for section in sections:
            if section.name == 'h2':  # Verifica si el elemento es un encabezado
                # Si se encuentra el encabezado de "Citas", se activa la captura de citas
                if 'Citas' in section.text:
                    in_relevant_section = True
                # Si se encuentran encabezados de secciones no deseadas, se desactiva la captura
                elif any(x in section.text for x in ['Refranes', 'Dichos', 'Proverbios']):
                    in_relevant_section = False
            # Si se encuentra dentro de la sección relevante, se captura el contenido
            if in_relevant_section:
                filtered_sections.append(section)  # Agregar la sección relevante a la lista
        return filtered_sections  # Retornar las secciones filtradas

    def find_quotes_and_authors(self, keywords: list[str]):
        quotes = []  # Lista para almacenar las citas encontradas
        authors = []  # Lista para almacenar los autores encontrados

        # Filtrar las secciones relevantes
        relevant_sections = self._filter_relevant_sections()

        # Limitar la búsqueda de citas y autores a las secciones relevantes
        for section in relevant_sections:
            if section.name == 'ul':  # Solo buscamos dentro de listas <ul> de citas
                for quote_item in section.find_all('li'):  # Buscar cada elemento de la lista
                    # Buscar citas basadas en las palabras clave
                    for keyword in keywords:
                        if keyword in quote_item.text:  # Verifica si la palabra clave está en el texto de la cita
                            # Resaltar la palabra clave en la cita
                            highlighted_quote = quote_item.text.replace(keyword, f"\033[1;31;40m{keyword}\033[m")
                            quotes.append(highlighted_quote)  # Agregar la cita resaltada a la lista

                            # Intentar obtener el autor directamente después de la cita
                            author_tag = quote_item.find('a', title=True)  # Busca el enlace del autor
                            # Verifica que el enlace del autor no sea uno de los enlaces no deseados
                            if author_tag and not any(kw in author_tag['href'].lower() for kw in ['ayuda', 'login', 'registro', 'signup', 'admin']):
                                authors.append(author_tag.text)  # Agregar el nombre del autor a la lista
                            else:
                                authors.append("Anónimo")  # Si no hay autor, agregar "Anónimo"
                            break  # Salir del bucle de palabras clave una vez que se encuentra una coincidencia
        
        return quotes, authors  # Retornar las listas de citas y autores