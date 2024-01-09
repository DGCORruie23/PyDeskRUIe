import tkinter as tk
import pandas as pd

from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import ttk

bdate_list = [ xdate.strftime("%d/%m/%Y") for xdate in \
                 pd.bdate_range(start='1/1/1920', end='1/1/2025') ]

root = tk.Tk()
root.title("Physical Deal Porter")
width=400
height=500
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

deliverydate = tk.Label(root, text="Delivery :")
deliverydate.place(x=10,y=230,width=70,height=25)
deliverydate_box = ttk.Combobox(root, width=20, values=bdate_list)
deliverydate_box.place(x=100,y=230,width=200,height=25)

pricingdate = tk.Label(root, text="Pricing :")
pricingdate.place(x=10,y=335,width=70,height=25)
pricingdate_box = AutocompleteCombobox(root, width=20, completevalues=bdate_list)
pricingdate_box.place(x=100,y=335,width=200,height=25)

root.mainloop()

# from ttkwidgets.autocomplete import AutocompleteCombobox
# import tkinter as tk
# from tkinter import ttk, messagebox
# from src.UC.usercases import getPaisesUC
#
# def infoP(event):
#         messagebox.showinfo("Alerta", f"Opción elegida: {opcion_nacionalidad.get()}")
#
# opc_paises = []
# for pais in getPaisesUC():
#         opc_paises.append(pais.nombre_pais)
#
# window = tk.Tk()
#
# opcion_nacionalidad = tk.StringVar()
#
# tk.Label(window, text="Combobox with autocompletion for the Tk instance's methods:").pack(side='left')
# entry = AutocompleteCombobox(window, width=20, completevalues=opc_paises, textvariable=opcion_nacionalidad)
# entry.pack(side='right')
#
# entry.bind("<<ComboboxSelected>>", infoP)
# entry.bind('<Return>', infoP)
# window.mainloop()


# from ttkwidgets.autocomplete import AutocompleteEntry
# from tkinter import *
#
# countries = [
#         'Antigua and Barbuda', 'Bahamas','Barbados','Belize', 'Canada',
#         'Costa Rica ', 'Cuba', 'Dominica', 'Dominican Republic', 'El Salvador ',
#         'Grenada', 'Guatemala ', 'Haiti', 'Honduras ', 'Jamaica', 'Mexico',
#         'Nicaragua', 'Saint Kitts and Nevis', 'Panama ', 'Saint Lucia',
#         'Saint Vincent and the Grenadines', 'Trinidad and Tobago', 'United States of America'
#         ]
#
# ws = Tk()
# ws.title('PythonGuides')
# ws.geometry('400x300')
# ws.config(bg='#f25252')
#
# frame = Frame(ws, bg='#f25252')
# frame.pack(expand=True)
#
# Label(
#     frame,
#     bg='#f25252',
#     font = ('Times',21),
#     text='Countries in North America '
#     ).pack()
#
# entry = AutocompleteEntry(
#     frame,
#     width=30,
#     font=('Times', 18),
#     completevalues=countries
#     )
# entry.pack()
#
# ws.mainloop()


# import tkinter as tk
# def mostrar_info_adicional( numero_tarjeta):
#     # Esta función muestra información adicional cuando se hace clic en una tarjeta
#     # Aquí puedes implementar la lógica para mostrar detalles específicos de la tarjeta seleccionada
#     print(f"Mostrando detalles de la tarjeta {numero_tarjeta}")
#
#
# def crear_tarjetas(root):
#     # Función para crear las tarjetas
#     for i in range(1, 6):  # Crear 5 tarjetas como ejemplo
#         tarjeta = tk.Frame(root, width=200, height=100, bd=1, relief=tk.RAISED)
#         tarjeta.grid(row=i, column=0, padx=10, pady=10)
#
#         etiqueta = tk.Label(tarjeta, text=f"Tarjeta {i}", font=("Arial", 12))
#         etiqueta.pack(padx=5, pady=5)
#
#         # Asociar un evento de clic a cada tarjeta
#         tarjeta.bind("<Button-1>", lambda event, num=i: mostrar_info_adicional(num))
#
#
# def main():
#     root = tk.Tk()
#     root.title("Tarjetas Informativas")
#
#     crear_tarjetas(root)
#
#     root.mainloop()
#
#
# if __name__ == "__main__":
#     main()


# from tkinter import *
#
# root = Tk()
#
# def key(event):
#     print("pressed", repr(event.char))
#
# def callback(event):
#     frame.focus_set()
#     print("clicked at", event.x, event.y)
#
# frame = Frame(root, width=100, height=100)
# frame.bind("<Key>", key)
# frame.bind("<Button-1>", callback)
# frame.pack()
#
# root.mainloop()