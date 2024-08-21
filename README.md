# Sistema de WebScrapping-Proyecto Programación Orientada a Objetos

## Páginas Web:
Sitios Wiki:
  * [Wikiquote](https://es.wikiquote.org/wiki/Portada)
  * [Fandom Movies](https://www.fandom.com/topics/movies)
  * [Wikipedia](https://es.wikipedia.org/wiki/Wikipedia:Portada)
    
Sitios de Retail:

## Diagramas de Clases:

```mermaid
classDiagram
    BeautifulSoup <|-- Page
    Page <|-- Products
    Products *-- ProductCard
    Products <|-- MercadoLibre
    Products <|-- Exito

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

        + search_products()
        - compute_one_product()
        - _compute_products()
    }

    class Exito{
        + CARD_DATA
        + CARD_DATA2

        + search_products()
        - compute_one_product()
        - _compute_products()
    }

```


## Abordaje de Solución:

## Instalación e Uso:

## Librerías usadas

- beautifulsoup4
- requests
- lxml
- pandas
- openpyxl
- matplotlib
- selenium

## Reportes
[Reporte de datos](https://unaledu-my.sharepoint.com/:f:/g/personal/diporrasc_unal_edu_co/EgGtalNhip1EqE6p7OGyqIIB4OAbREHbszYB5mtlMhiqcA?e=m3yN1G)


## Uso de selenium

Algunas páginas cargan su contenido después de acceder a ellas, haciendo que la librería requests no sea útil en estas páginas. Con selenium se evita este problema aunque toma más tiempo su ejecución.

El uso de selenium está disponible en este programa para Google Chrome. **Es necesario instalar el driver del navegador.** Puede descargarlo a través de este [link](https://googlechromelabs.github.io/chrome-for-testing/) y guardarlo en la carpeta `./drivers/`
