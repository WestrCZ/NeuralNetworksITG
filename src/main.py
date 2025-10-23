import tkinter as tk
from gui import *


def MAIN():
    """Hlavní funkce - spustí GUI a vrátí data po kliknutí na Odeslat"""
    mnist_data = None
    
    root = tk.Tk()
    gui = gui(root)
    
    # Centrace okna
    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    
    # Spustit GUI
    root.mainloop()
    
    # Po zavření získat data
    mnist_data = gui.get_data()
    
    return mnist_data


# === POUŽITÍ ===
if __name__ == "__main__":
    print("Spouštím MNIST drawer...")
    
    # Zavolá se MAIN, otevře se GUI, uživatel nakreslí a klikne Odeslat
    result = MAIN()
    
    # Po zavření okna máme data
    if result:
        print(f"Získáno {len(result)} hodnot")
        print(f"První 5 hodnot: {result[:5]}")
        non_zero = sum(1 for x in result if x > 0.01)
        print(f"Aktivních pixelů: {non_zero}")
    else:
        print("Žádná data nebyla získána")