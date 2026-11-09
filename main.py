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
        self.obras = cargar()
        self.calas_inputs = []
        self.ultimos = []

        root = BoxLayout(orientation='vertical', padding=5)
        root.add_widget(Label(text='PRUEBAS DE COMPACTACION 93%', bold=True, font_size=22, color=(0,0,0,1), size_hint_y=None, height=60))

        scroll = ScrollView()
        col = BoxLayout(orientation='vertical', spacing=10, padding=10, size_hint_y=None)
        col.bind(minimum_height=col.setter('height'))

        col.add_widget(Label(text='OBRAS GUARDADAS', bold=True, font_size=14, color=(0,0,0,1), size_hint_y=None, height=25))
        nombres = list(dict.fromkeys([o['obra'] for o in self.obras])) if self.obras else ["-- Sin obras --"]
        self.spin_obras = Spinner(text=nombres[0], values=nombres, size_hint_y=None, height=60, font_size=16)
        col.add_widget(self.spin_obras)

        b_cargar = Button(text='CARGAR OBRA SELECCIONADA', size_hint_y=None, height=60, font_size=16, background_color=(0.05,0.15,0.3,1))
        b_cargar.bind(on_press=self.cargar_obra)
        col.add_widget(b_cargar)

        col.add_widget(Label(text='NOMBRE DE LA OBRA', bold=True, font_size=14, color=(0,0,0,1), size_hint_y=None, height=25))
        self.in_obra = TextInput(font_size=20, size_hint_y=None, height=60, multiline=False)
        col.add_widget(self.in_obra)

        col.add_widget(Label(text='QUIEN LO SOLICITA', bold=True, font_size=14, color=(0,0,0,1), size_hint_y=None, height=25))
        self.in_solicita = TextInput(font_size=20, size_hint_y=None, height=60, multiline=False)
        col.add_widget(self.in_solicita)

        col.add_widget(Label(text='FECHA (dd/mm/aaaa)', bold=True, font_size=14, color=(0,0,0,1), size_hint_y=None, height=25))
        self.in_fecha = TextInput(text=datetime.now().strftime("%d/%m/%Y"), font_size=20, size_hint_y=None, height=60, multiline=False)
        col.add_widget(self.in_fecha)

        col.add_widget(Label(text='SECA MAXIMA LAB (kg/m3)', bold=True, font_size=14, color=(0,0,0,1), size_hint_y=None, height=25))
        self.in_secamax = TextInput(font_size=22, size_hint_y=None, height=60, input_filter='float', multiline=False)
        col.add_widget(self.in_secamax)

        col.add_widget(Label(text='HUMEDAD OPTIMA LAB (%)', bold=True, font_size=14, color=(0,0,0,1), size_hint_y=None, height=25))
        self.in_wopt = TextInput(font_size=22, size_hint_y=None, height=60, input_filter='float', multiline=False)
        col.add_widget(self.in_wopt)

        col.add_widget(Label(text='NUMERO DE CALAS', bold=True, font_size=14, color=(0,0,0,1), size_hint_y=None, height=25))
        self.spin_num = Spinner(text='3', values=['1','2','3','4','5'], size_hint_y=None, height=60, font_size=18)
        self.spin_num.bind(text=self.generar_calas)
        col.add_widget(self.spin_num)

        self.box_calas = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.box_calas.bind(minimum_height=self.box_calas.setter('height'))
        col.add_widget(self.box_calas)

        fila = BoxLayout(spacing=10, size_hint_y=None, height=70)
        btn_calc = Button(text='CALCULAR TODO', font_size=18, bold=True, background_color=(0.05,0.15,0.3,1))
        btn_calc.bind(on_press=self.calcular)
        btn_limp = Button(text='LIMPIAR', font_size=16, bold=True, background_color=(0.3,0.3,0.3,1), size_hint_x=0.4)
        btn_limp.bind(on_press=self.limpiar_todo)
        fila.add_widget(btn_calc); fila.add_widget(btn_limp)
        col.add_widget(fila)

        self.lbl_res = Label(text='1) Humedad = Material / Volumen\n2) Seca = Humedad / (1+W/100)\n3) Grado = Seca / SecaMax *100\n\nVerde = SI PASA  Rojo = NO PASA (93%)', font_size=14, color=(0,0,0,1), size_hint_y=None, height=450, markup=True)
        col.add_widget(self.lbl_res)

        b_guardar = Button(text='GUARDAR LOTE', size_hint_y=None, height=65, font_size=18, bold=True, background_color=(0.1,0.4,0.15,1))
        b_guardar.bind(on_press=self.guardar_prueba)
        col.add_widget(b_guardar)

        b_hist = Button(text='VER HISTORIAL', size_hint_y=None, height=55, font_size=16, background_color=(0.4,0.25,0.05,1))
        b_hist.bind(on_press=self.ver_historial)
        col.add_widget(b_hist)

        b_borrar = Button(text='BORRAR OBRA', size_hint_y=None, height=50, font_size=14, background_color=(0.5,0.1,0.1,1))
        b_borrar.bind(on_press=self.borrar_obra)
        col.add_widget(b_borrar)

        self.lbl_hist = Label(text='', font_size=13, color=(0,0,0,1), size_hint_y=None, height=400, markup=True)
        col.add_widget(self.lbl_hist)

        scroll.add_widget(col)
        root.add_widget(scroll)
        self.generar_calas(None, '3')
        return root

    def generar_calas(self, a, texto):
        self.box_calas.clear_widgets()
        self.calas_inputs = []
        n = int(texto)
        for i in range(1, n+1):
            self.box_calas.add_widget(Label(text=f'CALA {i}', font_size=14, bold=True, color=(0,0,0,1), size_hint_y=None, height=25))
            row = BoxLayout(spacing=8, size_hint_y=None, height=55)
            m = TextInput(hint_text='g Mat', font_size=16, input_filter='float', multiline=False)
            v = TextInput(hint_text='f Vol', font_size=16, input_filter='float', multiline=False)
            w = TextInput(hint_text='i W%', font_size=16, input_filter='float', multiline=False)
            row.add_widget(m); row.add_widget(v); row.add_widget(w)
            self.box_calas.add_widget(row)
            self.calas_inputs.append({'m':m,'v':v,'w':w})
        self.box_calas.height = n * 85

    def cargar_obra(self, *args):
        texto = self.spin_obras.text
        if texto.startswith("--"): return
        for o in self.obras:
            if o['obra'] == texto:
                self.in_obra.text = o['obra']; self.in_solicita.text = o.get('solicita',''); self.in_fecha.text = o.get('fecha_obra',''); self.in_secamax.text = o.get('seca_max',''); self.in_wopt.text = o.get('w_opt','')
                break

    def calcular(self, *args):
        try:
            seca_max = float(self.in_secamax.text.replace(',','.'))
            res = ""; self.ultimos = []
            for idx, c in enumerate(self.calas_inputs, 1):
                if not c['m'].text or not c['v'].text or not c['w'].text: continue
                g = float(c['m'].text.replace(',','.')); f = float(c['v'].text.replace(',','.')); w = float(c['w'].text.replace(',','.'))
                humedad = g / f; seca = humedad / (1 + w/100)
                hum_kg = humedad * 1000; seca_kg = seca * 1000; grado = (seca_kg / seca_max) * 100
                color = "0a8a0a" if grado >= 93 else "ff0000"
                estado = "SI PASA" if grado >= 93 else "NO PASA"
                # AQUI ESTA EL ARREGLO QUE PEDIAS
                res += f"[color={color}][b]Cala {idx}: H={hum_kg:.0f} kg/m3 S={seca_kg:.0f} kg/m3 -> {grado:.1f}% {estado}[/b][/color]\n"
                res += f"[color=000000]  g={g}/f={f}={humedad:.4f} | S={humedad:.4f}/(1+{w}/100)={seca:.4f}[/color]\n\n"
                self.ultimos.append({'cala':idx,'humedad':hum_kg,'seca':seca_kg,'grado':grado,'estado':estado,'g':g,'f':f,'w':w})
            if not self.ultimos: self.lbl_res.text = "Llena 1 cala"; return
            prom = sum(u['grado'] for u in self.ultimos)/len(self.ultimos)
            col_p = "0a8a0a" if prom >= 93 else "ff0000"
            est_p = "SI PASA" if prom >= 93 else "NO PASA"
            res += f"[color={col_p}][size=20][b]PROMEDIO: {prom:.1f}% {est_p}[/size][/b][/color]"
            self.lbl_res.text = res
            self.lbl_res.height = 200 + len(self.ultimos)*90
        except Exception as e:
            self.lbl_res.text = f"Error {e}"

    def limpiar_todo(self, *args):
        self.in_obra.text=""; self.in_solicita.text=""; self.in_secamax.text=""; self.in_wopt.text=""
        self.in_fecha.text = datetime.now().strftime("%d/%m/%Y")
        for c in self.calas_inputs: c['m'].text=""; c['v'].text=""; c['w'].text=""
        self.lbl_res.text="Datos limpiados"

    def guardar_prueba(self, *args):
        self.calcular()
        if not self.ultimos: return
        for u in self.ultimos:
            self.obras.append({'fecha': datetime.now().strftime("%d/%m/%Y %H:%M"), 'fecha_obra': self.in_fecha.text, 'obra': self.in_obra.text, 'solicita': self.in_solicita.text, 'seca_max': self.in_secamax.text, 'w_opt': self.in_wopt.text, 'cala': u['cala'], 'humedad': f"{u['humedad']:.0f}", 'seca': f"{u['seca']:.0f}", 'grado': f"{u['grado']:.1f}", 'estado': u['estado'], 'w_campo': str(u['w'])})
        guardar(self.obras)
        self.spin_obras.values = list(dict.fromkeys([o['obra'] for o in self.obras]))
        self.lbl_res.text += "\n\nGuardado OK"

    def borrar_obra(self, *args):
        txt = self.spin_obras.text
        self.obras = [o for o in self.obras if o['obra'] != txt]
        guardar(self.obras)
        self.spin_obras.values = list(dict.fromkeys([o['obra'] for o in self.obras])) if self.obras else ["-- Sin obras --"]
        self.spin_obras.text = self.spin_obras.values[0]

    def ver_historial(self, *args):
        if not self.obras: self.lbl_hist.text = "Vacio"; return
        t = ""
        for o in self.obras[-20:]:
            color = "0a8a0a" if float(o['grado']) >= 93 else "ff0000"
            t += f"[color={color}]{o.get('fecha_obra','')} {o['obra']} C{o['cala']} H:{o['humedad']} S:{o['seca']} {o['grado']}% {o['estado']}[/color]\n"
        self.lbl_hist.text = t

PruebasCompactacion().run()
