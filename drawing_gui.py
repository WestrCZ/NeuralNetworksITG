import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import tkinter.messagebox
import numpy as np

# Nastavení
BIG_SIZE = 280   # velikost hlavního plátna (pro kreslení) - zvětšeno na 280x280
SMALL_SIZE = 28  # cílové rozlišení pro MNIST
DEFAULT_BRUSH_RADIUS = 3  # výchozí poloměr štětce
DEFAULT_BRUSH_SMOOTHNESS = 0.5  # výchozí jemnost štětce (0.0 = ostrý, 1.0 = velmi měkký)
BRUSH_PREVIEW_SIZE = 100  # velikost náhledu štětce


class drawing_gui:
    def __init__(self, root):
        self.root = root
        self.root.title("MNIST Soft Brush Drawer s editorem štětce")

        # Parametry štětce
        self.brush_radius = DEFAULT_BRUSH_RADIUS
        self.brush_intensity = 1.0  # Fixní intenzita
        self.brush_smoothness = DEFAULT_BRUSH_SMOOTHNESS  # Nový parametr jemnosti

        # === HLAVNÍ LAYOUT ===
        main_frame = tk.Frame(root)
        main_frame.pack(padx=10, pady=10)

        # Levý panel - kreslení
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=10)

        # Prostřední panel - preview MNIST
        middle_frame = tk.Frame(main_frame)
        middle_frame.pack(side=tk.LEFT, padx=10)

        # Pravý panel - editor štětce
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, padx=10)

        # === KRESLÍCÍ CANVAS ===
        tk.Label(left_frame, text="Kreslící plátno (280x280)", font=("Arial", 10, "bold")).pack()
        self.big_canvas = tk.Canvas(left_frame, width=BIG_SIZE, height=BIG_SIZE, bg='black', highlightthickness=2, highlightbackground='gray')
        self.big_canvas.pack(pady=5)

        # === MNIST PREVIEW ===
        tk.Label(middle_frame, text="MNIST náhled (28x28)", font=("Arial", 10, "bold")).pack()
        self.preview_canvas = tk.Canvas(middle_frame, width=SMALL_SIZE*10, height=SMALL_SIZE*10, bg='black', highlightthickness=2, highlightbackground='gray')
        self.preview_canvas.pack(pady=5)

        # === EDITOR ŠTĚTCE ===
        brush_label = tk.Label(right_frame, text="Editor štětce", font=("Arial", 12, "bold"))
        brush_label.pack()

        # Náhled štětce
        tk.Label(right_frame, text="Náhled štětce", font=("Arial", 10)).pack(pady=(10,5))
        self.brush_preview_canvas = tk.Canvas(right_frame, width=BRUSH_PREVIEW_SIZE, height=BRUSH_PREVIEW_SIZE, bg='black', highlightthickness=1, highlightbackground='gray')
        self.brush_preview_canvas.pack()

        # Kontroly štětce
        controls_frame = tk.Frame(right_frame)
        controls_frame.pack(pady=10, fill=tk.X)

        # Velikost štětce
        tk.Label(controls_frame, text="Velikost štětce:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.radius_var = tk.IntVar(value=self.brush_radius)
        self.radius_scale = tk.Scale(controls_frame, from_=1, to=8, orient=tk.HORIZONTAL, variable=self.radius_var, command=self.update_brush_preview)
        self.radius_scale.grid(row=0, column=1, sticky=tk.EW, padx=5)
        self.radius_label = tk.Label(controls_frame, text=f"{self.brush_radius}px", font=("Arial", 10))
        self.radius_label.grid(row=0, column=2)

        # Jemnost štětce (NOVÝ)
        tk.Label(controls_frame, text="Jemnost štětce:", font=("Arial", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.smoothness_var = tk.DoubleVar(value=self.brush_smoothness)
        self.smoothness_scale = tk.Scale(controls_frame, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, variable=self.smoothness_var, command=self.update_brush_preview)
        self.smoothness_scale.grid(row=1, column=1, sticky=tk.EW, padx=5)
        self.smoothness_label = tk.Label(controls_frame, text=f"{self.brush_smoothness:.1f}", font=("Arial", 10))
        self.smoothness_label.grid(row=1, column=2)

        # Typ štětce
        tk.Label(controls_frame, text="Typ štětce:", font=("Arial", 10)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.brush_type_var = tk.StringVar(value="soft")
        brush_type_frame = tk.Frame(controls_frame)
        brush_type_frame.grid(row=2, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        tk.Radiobutton(brush_type_frame, text="Měkký", variable=self.brush_type_var, value="soft", command=self.update_brush_preview).pack(side=tk.LEFT)
        tk.Radiobutton(brush_type_frame, text="Tvrdý", variable=self.brush_type_var, value="hard", command=self.update_brush_preview).pack(side=tk.LEFT)

        # Konfigurace gridu
        controls_frame.columnconfigure(1, weight=1)

        # Hodnoty štětce
        values_frame = tk.Frame(right_frame)
        values_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(values_frame, text="Lineární hodnoty štětce", font=("Arial", 10, "bold")).pack()
        
        # Text area pro zobrazení hodnot
        self.values_text = tk.Text(values_frame, height=8, width=25, font=("Courier", 8), bg='#f0f0f0')
        self.values_text.pack(pady=5)
        
        # Scrollbar pro text
        scrollbar = tk.Scrollbar(values_frame, orient=tk.VERTICAL, command=self.values_text.yview)
        self.values_text.configure(yscrollcommand=scrollbar.set)

        # === BUTTONS ===
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.clear_btn = tk.Button(button_frame, text="Vymazat", command=self.clear, bg='#ff6b6b', fg='white', font=("Arial", 12))
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        self.submit_btn = tk.Button(button_frame, text="Odeslat", command=self.submit, bg='#4ecdc4', fg='white', font=("Arial", 12))
        self.submit_btn.pack(side=tk.LEFT, padx=5)

        self.save_btn = tk.Button(button_frame, text="Uložit obrázek", command=self.save_image, bg='#45b7d1', fg='white', font=("Arial", 12))
        self.save_btn.pack(side=tk.LEFT, padx=5)

        self.info_btn = tk.Button(button_frame, text="Zobrazit data", command=self.show_data_info, bg='#96ceb4', fg='white', font=("Arial", 12))
        self.info_btn.pack(side=tk.LEFT, padx=5)

        # === STATUS BAR ===
        self.status_var = tk.StringVar()
        self.status_var.set("Připraven - nakreslete číslicu")
        self.status_label = tk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill=tk.X, pady=5)

        # Interní obrázek pro kreslení (velký canvas)
        self.big_img = Image.new("L", (BIG_SIZE, BIG_SIZE), 0)
        self.big_draw = ImageDraw.Draw(self.big_img)

        # Události myši
        self.big_canvas.bind("<B1-Motion>", self.paint)
        self.big_canvas.bind("<Button-1>", self.paint)

        # Preview obrázky
        self.preview_photo = None
        self.brush_preview_photo = None

        # Data pro MNIST
        self.mnist_tuple = None

        # Inicializace
        self.update_preview()
        self.update_brush_preview()

    def calculate_brush_intensity(self, distance, max_radius):
        """Vypočítá intenzitu štětce na základě vzdálenosti od středu s jemností"""
        if distance > max_radius:
            return 0
        
        brush_type = self.brush_type_var.get()
        normalized_dist = distance / max_radius
        smoothness = self.smoothness_var.get()
        
        if brush_type == "hard":
            # Tvrdý štětec - s jemností ovlivňuje jen okraje
            if smoothness < 0.1:
                return 1.0  # Úplně tvrdý
            else:
                # Jemnost ovlivňuje jak rychle intenzita klesá na okrajích
                edge_threshold = 1.0 - smoothness
                if normalized_dist <= edge_threshold:
                    return 1.0
                else:
                    # Měkký přechod na okraji
                    edge_dist = (normalized_dist - edge_threshold) / smoothness
                    return max(0.0, 1.0 - edge_dist)
        else:
            # Měkký štětec - jemnost ovlivňuje křivku poklesu
            if smoothness < 0.1:
                # Téměř lineární pokles
                return 1.0 - normalized_dist
            elif smoothness > 0.9:
                # Velmi měkký, exponenciální pokles
                return (1.0 - normalized_dist) ** 3
            else:
                # Interpolace mezi lineárním a exponenciálním poklesem
                linear = 1.0 - normalized_dist
                exponential = (1.0 - normalized_dist) ** (1 + smoothness * 2)
                return linear * (1 - smoothness) + exponential * smoothness

    def update_brush_preview(self, *args):
        """Aktualizuje náhled štětce a hodnoty"""
        self.brush_radius = self.radius_var.get()
        self.brush_smoothness = self.smoothness_var.get()

        # Aktualizace labelů
        self.radius_label.config(text=f"{self.brush_radius}px")
        self.smoothness_label.config(text=f"{self.brush_smoothness:.1f}")

        # Vytvoření matice hodnot pro reálnou velikost štětce
        brush_size = self.brush_radius * 2 + 1  # průměr štětce
        values_matrix = []
        
        # Inicializace matice nulami
        for y in range(brush_size):
            row = []
            for x in range(brush_size):
                row.append(0.0)
            values_matrix.append(row)
        
        # Vyplnění skutečných hodnot štětce
        brush_center = self.brush_radius
        for dy in range(-self.brush_radius, self.brush_radius + 1):
            for dx in range(-self.brush_radius, self.brush_radius + 1):
                distance = (dx**2 + dy**2)**0.5
                intensity = self.calculate_brush_intensity(distance, self.brush_radius)
                
                # Střed štětce je vždy plná intenzita
                if dx == 0 and dy == 0:
                    intensity = 1.0
                
                # Uložit do matice
                matrix_x = brush_center + dx
                matrix_y = brush_center + dy
                if 0 <= matrix_x < brush_size and 0 <= matrix_y < brush_size:
                    values_matrix[matrix_y][matrix_x] = intensity

        # PIXEL ART náhled - nakreslit jako mřížka čtverečků
        self.brush_preview_canvas.delete("all")
        
        # Vypočítat velikost každého pixelu
        pixel_size = min(BRUSH_PREVIEW_SIZE // brush_size, 12)  # Max 12px na čtvereček
        if pixel_size < 4:
            pixel_size = 4  # Minimum 4px na čtvereček pro lepší viditelnost
        
        # Vypočítat offset pro centrování
        total_width = brush_size * pixel_size
        total_height = brush_size * pixel_size
        offset_x = (BRUSH_PREVIEW_SIZE - total_width) // 2
        offset_y = (BRUSH_PREVIEW_SIZE - total_height) // 2
        
        # Nakreslit každý pixel jako čtvereček
        for y in range(brush_size):
            for x in range(brush_size):
                intensity = values_matrix[y][x]
                
                # Pozice čtverečku
                x1 = offset_x + x * pixel_size
                y1 = offset_y + y * pixel_size
                x2 = x1 + pixel_size
                y2 = y1 + pixel_size
                
                # Barva podle intenzity (0-255)
                gray_value = int(intensity * 255)
                color = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
                
                # Nakreslit čtvereček
                if intensity > 0.01:  # Pouze viditelné pixely
                    self.brush_preview_canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=color, outline="#555555", width=1
                    )
                else:
                    # Černé pozadí s jemnou mřížkou
                    self.brush_preview_canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill="#000000", outline="#222222", width=1
                    )
        
        # Přidat info text
        brush_type = self.brush_type_var.get()
        info_text = f"{brush_size}×{brush_size} ({brush_type}, {self.brush_smoothness:.1f})"
        self.brush_preview_canvas.create_text(
            BRUSH_PREVIEW_SIZE//2, BRUSH_PREVIEW_SIZE-10,
            text=info_text, fill="white", font=("Arial", 8)
        )

        # Aktualizace textových hodnot
        self.update_brush_values_display(values_matrix)

    def update_brush_values_display(self, values_matrix):
        """Zobrazí numerické hodnoty štětce"""
        self.values_text.delete(1.0, tk.END)
        
        brush_size = len(values_matrix)
        brush_type = self.brush_type_var.get()
        
        self.values_text.insert(tk.END, f"Štětec {self.brush_radius}px ({brush_size}×{brush_size})\n")
        self.values_text.insert(tk.END, f"Typ: {brush_type}\n")
        self.values_text.insert(tk.END, f"Jemnost: {self.brush_smoothness:.1f}\n\n")
        
        # Zobrazit celou matici štětce
        for y in range(brush_size):
            line = ""
            for x in range(brush_size):
                value = values_matrix[y][x]
                if value < 0.01:
                    line += " . "  # Tečka pro nulové hodnoty
                elif value >= 0.995:
                    line += " █ "  # Plná hodnota jako blok
                else:
                    # Zobrazit jako desetinné číslo
                    line += f"{value:.1f}"[1:] + " "
            line += "\n"
            self.values_text.insert(tk.END, line)
        
        # Přidat statistiky
        total_pixels = brush_size * brush_size
        active_pixels = sum(1 for row in values_matrix for val in row if val > 0.01)
        max_val = max(max(row) for row in values_matrix)
        avg_val = sum(sum(row) for row in values_matrix) / total_pixels
        
        self.values_text.insert(tk.END, f"\nStatistiky:\n")
        self.values_text.insert(tk.END, f"Aktivní pixely: {active_pixels}/{total_pixels}\n")
        self.values_text.insert(tk.END, f"Max hodnota: {max_val:.2f}\n")
        self.values_text.insert(tk.END, f"Průměr: {avg_val:.2f}\n")

    def paint(self, event):
        """Kreslení s jemným štětcem"""
        x, y = event.x, event.y

        # Štětec s jemností
        for dx in range(-self.brush_radius, self.brush_radius + 1):
            for dy in range(-self.brush_radius, self.brush_radius + 1):
                dist = (dx**2 + dy**2)**0.5
                intensity = self.calculate_brush_intensity(dist, self.brush_radius)
                
                # Střed štětce je vždy plná intenzita
                if dx == 0 and dy == 0:
                    intensity = 1.0
                
                if intensity > 0.01:  # Pouze pokud má štětec nějaký efekt
                    px = x + dx
                    py = y + dy
                    if 0 <= px < BIG_SIZE and 0 <= py < BIG_SIZE:
                        current = self.big_img.getpixel((px, py))
                        new_value = min(255, int(current + intensity * 255))
                        self.big_img.putpixel((px, py), new_value)

        # Vizuální feedback na canvasu - jednoduchý kruh
        self.big_canvas.create_oval(
            x - self.brush_radius, y - self.brush_radius,
            x + self.brush_radius, y + self.brush_radius,
            fill="white", outline="gray", width=1
        )

        self.update_preview()
        brush_type = self.brush_type_var.get()
        self.status_var.set(f"Kreslím {brush_type} štětcem {self.brush_radius}px (jemnost {self.brush_smoothness:.1f})... Stiskněte 'Odeslat' když budete hotovi")

    def update_preview(self):
        """Přepočítá obraz na 28x28 a vykreslí náhled"""
        # zmenšení pomocí Pillow (bilinear = hladké)
        small_img = self.big_img.resize((SMALL_SIZE, SMALL_SIZE), Image.BILINEAR)

        # vytvořit náhled zvětšený 10x
        preview_large = small_img.resize((SMALL_SIZE*10, SMALL_SIZE*10), Image.NEAREST)
        self.preview_photo = ImageTk.PhotoImage(preview_large)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(0, 0, image=self.preview_photo, anchor=tk.NW)

        # uložit flatten tuple (normalizované na 0-1 pro 3Blue1Brown formát)
        raw_data = small_img.getdata()
        self.mnist_tuple = tuple(pixel / 255.0 for pixel in raw_data)

    def clear(self):
        """Vymazat canvas"""
        self.big_canvas.delete("all")
        self.big_img = Image.new("L", (BIG_SIZE, BIG_SIZE), 0)
        self.big_draw = ImageDraw.Draw(self.big_img)
        self.update_preview()
        self.status_var.set("Canvas vymazán - nakreslete číslicu")

    def submit(self):
        """Odeslat data - zavře okno"""
        self.status_var.set("Data odeslána!")
        self.root.quit()

    def save_image(self):
        """Uložit aktuální MNIST obrázek"""
        if self.mnist_tuple:
            # Převést zpět na 0-255 a uložit
            small_img = self.big_img.resize((SMALL_SIZE, SMALL_SIZE), Image.BILINEAR)
            filename = f"mnist_drawing.png"
            small_img.save(filename)
            self.status_var.set(f"Obrázek uložen jako {filename}")

    def show_data_info(self):
        """Zobrazit informace o aktuálních datech"""
        if self.mnist_tuple:
            non_zero = sum(1 for x in self.mnist_tuple if x > 0.01)
            max_val = max(self.mnist_tuple)
            avg_val = sum(self.mnist_tuple) / len(self.mnist_tuple)
            brush_type = self.brush_type_var.get()
            
            info = f"""MNIST Data Info:
Rozměry: 28x28 = {len(self.mnist_tuple)} pixelů
Nenulové pixely: {non_zero}
Maximální hodnota: {max_val:.3f}
Průměrná hodnota: {avg_val:.3f}
Formát: 3Blue1Brown kompatibilní (0.0-1.0)

První 5 hodnot: {list(self.mnist_tuple[:5])}

Aktuální štětec:
Velikost: {self.brush_radius}px
Typ: {brush_type}
Jemnost: {self.brush_smoothness:.1f}
Kreslící plátno: {BIG_SIZE}x{BIG_SIZE}px

Dostupné formáty výstupu:
- get_data("numpy") → 2D array (28x28)
- get_data("tuple") → tuple (784 prvků)
- get_data("list") → list (784 prvků)
- get_data_flat("numpy") → 1D array (784)"""
            
            tk.messagebox.showinfo("Data Info", info)

    def get_data(self, format_type="numpy"):
        """Vrátí aktuální 28x28 data v požadovaném formátu
        
        Args:
            format_type (str): 'numpy', 'tuple', nebo 'list' (default: 'numpy')
            
        Returns:
            numpy.ndarray (28x28), tuple (784 prvků), nebo list (784 prvků) s hodnotami 0.0-1.0
        """
        if self.mnist_tuple is None:
            return None
        
        if format_type == "numpy":
            # Vrať jako numpy array s shape (28, 28) pro 2D obrázek
            return np.array(self.mnist_tuple).reshape(28, 28)
        elif format_type == "list":
            # Vrať jako běžný Python list
            return list(self.mnist_tuple)
        elif format_type == "tuple":
            # Vrať jako tuple
            return self.mnist_tuple
        else:
            raise ValueError(f"Neplatný format_type: {format_type}. Použijte 'numpy', 'tuple', nebo 'list'.")
    
    def get_data_flat(self, format_type="numpy"):
        """Vrátí aktuální 28x28 data jako 1D pole (784 prvků)
        
        Args:
            format_type (str): 'numpy', 'tuple', nebo 'list' (default: 'numpy')
            
        Returns:
            numpy.ndarray (784,), tuple (784 prvků), nebo list (784 prvků) s hodnotami 0.0-1.0
        """
        if self.mnist_tuple is None:
            return None
        
        if format_type == "numpy":
            # Vrať jako 1D numpy array
            return np.array(self.mnist_tuple)
        elif format_type == "list":
            # Vrať jako běžný Python list
            return list(self.mnist_tuple)
        elif format_type == "tuple":
            # Vrať jako tuple
            return self.mnist_tuple
        else:
            raise ValueError(f"Neplatný format_type: {format_type}. Použijte 'numpy', 'tuple', nebo 'list'.")

# Spuštění aplikace (pokud je soubor spuštěn přímo)
if __name__ == "__main__":
    root = tk.Tk()
    app = drawing_gui(root)
    root.mainloop()
    
    # Získání dat po zavření okna v různých formátech pomocí argumentů
    if app.mnist_tuple:
        print("=== VÝSTUPY V RŮZNÝCH FORMÁTECH ===")
        
        # NumPy array (2D - 28x28) - DEFAULT
        numpy_2d = app.get_data()  # Default je "numpy"
        print(f"NumPy 2D (default): {numpy_2d.shape}, dtype: {numpy_2d.dtype}")
        print(f"První řádek: {numpy_2d[0][:5]}...")
        
        # NumPy array (1D - 784 prvků) 
        numpy_1d = app.get_data_flat()  # Default je "numpy"
        print(f"NumPy 1D (default): {numpy_1d.shape}, dtype: {numpy_1d.dtype}")
        print(f"První 5 hodnot: {numpy_1d[:5]}")
        
        # Explicitní formáty
        tuple_data = app.get_data("tuple")
        list_data = app.get_data("list")
        
        print(f"Tuple: {len(tuple_data)} prvků, první 5: {tuple_data[:5]}")
        print(f"List: {len(list_data)} prvků, první 5: {list_data[:5]}")
        
        print("\n=== POUŽITÍ ===")
        print("app.get_data()           # NumPy 2D (28x28) - default")  
        print("app.get_data('numpy')    # NumPy 2D (28x28)")
        print("app.get_data('tuple')    # Tuple (784 prvků)")
        print("app.get_data('list')     # List (784 prvků)")
        print("app.get_data_flat()      # NumPy 1D (784) - default")
        print("app.get_data_flat('tuple') # Tuple 1D (784)")