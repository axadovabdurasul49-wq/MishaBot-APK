import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class SuhbatBot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Tarix fayli
        self.history_file = "suhbat_tarixi.json"
        self.suhbat_tarixi = self.yukla_tarix()
        
        # Chat ko'rsatish uchun scroll
        self.scroll = ScrollView()
        self.chat_label = Label(text='', size_hint_y=None, text_size=(None, None), halign='left', valign='top')
        self.chat_label.bind(texture_size=self.chat_label.setter('size'))
        self.scroll.add_widget(self.chat_label)
        self.add_widget(self.scroll)
        
        # Input va tugma
        input_layout = BoxLayout(size_hint_y=0.2, orientation='horizontal')
        self.input_text = TextInput(hint_text='Xabar yozing...', multiline=False)
        input_layout.add_widget(self.input_text)
        
        send_btn = Button(text='Yubor')
        send_btn.bind(on_press=self.yuborish)
        input_layout.add_widget(send_btn)
        self.add_widget(input_layout)
        
        self.kirish_xabari()
    
    def yukla_tarix(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def saqla_tarix(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.suhbat_tarixi, f, ensure_ascii=False, indent=4)
    
    def kirish_xabari(self):
        self.yozish("Misha: Salom, jigar! Suhbatlashamiz. 😊\n")
        if self.suhbat_tarixi:
            self.yozish(f"Oldingi suhbatdan: {len(self.suhbat_tarixi)} ta xabar eslayman.\n")
    
    def yuborish(self, instance):
        xabar = self.input_text.text.strip()
        if not xabar:
            return
        
        self.suhbat_tarixi.append({"user": xabar})
        self.yozish(f"Siz: {xabar}\n")
        self.input_text.text = ''
        
        javob = self.oddiy_javob(xabar)
        self.suhbat_tarixi.append({"bot": javob})
        self.yozish(f"Misha: {javob}\n")
        
        self.saqlash()
    
    def oddiy_javob(self, xabar):
        xabar = xabar.lower()
        if "salom" in xabar:
            return "Salom! Qalaysan?"
        elif "qalaysan" in xabar:
            return "Yaxshiman! Senchi?"
        elif "o'yin" in xabar:
            return "O'yinlar yaxshi! Qaysi birini yoqtirasan?"
        else:
            return "Qiziq! Yana gaplashamiz."
    
    def yozish(self, matn):
        old_text = self.chat_label.text
        self.chat_label.text = old_text + matn
        self.chat_label.text_size = self.chat_label.texture_size

class MishaApp(App):
    def build(self):
        return SuhbatBot()

if __name__ == '__main__':
    MishaApp().run()
