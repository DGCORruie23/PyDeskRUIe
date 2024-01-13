import tkinter as tk
from tkinter import ttk, scrolledtext
from src.res.Colors import verde, rojo
from src.UC.usercases import getMensajesUC


class ResumenScreen:
    def __init__(self, root):
        self.root = root

    def resumenFrame(self):

        self.resumen_frame = tk.Frame(self.root, width=430, height=650, bg=rojo)
        self.resumen_frame.pack(side=tk.RIGHT, padx=(10,0))
        self.resumen_frame.pack_propagate(False)

        msg_title = tk.Label(self.resumen_frame, text="Resumen", font=("Arial", 15))
        msg_title.pack(side=tk.TOP, padx=5, pady=(20, 0))

        frameM = tk.Frame(self.resumen_frame)
        frameM.pack(pady=(20, 0))

        canvasM = tk.Canvas(frameM)
        scrollbarM = tk.Scrollbar(frameM, orient="vertical", command=canvasM.yview)
        scrollable_frameM = tk.Frame(canvasM)

        scrollable_frameM.bind(
            "<Configure>",
            lambda e: canvasM.configure(
                scrollregion=canvasM.bbox("all"),
                width=380, height=550
            )
        )

        canvasM.create_window((0, 0), window=scrollable_frameM, anchor="nw")
        canvasM.configure(yscrollcommand=scrollbarM.set)

        canvasM.pack(side="right", fill="both", expand=True)
        # canvasM.pack(side=tk.RIGHT)
        scrollbarM.pack(side="right", fill="y")

        textoInfo = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque eget ex fringilla, ultrices leo sit amet, finibus lectus. Cras placerat consequat elementum. Interdum et malesuada fames ac ante ipsum primis in faucibus. Cras a nibh dignissim, condimentum enim eu, fermentum tortor. Vestibulum vitae tellus ligula. Duis bibendum, ante ut blandit luctus, est ex convallis mi, quis bibendum sem mi in erat. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Sed pharetra libero nec congue vestibulum. Nullam id ante blandit massa aliquam volutpat sit amet quis mauris. Suspendisse posuere nisi in tristique ullamcorper."

        # Agregar texto con saltos de línea a cada ScrolledText
        list_msg = getMensajesUC()

        # for i in range(10):
        for i, data in enumerate(list_msg):
            # texto_formateado = self.dividir_texto(data.mensaje, 40)
            scrolled_text = scrolledtext.ScrolledText(
                scrollable_frameM, wrap=tk.WORD, width=45, height=10, font=("Arial", 11)
            )
            scrolled_text.pack(fill="both", expand=True, pady=5)
            scrolled_text.insert(tk.END, i)
            scrolled_text.insert(tk.END, data.mensaje)  # Insertar texto con saltos de línea


    def dividir_texto(self, texto, longitud_max=30):
        palabras = texto.split()
        lineas = []
        linea_actual = ""
        for palabra in palabras:
            if len(linea_actual) + len(palabra) < longitud_max:
                linea_actual += palabra + " "
            else:
                lineas.append(linea_actual)
                linea_actual = palabra + " "
        lineas.append(linea_actual)
        return "\n".join(lineas)




