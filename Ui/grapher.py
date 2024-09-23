import matplotlib.pyplot as plt




class Grapher:
    def __init__(self, data, dates):
        self.data_raw = data
        self.dates_raw = dates
        if len(data) != len(dates):
            raise ValueError("Data and dates must have the same length")
    
    def graph(self, label=None, scientific=False):
        # Eliminar datos N/A
        data = []
        dates = []
        for i in range(len(self.data_raw)):
            if not self.data_raw[i] == 'N/A':
                data.append(float(self.data_raw[i]))
                dates.append(self.dates_raw[i])

        data = [float(i) for i in self.data_raw]
        dates = [i for i in self.dates_raw]
                

        plt.plot(dates, data, label=label)
        plt.xlabel('Fecha')
        plt.ylabel('Precio')
        plt.title('Tendencia de precios')
        if scientific:
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        else:
            plt.ticklabel_format(style='plain', axis='y')
        if label:
            plt.legend()
    
    def show(self, block=True):
        plt.show(block=block)




    