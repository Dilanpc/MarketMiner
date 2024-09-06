import sys
import os
import threading
from MarketMiner.scrape import MercadoLibre, Exito, Linio

def report(clase, search, ruta, ruta_links, __tries=1):
    try:
        page = clase()
        page.search_products(search)
        page.make_report(ruta, ruta_links)
    except Exception as e:
        print(f"Error en reporte de {search}: {e}")
        __tries += 1
        if __tries < 4:
            print(f"Intento {__tries}/3")
            report(clase, search, ruta, ruta_links, __tries)
        else:
            print(f"Se ha superado el número de intentos para {search}")
            
ruta = "reports"

busquedas: list[str] = ["computador", "iphone 15", "impresora 3d", "tarjeta gráfica", "celular", "tv", "reloj", "audífonos", "camisa", "zapatos", "pantalón"]


if __name__ == "__main__":
    exeMercadoLibre = input("¿Ejecutar MercadoLibre? s/n: ").lower() == "s"
    exeExito = input("¿Ejecutar Exito? s/n: ").lower() == "s"
    exeLinio = input("¿Ejecutar Linio? s/n: ").lower() == "s"

    if exeMercadoLibre:
        print("Iniciando reportes de MercadoLibre")
        threads = []

        for busqueda in busquedas: # Crear un hilo por cada busqueda
            threads.append(threading.Thread(target=lambda keyword=busqueda: report(MercadoLibre, keyword, f"{ruta}/mercadoLibre/{keyword}Report.csv", f"{ruta}/mercadoLibre/{keyword}Links.csv")))

        porcentaje = 0

        for t in threads: # Iniciar los hilos
            t.start()

        for t in threads: # Esperar a que los hilos terminen
            t.join()
            porcentaje += 100 / len(threads)
            print(f"{round(porcentaje)}% completado", end="\r")
        
        print("\nMercadoLibre finalizado")

    if exeExito:
        print("Iniciando reportes de Exito")
        threads = []

        for busqueda in busquedas:
            threads.append(threading.Thread(target=lambda keyword=busqueda: report(Exito, keyword, f"{ruta}/exito/{keyword}Report.csv", f"{ruta}/exito/{keyword}Links.csv")))


        porcentaje = 0
        for t in threads:
            t.start()
        for t in threads:
            t.join()
            porcentaje += 100 / len(threads)
            print(f"{round(porcentaje)}% completado", end="\r")
        
        print("\nExito finalizado")


    if exeLinio:
        print("Iniciando reportes de Linio")
        threads = []

        for busqueda in busquedas:
            threads.append(threading.Thread(target=lambda keyword=busqueda: report(Linio, keyword, f"{ruta}/linio/{keyword}Report.csv", f"{ruta}/linio/{keyword}Links.csv")))


        porcentaje = 0
        for t in threads:
            t.start()
        for t in threads:
            t.join()
            porcentaje += 100 / len(threads)
            print(f"{round(porcentaje)}% completado", end="\r")
        
        print("\nLinio finalizado")