# Sistema de WebScrapping-Proyecto Programación Orientada a Objetos

## Alternativa Seleccionada:
 * **_Sistema de WebScrapping para páginas de retail y páginas tipo wiki_**

## Definición del Problema

### Páginas de Retail:
 * ### Realizar la extracción de datos asociados a productos de diferentes páginas de retail, como Mercado Libre, Linio y Éxito, con el fin de comparar precios, disponibilidad y otras características de los productos. 
 
 * El enfoque principal de la parte del programa dedicada a las páginas de retail, será a productos de tecnología y electrodomésticos. Los datos recolectados de productos como televisores, celulares, tablets, audífonos, entre otros, serán tomados durante un cierto periodo de tiempo para tener un registro histórico de las variaciones de los precios y disponibilidades, que será almacenado en una base de datos. Con el objetivo de enseñar los datos de una manera más intuitiva y un poco más práctica, inicialmente se pensó en la realización de una pequeña interfaz que sea capaz de mostrar los datos recolectados dependiendo del producto que el usuario desee buscar, y tenga la posibilidad de acceder directamente al link del producto en específico que le llame la atención. 
 * De esta manera y en sentido de orientar los datos recolectados por el sistema mencionado, paralelo y aparte a este proyecto, se puede buscar en un futuro es la creación de una interfaz mayor que sea capaz de permitir al usuario realizar la comparativa simultáneamente entre productos de diferentes páginas de retail, y así es permitirle evitar la acción de realizar la comparación del producto de interés ingresando a cada una de las páginas individualmente. 

### Páginas Wiki:
 * ### Realizar la extracción de texto de páginas como Wikipedia o Wiki Quotes, buscando automatizar la extracción de títulos, párrafos y citas. 
 
 * La extracción de texto vendría sujeta al interés del usuario del programa. En ese sentido se planteó específicamente para el caso de la extracción de Wiki Quotes, el registro de las citas asociadas a ciencia. Principalmente se busca que el programa entregue una cita con su respectivo autor asociado. Para el caso de Wikipedia, se tiene como primera alternativa la extracción de texto de un tema en concreto, y como segunda la extracción de una página asociada a una película en específico, capaz de brindar información particular de la misma, como su título, su director, su trama y sus premios. 

## Páginas Web:

### Sitios de Retail:

* [Mercado Libre](https://www.mercadolibre.com.co)
* [Linio](https://linio.falabella.com.co/linio-co)
* [Éxito](https://www.exito.com/?srsltid=AfmBOor0YAfmwqltX-hxWduWqMq0UKwCbFNT9Od6TJyyvHtGHMWu7Rpw)

###### NOTA: Sujeto a adición de más páginas

### Sitios Wiki:
  * [Wikiquote](https://es.wikiquote.org/wiki/Portada)
  * [Wikipedia](https://es.wikipedia.org/wiki/Wikipedia:Portada)
  
    


## Diagramas de Clases:

### Diagrama de Clases Scrapping a Páginas de Retail:

A continuación se presenta el diagrama de clases del programa principal encargado de realizar el scrapeo a las páginas de Retail. Se puede observar que se parte del trabajo con librerías como Selenium y BeautifulSoup que facilitan la automatización del navegador y la extracción de datos estructurados de las páginas web.

```mermaid
classDiagram
    BeautifulSoup <|-- Page
    Page <|-- Products
    Products *-- ProductCard
    Products <|-- MercadoLibre
    Products <|-- Exito
    Products <|-- Linio


    class BeautifulSoup{
        + find()
        + find_all()
    }

    class Page{
        - _driver
        + html

        + find()
        + find_all()
    }

    class Products{
        + page_name
        + link
        + products
        + names
        + prices
        + links
        + SELENIUM

        - _enter_webpage(link: str)
        + search_products(link: str)
        + get_product_by_link(link: str)
        - _compute_info()
        - _compude_product(link:str)
        - _compute_one_product()

    }

    class ProductCard{
        + tag
        + _attrs_name
        + _attrs_price
        + _attrs_link
        + _exc_attrs_name
        + _exc_attrs_price
        + _exc_attrs_link
        + name
        + price_txt
        + price
        + link

        + define_product()
        - _compute_name()
        - _compute_price()
        - _compute_link()
        - _search_attrs_in_list(sections: list, attrs: dict, excluded: dict)
        - __decode_price()
    }


    class MercadoLibre{
        + CARD_DATA
        + CARD_DATA2

        + search_products(product)
        - compute_one_product()
        - _compute_products()
    }

    class Exito{
        + CARD_DATA
        + CARD_DATA2

        + search_products(product)
        - compute_one_product()
        - _compute_products()
    }

    class Linio {
        + __CARD_DATA
        + page_name: str
        + search_products(product)
        + _compute_products()
    }

```

Las clases presentes en el diagrama se explican a continuación:  

* BeautifulSoup: Será la clase encargada de encapsular las funcionalidades de la librería BeautifulSoup, permitiendo el uso de métodos como find() y find_all(), que facilitan la búsqueda de elementos en el HTML de las páginas web.

* Page: Será la clase que representa a una página web. Contiene un controlador de navegador _driver y el contenido HTML de la página. Esta clase también proporciona métodos para buscar elementos en la página utilizando las capacidades de la librería BeautifulSoup.

* Products: Será la clase responsable de gestionar la búsqueda y extracción de productos de las páginas de retail. Esta clase incluye atributos como page_name, link, products, names, prices, y links. Los métodos proporcionan el ingreso a una página web, permitiendo buscar productos, y obtener información específica de productos mediante enlaces.

* ProductCard: Será la clase que represente una tarjeta de producto individual, que contiene atributos como name, price, y link. Sus métodos permiten definir los productos y estimar sus atributos.

 ###### NOTA: Se decidió utilizar el término tarjeta para describir a la sección de la página web que encapsula a cada uno de los productos y los enseña en la página principal tras la búsqueda. Muestra la imagen del producto, su nombre, precio, descuento, valoración, entre otras características. Para este caso solo se utilizan los datos de precio, nombre y link. 

* Mercado Libre, Exito y Linio: Serán las clases destinadas a manejar la búsqueda de productos en sus respectivas plataformas. Todas las clases tienen atributos para almacenar datos de tarjetas de productos (CARD_DATA, CARD_DATA2) y métodos para realizar búsquedas y calcular información sobre los productos.


### Diagrama de Clases Scrapping a Páginas Wiki:

A continuación se presenta el diagrama de clases del programa encargado de extraer el texto de páginas de Wiki, como Wikipedia y Wikiquote.

```mermaid

classDiagram
   WikiPage <|-- Wikipedia
   WikiPage <|-- WikiQuoteScience
   Wikipedia<|-- WikiMovie
    
   

   class WikiPage{
        + url: str
        + page
        + soup: BeautifulSoup
+ get_tittle()
+ get_paragraph()
    }

    class Wikipedia{
        + find_keywords(keywords: list)
    }

    class WikiQuoteScience{
        + find_quotes(keywords: list)
+find_author(keywords: list)

    }

   class WikiMovie{


        + get_title()
+get_actors()
+get_director()
+get_argument()
+get_movie_details()

    }
    

```


El diagrama incluye las siguientes clases:

* WikiPage: Esta clase representará a una página Wiki genérica. Por esto contará con atributos como url, page, y soup. Este último utiliza la librería BeautifulSoup y facilita el análisis del contenido HTML. Los métodos get_title() y get_paragraph(), permitirán extraer el título y los párrafos de la página, proporcionando una base común para las clases hijas. 

* Wikipedia: Esta será una subclase de WikiPage y añadirá funcionalidades específicas para la búsqueda de palabras clave en Wikipedia. Para esto se utilizará el método find_keywords(keywords: list), que recibirá unas palabras clave de interés y serán buscadas en la página.

* WikiQuoteScience: También será una subclase de Wikipage y se enfocará en la búsqueda de citas científicas en la página WikiQuote. Los métodos find_quotes() y y find_author() permitirán extraer citas junto a los autores de las mismas.

* WikiMovie: Esta clase será una clase hija de Wikipedia, y estará dedicada a la información sobre películas encontrada en dicha página. La idea es que permita, mediante los métodos definidos, encontrar, el título de la película, los actores, director/es y argumento de la película de interés que se busquen en la página principal de Wikipedia.
   
### Diagrama de Clases de Interfaz:

```mermaid
   classDiagram
    QMainWindow <|-- Interface
    Interface *-- QTabWidget
    QTabWidget *-- MarketMinerTab
    QTabWidget *-- ReportsTab
    MarketMinerTab *-- Header
    MarketMinerTab *-- FrameShops
    FrameShops *-- Shop
    Shop *-- SearchTread
    Shop *-- ProductInfo
    Shop *-- Results
    Results *-- ProductButton

    ReportsTab *--ReportHeader
    ReportsTab *-- ReportList
    ReportList *-- ReportCard
    ReportCard *-- ReportThread
    ReportsTab *-- ReportInfo
    ReportInfo *-- ReportInfoList
    ReportInfoList *-- ReportInfoCard


    class QMainWindow{

    }
    class Interface{
        + app: QApplication
        + tabs: QTabWidget
        + reportManager
        + exec()
    }

    class QTabWidget{

    }

    class MarketMinerTab{
        + header: Header
        + frameShops: FrameShops
        + searchButtonState()
        + sort_by_price()
    }

    class Header{
        + tittle: QLabel
        + entry: QLineEdit
        + button: QPushButton
        + sorted: QCheckBox
        + seacrh()
    }

    class FrameShops{
        + mercadoShop: Shop
        + exitoShop: Shop
        + linioShop: Shop
        + shops: list[Shop]
        + search()
        + reactivateButton()
        + sort_by_price()
    }

    class Shop{
        + tittle: QLabel
        + ecommerce: Product
        - loading: bool
        - sorted: bool
        + results: Results
        + last_query
        + product_info: ProductInfo
        + thread: SearchTread
        + setTittle()
        + setEcommerce()
        + updateProducts()
        + print_products()
        + get_products()
        + sort_by_price()
        + clearWidget()
        + showProduct()
        + hideProduct()
    }

    class SearchTread{
        + ready: Signal
        + run()
    }

    class Results{
        + buttons: list[ProductButton]
        + widget: QWidget
        + layout: QVBoxLayout
        + updateButtons()
        + clear()
        + noResults()
        + showProduct()
        + hideProduct()
    }

    class ProductButton{
        + product: ProductCard
    }

    class ProductInfo{
        + name: QLabel
        + QPrice: QLabel
        + link: QPushButton
        + closeButton: QPushButton
        + setProduct()
        + openLink()
    }



    class ReportsTab{
        + reportManager: ReportManager
        + mainWidget: QWidget
        + reportList: reportList
        + header: ReportHeader
        + info: ReportInfo
        + hideReportInfo()
    }

    class ReportHeader{
        + reportsManager: ReportManager
        + reportList: ReportList
        + tittle: QLabel
        + nameEntry: QLineEdit
        + queryEntry: QLineEdit
        + classEntry: QComboBox
        + addbtn: QPushButton
        + addReport()

    }

    class ReportList{
        + widget: QWidget
        + cards: list[ReportCard]
        + layout: QVBoxLayout
        + updateCards()
        + addCard()
        + clear()
    }

    class ReportCard{
        + reportUi: ReportsTab
        + report: Report
        + tittle: QLabel
        + query: QLabel
        + class_: QLabel
        + path: QLabel
        + startbtn: QPushButton
        + infobtn: QPushButton
        + layout: QGridLayout
        + run()
        + reportFinished()
        + showInfo()

    }


    class ReportThread{
        + ready: Signal
        + run()
    }

    class ReportInfo{
        + reportUi: ReportTab
        + report: Report
        + closebtn: QPushButton
        + tittle: QLabel
        + query: QLabel
        + list: ReportInfoList
        + layout: QGridLayout
        + setReport()
    }


    class ReportInfoList{
        + data: list[list[str]]
        + widget: QWidget
        + layout: QVBoxLayout
        + cards: list[ReportInfoCard]
        + load_data()
        + updateCards()
        + clear()
    }


    class ReportInfoCard{
        + name: startbtn
        + dates: list[float]
        + namelabel: QLabel
        + showbtn: QPushButton
        + layout: QHBoxLayout
        - graph()
    }
  

```


## Abordaje de Solución:

Dentro del código HTML de las páginas a scrapear, cada sección que contenga información se agrupa por diferentes etiquetas, como h2, p, h3, etc. Las etiqutas marcan la estructura jerárquica de los encabezados y párrafos dentro de una página. Es importante mencionar que incluso la información contenida en tablas también posee sus respectivas etiquetas. Por ejemplo, en el caso de páginas como Wikipedia, los encabezados en negrilla poseen una etiqueta de tipo h2 y los párrafos etiquetas de tipo p. Cada etiqueta puede demarcar patrones comunes en la estructura de la página, que serán el objetivo principal para realizar la extracción de los datos. 
Para realizar el scrapeo de las páginas, inicialmente se realizó la inspección del código HTML de los diferentes links, con el objetivo de buscar cada una de las etiquetas. Una vez encontrada una etiqueta de una sección de interés, se contrastó con las etiquetas de otras secciones para poder encontrar el patron que se mencionó anteriormente. Encontrando el patrón, se definieron métodos específicos para extraer la información asociada a cada etiqueta, y sobre ellos se fue diseñando el programa que se mostrará por partes a continuación. Se optó por dividir tanto el sistema de retail como el de wikis en diferentes ejecuciones, para poder trabajar en cada uno de manera específica. Además de esto, con MarketMiner se buscó un enfoque más comercial y dirigido a cualquier tipo de persona. Por lo que para esto se diseñó una interfaz que permitiese la interacción del programa de mejor manera para el usuario. Para el caso de WikiMiner, al ser de menor interés comercial, solo se realizó la ejecución mediante la consola. Sin embargo, no se descarta la implementación de los programas en una misma interfaz que brinde al usuario ambas alternativas. 

### Clase Page
Para ingresar a las páginas de retail se crea la clase Page, que hereda de BeautifulSoup: Page recibe un link el cual abre usando la librería request o selenium según se requiera, con el objetivo final de obtener el código fuente de la página. Adicionalmente se redefinen los métodos find() y find_all() añadiendo la funcionalidad de búsqueda por etiquetas HTML.

### Clase Product
Esta clase que hereda de Page, está dirigida a manejar el código fuente obtenido para encontrar productos de páginas retail con los atributos y etiquetas HTML que se especifiquen. Su principal método search_products(), recibe un link, entra y guarda el código fuente usando la clase de la que hereda, Page, luego se encarga de buscar las secciones donde se puede obtener información de cada producto, las características de cada producto se buscan en la clase ProductCard, al final se obtiene una lista de objetos ProductCard que contienen el nombre, precio y link de cada producto.
Una vez que se tenga la lista de ProductCards, la clase Product ofrece el método make_report() el cual crea un archivo csv o lo actualiza si ya existe con los productos que tiene guardados en su instancia. Es posible adicionar una ruta para un archivo csv de links.

### Clase ProductCard
Con el objetivo de guardar cada producto de forma en la que sea sencillo acceder a sus atributos se crea ProductCard, esta clase guarda el nombre, precio o link del producto y proporciona métodos para encontrar estos atributos en una sección del código HTML proporcionado en su inicialización. Para especificar qué atributos debe buscar, se diseñaron métodos que reciben listas de diccionarios, cada diccionario contine uno o varios atributos, y el método se encargará de buscar en el orden de la lista los atributos de cada diccionario, además, exite la opción de añadir atributos que si se encuentran, se descarta la sección.

### Clases MercadoLibre, Exito y Linio
Estas clases heredan de Product, su principal función es guardar los atributos que se necesitan para hallar cada producto en su respectiva página, estos datos se guardan en las variables __CARD_DATA, estos se usarán para redefinir _compute_products, la redefinición consiste en llamar a al método _compute_products de la clase padre, Product, usando de argumentos las variables __CARD_DATA.




### Clase WikiPage:
Para el sistema dedicado a las páginas wiki, se definieron las clases que se plantearon en el diagrama de clases, con sus respectivos métodos y atributos. En primer lugar, dentro del módulo wiki_page.py se construyó la clase WikiPage, que será la clase padre que busca abstraer a una página Wiki en general. La clase recibe como atributo un link que dirige a la página wiki que se va a instanciar, y define un método que entrega el título de la página. Utilizando las librerías Requests y BeautifulSoup, se registra como txto el HTML de la página para poder parsearla (analizar una cadena de texto para identificar y extraer la información de interés). Esta clase será la encargada de heredar el atributo de URL y el método get_title a las demás clases hijas (WikiQuoteScience y Wikipedia)

``` python
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

```

### Clase Wikipedia:

En segundo lugar, dentro del módulo wikipedia.py se construyó la clase Wikipedia, que es una clase hija de WikiPage y hereda el atributo que define al link de la página. Como el objetivo del sistema que scrapea las páginas de Wikipedia es permitir al usuario la búsqueda de la información de interés con la ayuda del filtrado por palabras clave, se definió un método find_keywords. Este método se encargará de recibir las palabras clave que ingrese el usuario y recorrer los diferentes párrafos de la página para buscar en cada uno de ellos, los que contengan a las palabras. Una vez se encuentren las palabras en algún párrafo, se imprimirá y se seguirán buscando párrafos coincidentes hasta el final de la página. Merece la pena resaltar que los párrafos se buscaron por la etiqueta 'p', por lo que inicialmente se van a registrar todos los elementos de la página asociados a la etiqueta. En el caso de Wikipedia, la etiqueta 'p' unícamente corresponde a los párrafos. 

``` python
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
                if keyword.lower() in paragraph.text.lower():  # Si se encuentra palabra clave está en el párrafo se imprime el párrafo
                    print(paragraph.text)  
                    print("-------------------------------------------------") 
                    break  # Salir del bucle de palabras clave si se encontró una coincidencia
```
### Ejecución

Con el objetivo de realizar una prueba correspondiente, se decidió restringir el link de la página de Wikipedia, a la página del [Real Madrid Club de Fútbol](https://es.wikipedia.org/wiki/Real_Madrid_Club_de_Fútbol). Con la idea de probar la ejecución, se usaron la palabra clave "champions", y se ejecutó el código que se muestra a continuación. 

``` python
# WIKIPEDIA
    print("----------------------  WIKIPEDIA  ---------------------------")
    wikipedia_page = Wikipedia('https://es.wikipedia.org/wiki/Real_Madrid_Club_de_Fútbol')
    
 # Definir la lista de palabras clave a buscar
    keywords = []
    while True:
        keywords.append(input("Ingrese una palabra clave: "))
        if keywords[-1] == "salir":
            keywords.pop()
            break
    
    print(wikipedia_page.get_title())  

    # Llamar al método para encontrar párrafos que contengan las palabras clave
    wikipedia_page.find_keyword(keywords)
```

En primer lugar se define el link de la página a scrapear. Luego se le solicita al usuario las palabras clave deseadas y hasta que se ingrese una palabra que rompa la ejecución ("salir"). Posteriormente se llama el método que entrega el título de la página y al método que encuentra los párrafos que contienen a las palabras deseadas. De esta manera se obtiene una ejecución con la siguiente forma: 

```
----------------------  WIKIPEDIA  ---------------------------
Ingrese una palabra clave: champion
Ingrese una palabra clave: salir

Real Madrid Club de Fútbol - Wikipedia, la enciclopedia libre

En la temporada 2022-23, en la jornada 16, el club juega por primera vez en su historia sin ningún español de inicio.[421]​

Adicionalmente, ganó su octavo Mundial de Clubes y su vigésima Copa del Rey tras golear al Barcelona 0-4 en semifinales en el Camp Nou.

Sin embargo, perdió la Supercopa de España por 3-1 frente al F. C. Barcelona en la final, quedó eliminado de la Champions League en semifinales tras perder 4-0 contra el Manchester City de Guardiola y quedó a 10 puntos del líder Barcelona en la Liga.

Aun así, no sobra destacar que alcanzando las semifinales, el Madrid ha llegado a 11 de las últimas 13 semifinales de la Champions League.

``` 
### Clase WikiQuoteScience:

En tercer lugar, en el módulo wikiquote_sience se construyó la clase WikiQuoteScience, y se buscó que con los métodos definidos, se filtraran solo las secciones relevantes dentro de la página. Esto es debido a que la página Wiki Quotes define diferentes secciones de la página con las mismas etiquetas. En ese sentido, se usó un método encargado de quitar secciones como "Refranes y Dichos Populares" de los párrafos con las etiquetas correspondientes a las citas. Luego de esto, se definió un método encargado de recopilar todas las secciones de interés que además utilizara el filtro mencionado anteriormente. Cada cita encontrada dentro de la página, se imprime con su respectivo autor y con la palabra "ciencia" resaltada, para dar una muestra de cómo podría funcionar la ejecución por palabras clave como en el caso de Wikipedia. Es importante mencionar, que en el apartado de los autores, también se aplicó un filtro dentro del propio método para quitar algunas secciones que se registraban como parte del mismo. Algunas de estas, correspondían a secciones con links, como bloques de registro de usuario y ayuda. Finalmente, en caso de que se registren citas sin autor, se imprime la cita con un autor "anónimo". 

``` python
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
```
### Ejecución

En cuanto a la ejecución del programa, nuevamente se utilizan unas palabras claves, pero en este caso ya son definidas para realizar la prueba correspondiente. Esto es con el objetivo de brindar una aplicabilidad a la búsqueda de las citas. Posteriormente se ejecutan los métodos que entregan el título de la página y las citas con sus respectivos autores. Para comprobar que se estuviesen encontrando el número de citas y autores adecuado, se realizaron dos líneas de código encargadas de contar las citas y los autores encontrados. 
``` python
# WIKIQUOTE
    print("----------------------  WIKIQUOTE  ---------------------------")
    wiki_quote_page = WikiQuoteScience('https://es.wikiquote.org/wiki/Ciencia')  # Crear una instancia de WikiQuoteScience

    keywords = ["ciencia", "científico"]  # Definir las palabras clave a buscar

    print(wiki_quote_page.get_title())  # Imprimir el título de la página
    
    # Obtener las citas y autores
    quotes, authors = wiki_quote_page.find_quotes_and_authors(keywords)
    
    # Imprimir cada cita con su respectivo autor
    for quote, author in zip(quotes, authors):
        print(f"{quote} - {author}")  # Imprimir cita y autor
        print("-------------------------------------------------")
        
    # Contar citas y autores
    print(f"Total de citas encontradas: {len(quotes)}")  # Imprimir la cantidad total de citas encontradas
    print(f"Total de autores encontrados: {len(authors)}")  # Imprimir la cantidad total de autores encontrados
```
A continuación se observa la forma que debería tener la ejecución: 
```
----------------------  WIKIQUOTE  ---------------------------
Ciencia - Wikiquote
«A la ciencia hay que temerla: por un lado te cura la tos y por el otro te manda un avión a tu pueblo y te tira una bomba nuclear».[2]
Gloria Fuertes - Gloria Fuertes
-------------------------------------------------
«A los hombres les encanta maravillarse: esa es la semilla de la ciencia». [3]
Emerson - Emerson
-------------------------------------------------
«Cada conquista de la ciencia es una victoria del absurdo». [4]
Jacques Monod - absurdo

``` 
### Clase WikiMovie

Por último lugar, en el módulo wikimovie.py, se construyó la clase WikiMovie. Esta es una clase hija de Wikipedia, pues la idea es que la información de las películas se busque dentro de la misma Wikipedia. Teniendo esto en cuenta, se definieron métodos encargados de analizar las tablas que contienen la información del director, título y actores de la película. Para cada uno de ellos, se buscó la etiqueta adecuada y definida dentro de la página en Wikipedia. Además de esto, se definió un método al final, encargado de recopilar los datos encontrados por los demás métodos. 

``` python
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
```
### Ejecución

Para la ejecución de la clase WikiMovie, se probó de manera general con la página de Wikipedia para la película Oppenheimer. Sin embargo, se solicita al usuario un link en caso de que desee buscar una película en específico. Luego se ejecuta el método get_movie_details que va a retornar toda la información de la película.  

``` python

# WIKIMOVIE
    print("----------------------  WIKIMOVIE  ---------------------------")
    link = input("Ingrese el enlace de la película en Wikipedia, vacio se usa oppenheimer: ")
    if link == "":
        movie = WikiMovie('https://es.wikipedia.org/wiki/Oppenheimer_(pel%C3%ADcula)')
    else:
        movie = WikiMovie(link)

    details = movie.get_movie_details()
    print("Título:", details['title'])
    print("Director:", details['director'])
    print("Actores:")
    for actor in details['actors']:
        print("-", actor)
    print("Argumento:", details['argument'])

```
De esta manera, la ejecución del código debería poseer la siguiente forma:

``` 
----------------------  WIKIMOVIE  ---------------------------
Ingrese el enlace de la película en Wikipedia, vacio se usa oppenheimer:
Título: Oppenheimer
Director: Christopher Nolan
Actores:
- Cillian Murphy
- Emily Blunt
- Matt Damon
- Florence Pugh
- Josh Hartnett
- Casey Affleck
- Rami Malek
- Kenneth Branagh
Argumento: En 1926, el estudiante en doctorado de 22 añosJ. Robert Oppenheimersufre de nostalgia y ansiedad mientras estudia con el físico experimentalPatrick Blacketten elLaboratorio Cavendishde  laUniversidad de Cambridge...
```

## Instalación e Uso:
Para que cada usuario pueda ejecutar el código usando python, únicamente se debe instalar el driver corresponediente a la versión de Google Chrome. Para instalar el driver puede consultar en la sección 'Uso de selenium' donde encontrará la página que se ha usado para obtener los drivers.
Luego de esto, el código correrá sin problemas.
Si lo prefiere, puede descargar el archivo de 'Releases' con el que obtendrá un archivo .exe para el sistema operativo Windows.

## Librerías usadas

- beautifulsoup4
- requests
- lxml
- pandas
- openpyxl
- matplotlib
- selenium
- PySide6

## Reportes
[Reporte de datos](https://unaledu-my.sharepoint.com/:f:/g/personal/diporrasc_unal_edu_co/EgGtalNhip1EqE6p7OGyqIIB4OAbREHbszYB5mtlMhiqcA?e=m3yN1G)


## Uso de selenium

Algunas páginas cargan su contenido después de acceder a ellas, haciendo que la librería requests no sea útil en estas páginas. Con selenium se evita este problema aunque toma más tiempo su ejecución.

El uso de selenium está disponible en este programa para Google Chrome. **Es necesario instalar el driver del navegador.** Puede descargarlo a través de este [link](https://googlechromelabs.github.io/chrome-for-testing/) y guardarlo en la carpeta `./drivers/`
