from ai import predict_class
from ai import get_response
from ai import get_intents
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput

intents = get_intents()

class MainGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MainGrid, self).__init__(**kwargs)
        self.cols = 2

        # widgets
        self.add_widget(Label(text="Message"))
        self.message = TextInput(multiline=False)
        self.add_widget(self.message)

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