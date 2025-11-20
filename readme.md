# Neuronky AI

Cílem projektu je vytvořit neuronovou síť, která je schopna rozpoznávat číslice psané rukou. </br>
Inspirací projektu je Youtube série od tvůrce [3Blue1Brown](https://www.youtube.com/c/3blue1brown).</br>
Některé části projektu mohou být identické těm, které má 3B1B ve [svém repozitáři](https://github.com/3b1b/videos/tree/master/_2017/nn), ze zmíněné série na neuronové sítě.

## Použité technologie

- Python 3.13.4 – [python.org](https://www.python.org/downloads/)  
- Veškeré závislosti jsou uvedeny v souboru `requirements.txt`.

## Iniciální příprava projektu

1. Stáhněte a nainstalujte Python z výše uvedeného odkazu.  
2. V root adresáři projektu otevřete terminál a spusťte příkaz:

   ```bash
   python /env/environment_init.py
   ```
Tento skript vytvoří virtuální prostředí, nainstaluje potřebné balíčky ze souboru requirements.txt a předzpracuje dataset ze souboru mnist.pkl.gz. Výsledná data budou uložena do složky /data ve formátu vhodném pro další vývoj.

Výstupem je trojice tuple, která obsahuje obrázky a jejich štítky jako NumPy pole:

```python
(
  (train_images, train_labels),
  (valid_images, valid_labels),
  (test_images, test_labels)
)
```
- Obrázky jsou uloženy jako numpy.ndarray.

- Štítky jsou pole celých čísel (třídy 0–9).

Při vývoji, nebo testu je nutno vždy před spuštěním prvního skriptu aktivovat environment, jinak vám nebudou fungovat balíčky.

### Powershell
```bash
.\neuronkyEnv\Scripts\Activate.ps1
```

### Bash
```bash
.\neuronkyEnv\Scripts\Activate.bat
```

Pro otestování dat z preprocesu spusťte v terminálu příkaz ```python test_load_preprocessed.py```. </br>
Vystup by měl vypadat asi takto:
```bash
Train data size: 50000
Validation data size: 10000
Test data size: 10000
First training input shape: (784, 1)
First training label shape: (10, 1)
First training label vector (one-hot):
[[0.]
 [0.]
 [0.]
 [0.]
 [0.]
 [1.]
 [0.]
 [0.]
 [0.]
 [0.]]
First validation label: 3
First test label: 7
```

## Deaktivace venv
Když chceme deaktivovat python prostředí naší neuronky, ve kterém máme balíčky, spustíme v terminálu
```bash
deactivate
```

## mnist_preprocess.py
Tento soubor rozbalí trénovací data z původního formátu do jiného, který už jsme schopni nějak přečíst.

## mnist_loader.py
Načítá z už rozbalených dat, jeho funkce budou používány v samotné neuronové síti.