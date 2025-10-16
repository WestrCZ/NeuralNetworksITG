import numpy as np
import drawing_gui as gui
import tkinter as tk

class ForwardPass:
    def __init__(self):
        self.vector1 = None
    
    def GetInputFromGUI(self, use_gui=True):
        """
        Gets 784 values representing a digit.
        
        Args:
            use_gui (bool): True = draw in GUI, False = load from file (future)
        
        Returns:
            numpy.ndarray: Array with 784 values
        """
        if use_gui:
            # Open GUI for drawing
            root = tk.Tk()
            app = gui.drawing_gui(root)
            root.mainloop()
            self.vector1 = app.get_data_flat("numpy")
            
        else:
            # Load from file - placeholder for now
            self.vector1 = np.random.randint(0, 255, size=784)
        
        print(f"Got {self.vector1.size} values")
        return self.vector1