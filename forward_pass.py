import numpy as np
import drawing_gui as gui
import tkinter as tk
from src.math_operations import MathOperations

class ForwardPass:
    def __init__(self):
        self.vector1 = None
    
    def run(self):
        # Spustí GUI
        root = tk.Tk()
        app = gui.drawing_gui(root)
        root.mainloop()
        
        # Po zavření okna získám numpy array 784 hodnot
        self.vector1 = app.get_data_flat("numpy")
        
        # Vypíšu hodnoty do konzole
        print("=== Hodnoty digit obrázku ===")
        print(self.vector1)
        print(f"Počet hodnot: {self.vector1.size}")
        
        return self.vector1

# Použití
if __name__ == "__main__":
    fp = ForwardPass()
    data = fp.run()