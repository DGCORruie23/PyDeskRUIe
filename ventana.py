import tkinter as tk

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Ventana Principal")

    def mostrar_ventana(self):
        # Crear la ventana principal
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="¡Hola desde la ventana principal!")
        self.label.pack()

        self.button = tk.Button(self.frame, text="Abrir Otra Ventana", command=self.abrir_ventana_secundaria)
        self.button.pack()

    def abrir_ventana_secundaria(self):
        # Crear y mostrar la ventana secundaria
        self.ventana_secundaria = tk.Toplevel(self.root)
        self.ventana_secundaria.title("Ventana Secundaria")

        self.label_secundaria = tk.Label(self.ventana_secundaria, text="¡Hola desde la ventana secundaria!")
        self.label_secundaria.pack()

        self.button_secundaria = tk.Button(self.ventana_secundaria, text="Cerrar", command=self.ventana_secundaria.destroy)
        self.button_secundaria.pack()
