from ai import predict_class
from ai import get_response
from ai import get_intents
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock

from kivy.config import Config
Config.set('graphics', 'width', '390')
Config.set('graphics', 'height', '844')

intents = get_intents()

class MainWindow(Screen):
    themessage = ObjectProperty(None)
    ai_answer = ObjectProperty(None)

    def animate_text(self, dt):
        if self.index < len(self.result):
            self.ai_answer.text += self.result[self.index]
            self.index += 1
        else:
            Clock.unschedule(self.animate_text)

    def enter_message(self):
        print('pressed! ', self.themessage.text)
        ints = predict_class(self.themessage.text)
        self.result = get_response(ints, intents)
        self.index = 0
        self.ai_answer.text = ''
        Clock.schedule_interval(self.animate_text, 0.1)
        self.themessage.text = ''

class SecondWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class Widgets(Widget):
    def popup_button(self):
        show_popup()

class P(FloatLayout):
    pass

kv = Builder.load_file('styles.kv')

class MainApp(App):
    def build(self):
        return kv

def show_popup():
    show = P()
    popup_window = Popup(title='Popup Window', content=show, size_hint=(None, None), size=(400, 400))
    popup_window.open()

if __name__ == "__main__":
    MainApp().run()

'''
while True:
    message = input('')
    if message == 'q':
        break
    ints = predict_class(message)
    result = get_response(ints, intents)
    print(result)
'''