import json;

def json_loader(path):
    """
    Načte JSON soubor a vrátí 3 arraye: structure, weights, biases
    
    Args:
        path (str): Cesta k JSON souboru
    
    Returns:
        tuple: (dimensions, weights, biases)
    """
    with open(path, 'r') as file:
        data = json.load(file)
    
    structure = data['dimensions']
    weights = data['weights']
    biases = data['biases']
    
    return structure, weights, biases

    
# MODEL:
# weights:[ ],
# iases: [ ],
#  
# structure:
# 16, 16, 20
# dest tisíc čísílek
# biases:
# 62 třeba
