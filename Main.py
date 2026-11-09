from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
import json, os
from datetime import datetime
Window.clearcolor = (1,1,1,1)
FILE = "obras_compactacion.json"
def cargar():
    if os.path.exists(FILE):
        try:
            with open(FILE,'r',encoding='utf-8') as f: return json.load(f)
        except: return []
    return []
def guardar(d):
    with open(FILE,'w',encoding='utf-8') as f: json.dump(d,f,ensure_ascii=False,indent=2)
class PruebasCompactacion(App):
    def build(self):
        self.obras = cargar(); self.calas_inputs = []; self.ultimos = []
        root = BoxLayout(orientation='vertical', padding=5)
        root.add_widget(Label
