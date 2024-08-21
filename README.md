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
    direction RL
    class User {
        +String nickname
        +int age
        +String gender
        +String nationality
        +Type_Selection()
    }

    class SearchEngine {
        + search_for(query: string) Result[]
    }

    class Result {
        +String title
        +String type
    }

    class Multimedia {
        +play()
        +pause()
        +stop()
        +download()
    }

    class Song {
        +String title
        +String artist
        +String language
        +String duration
        +String genre
    }

    class Genre {
        +String BPM
        +String instruments
        +String harmony
    }

    class Podcast  {
        +String title
        +String author
        +String duration
        +String description
        +String category
        +String publicationDate
    }

    class ShortVideo {
        +String title
        +String creator
        +String duration
        +String description
        +String tags
        +String publicationDate
    }
 
 direction TB
    User --> SearchEngine: selects
    SearchEngine --> Result

    Result --* Song 
    Result --* Podcast
    Result --* ShortVideo
    Song --* Genre

    Podcast --|> Multimedia
     Song --|> Multimedia
      ShortVideo --|> Multimedia

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
