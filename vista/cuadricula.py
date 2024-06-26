import tkinter as tk

class Cuadricula:
    def __init__(self, root, width, height):
        self.root = root
        self.root.title("Movimiento de Mando")
        self.canvas = tk.Canvas(root, width=width, height=height)
        self.canvas.pack()
        self.canvas.image_references = []  # Crear una lista vacía para mantener las referencias de las imágenes

    def actualizar_canvas(self, matriz):
        self.canvas.delete("all")
        img_width = 50
        img_height = 50
        
        # Lista de las rutas de las imágenes correspondientes a cada elemento
        image_paths = {
            1: "imagenes/negro.png",
            2: "imagenes/mandalorian.png",
            3: "imagenes/nave.png",
            4: "imagenes/darthVader.png",
            5: "imagenes/grogu.png",
            6: "imagenes/mandalorian_y_grogu.png"
        }
        
        for i, fila in enumerate(matriz):
            for j, elemento in enumerate(fila):
                img_path = image_paths.get(elemento)
                if img_path:
                    img = tk.PhotoImage(file=img_path)
                    # Calcular la posición de inicio de la imagen para que esté centrada en la celda de la cuadrícula
                    start_x = j * img_width + (img_width - img.width()) // 2
                    start_y = i * img_height + (img_height - img.height()) // 2
                    self.canvas.create_image(start_x, start_y, anchor=tk.NW, image=img)
                    self.canvas.image_references.append(img)  # Mantén una referencia a la imagen
        
