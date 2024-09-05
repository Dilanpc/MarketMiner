import sys
import os
#sys.path.append(os.path.join(os.path.dirname(__file__)))

from .comparador import Interface



def main():
    a = Interface()
    a.mainloop()


if __name__ == "__main__":
    main()
