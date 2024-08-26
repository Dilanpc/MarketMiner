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
                
class WikiQuoteScience(WikiPage):
    def __init__(self, url):
        super().__init__(url)
        self.url = url
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
        
    def find_quotes(self, quote):
        quotes = []
        for quote in self.soup.select('li'):
            for keyword in keywords:
                if keyword in quote.text:
                    highlited_quote = quote.text.replace(keyword, f"\033[1;31;40m{keyword}\033[m")
                    quotes.append(highlited_quote)
                    break
        
        return quotes
            
    def find_author(self, author):
        authors = []
        for author in self.soup.select('li'):
            author_tag = author.find('a', title=True)
            if author_tag:
                authors.append(author_tag.text)
            else:
                authors.append("Anónimo")
        return authors
            

                
if __name__ == "__main__":
    # WIKIPEDIA
    wikipedia_page = Wikipedia('https://es.wikipedia.org/wiki/Lionel_Messi')
    
 # Definir la lista de palabras clave a buscar
    keywords = ["Balón de Oro", "Balones de Oro"]
    
    print(wikipedia_page.get_title())  

    # Llamar al método para encontrar párrafos que contengan las palabras clave
    wikipedia_page.find_keyword(keywords)
    
    
    # WIKIQUOTE
    
    wiki_quote_page = WikiQuoteScience('https://es.wikiquote.org/wiki/Ciencia')
    keywords = ["ciencia", "científico"]
    print(wiki_quote_page.get_title())    
    quotes = wiki_quote_page.find_quotes(keywords)
    authors = wiki_quote_page.find_author(keywords)
    
    for quote, author in zip(quotes, authors):
        print(f"{quote} - {author}")
        print("-------------------------------------------------")
