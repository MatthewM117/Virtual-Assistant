from ai import predict_class
from ai import get_response
from ai import get_intents
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

intents = get_intents()

class MainGrid(Widget):
    message = ObjectProperty(None)

    def enter_message(self):
        print("Your message: ", self.message.text)
        self.message.text = ''

class MainApp(App):
    def build(self):
        return MainGrid()

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