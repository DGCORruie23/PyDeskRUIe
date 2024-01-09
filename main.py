import tkinter as tk
import time
import requests
import json
import sqlalchemy.dialects.sqlite

import src.res.Strings as Texts
from src.res.Colors import verde, rojo, marron, rojo_oscuro

import src.api.config as api
import src.db.models
from src.db.models import Usuario, Mensaje, RegistroNombres, RegistroFamilias, RescateComp
from src.UC.usercases import getAllPaisesUC, getAllFuerzaUC, getAllMunicipiosUC, getAllPuntosIUC, verifyUser, \
    updateUser, getDataUC
from src.UC.usercases import getMensajesUC

from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime
from types import SimpleNamespace

import ttkwidgets
from ttkwidgets.autocomplete import AutocompleteCombobox

from sqlalchemy import create_engine, Column, Integer, String, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func


from src.UI.splashScreen import SplashScreen
from src.UI.login import Login

def clean_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def main():
    root = tk.Tk()
    root.overrideredirect(True)
    root.title('Bienvenidos')

    imagenI = Image.open("src/res/drawable/logo.ico")  # Reemplaza con la ruta de tu imagen
    imagenI = imagenI.resize((24, 24))  # Cambiar el tamaño si es necesario
    icono = ImageTk.PhotoImage(imagenI)
    root.tk.call('wm', 'iconphoto', root._w, icono)

    scr1 = SplashScreen(root)
    scr1.splashFrame()

    root.mainloop()


if __name__ == "__main__":
    main()

