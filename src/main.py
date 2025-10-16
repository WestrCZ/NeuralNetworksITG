import tkinter as tk
from drawing_gui import drawing_gui
from forward_pass import ForwardPass


def MAIN():
    print("MAIN LOADED")
    
    # Vytvoř instanci
    fp = ForwardPass()
    
    # Zavolej funkci - otevře GUI
    vector = fp.GetInputFromGUI(True)
    
    # Teď máš vector s 784 hodnotami
    print(vector)
    print(vector.shape)  # (784,)


# TADY VOLÁŠ FUNKCI!
MAIN()