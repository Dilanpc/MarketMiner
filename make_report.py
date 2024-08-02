import threading
from scrape import MercadoLibre


if __name__ == "__main__":

    def report(search, ruta, ruta_links):
        page = MercadoLibre()
        page.search_products(search)
        page.make_report(ruta, ruta_links)

    threads = []

    threads.append(threading.Thread(target=lambda: report("computador", "reports/computadorReport.csv", "reports/computadorLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("iphone 15", "reports/iphoneReport.csv", "reports/iphoneLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("impresora 3d", "reports/impresoraReport.csv", "reports/impresoraLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("Tarjeta gráfica", "reports/tarjetaGraficaReport.csv", "reports/tarjetaGraficaLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("celular", "reports/celularReport.csv", "reports/celularLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("tv", "reports/tvReport.csv", "reports/tvLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("reloj", "reports/relojReport.csv", "reports/relojLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("audífonos", "reports/audifonosReport.csv", "reports/audifonosLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("camisa", "reports/camisaReport.csv", "reports/camisaLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("zapatos", "reports/zapatosReport.csv", "reports/zapatosLinks.csv")))
    threads.append(threading.Thread(target=lambda: report("pantalón", "reports/pantalonReport.csv", "reports/pantalonLinks.csv")))

    porcentaje = 0

    for t in threads:
        t.start()

    for t in threads:
        t.join()
        porcentaje += 100 / len(threads)
        print(f"{round(porcentaje)}% completado", end="\r")
    
    print("\nFinalizado")
