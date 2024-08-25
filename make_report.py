import threading
from scrape import MercadoLibre


def report(search, ruta, ruta_links, __tries=1):
    try:
        page = MercadoLibre()
        page.search_products(search)
        page.make_report(ruta, ruta_links)
    except Exception as e:
        print(f"Error en reporte de {search}: {e}")
        __tries += 1
        if __tries < 4:
            print(f"Intento {__tries}/3")
            report(search, ruta, ruta_links, __tries)
        else:
            print(f"Se ha superado el número de intentos para {search}")
            



if __name__ == "__main__":

    threads = []

    threads.append(threading.Thread(target=lambda: report("computador", "reports/mercadoLibre/computadorReport.csv", "reports/mercadoLibre/computadorLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("iphone 15", "reports/mercadoLibre/iphoneReport.csv", "reports/mercadoLibre/iphoneLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("impresora 3d", "reports/mercadoLibre/impresoraReport.csv", "reports/mercadoLibre/impresoraLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("Tarjeta gráfica", "reports/mercadoLibre/tarjetaGraficaReport.csv", "reports/mercadoLibre/tarjetaGraficaLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("celular", "reports/mercadoLibre/celularReport.csv", "reports/mercadoLibre/celularLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("tv", "reports/mercadoLibre/tvReport.csv", "reports/mercadoLibre/tvLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("reloj", "reports/mercadoLibre/relojReport.csv", "reports/mercadoLibre/relojLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("audífonos", "reports/mercadoLibre/audifonosReport.csv", "reports/mercadoLibre/audifonosLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("camisa", "reports/mercadoLibre/camisaReport.csv", "reports/mercadoLibre/camisaLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("zapatos", "reports/mercadoLibre/zapatosReport.csv", "reports/mercadoLibre/zapatosLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("pantalón", "reports/mercadoLibre/pantalonReport.csv", "reports/mercadoLibre/pantalonLinks.csv")))
    
    porcentaje = 0

    for t in threads:
        t.start()

    for t in threads:
        t.join()
        porcentaje += 100 / len(threads)
        print(f"{round(porcentaje)}% completado", end="\r")
    
    print("\nFinalizado")
