from ai import predict_class
from ai import get_response
from ai import get_intents
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from pyobjus import autoclass, objc_str
from kivy.utils import platform
#from texttospeech import text_to_speech
#import threading
from tools import parse_todo_list2
from calendar_utils import parse_calendar_message
from todolist import search_todo_list

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

    def stop_text_animation(self):
        Clock.unschedule(self.animate_text)
        self.ai_answer.text = self.result

    def create_todo_list(self):
        self.index = 0
        self.ai_answer.text = ''
        todo_list = parse_todo_list2(self.themessage.text)
        self.result = "Certainly! "
        todo_list_length = len(todo_list)
        if (todo_list_length) == 1:
            self.result += "'" + todo_list[0] + "'" + ' has been added to your to-do list.'
        else:
            for i in range(todo_list_length):
                if i == todo_list_length - 1:
                    self.result += "and '" + todo_list[i] + "'"
                    break
                self.result += "'" + todo_list[i] + "', "
            self.result += ' have been added to your to-do list.'
        #thread1 = threading.Thread(target=text_to_speech, args=(self.result,))
        #thread1.start()
        Clock.schedule_interval(self.animate_text, 0.1)
        self.themessage.text = ''

    def create_calendar_event(self):
        self.index = 0
        self.ai_answer.text = ''
        calendar_event = parse_calendar_message(self.themessage.text)
        event_name = calendar_event[0]
        event_date = calendar_event[1]
        event_time = calendar_event[2]
        if 'tomorrow' not in event_date:
            self.result = "Absolutely! '" + event_name + "' has been added to your calendar on " + event_date + ' from ' + event_time + '.'
        else:
            self.result = "Absolutely! '" + event_name + "' has been added to your calendar for " + event_date + ' from ' + event_time + '.'
        #thread1 = threading.Thread(target=text_to_speech, args=(self.result,))
        #thread1.start()
        Clock.schedule_interval(self.animate_text, 0.1)
        self.themessage.text = ''

    # add a debounce to not allow users to type another message before ai is done talking.

    def find_date(self):
        months = [
            'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
            'december', 'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sept', 'aug', 'oct', 'nov', 'dec'
        ]

    def find_todolist_item(self, date):
        self.index = 0
        self.ai_answer.text = ''
        todolist_items = search_todo_list(date)
        self.result = 'On ' + date + ' you have: '
        for i in todolist_items:
            self.result += i + ' '
        Clock.schedule_interval(self.animate_text, 0.1)
        self.themessage.text = ''


    def enter_message(self):
        ints = predict_class(self.themessage.text)
        #{'intent': 'greetings', 'probability': '0.9999906'}] = near perfect match
        #[{'intent': 'greetings', 'probability': '0.97283036'}] = unrelated
        print(ints)
        if float(ints[0]['probability']) < 0.99:
            # for unrelated message
            self.result = "I'm sorry, but I do not understand. I am an AI designed to help with personal productivity tasks."
            self.index = 0
            self.ai_answer.text = ''
            #thread1 = threading.Thread(target=text_to_speech, args=(self.result,))
            #thread1.start()
            Clock.schedule_interval(self.animate_text, 0.1)
            self.themessage.text = ''
            return
        
        if ints[0]['intent'] == 'todo':
            self.find_todolist_item('june 1st 2023')
            return
        '''
        elif ints[0]['intent'] == 'calendar':
            self.create_calendar_event()
            return
        '''
        self.result = get_response(ints, intents)
        self.index = 0
        self.ai_answer.text = ''
        #thread1 = threading.Thread(target=text_to_speech, args=(self.result,))
        #thread1.start()
        Clock.schedule_interval(self.animate_text, 0.1)
        #thread1.join()
        self.themessage.text = ''

class SecondWindow(Screen):
    
    def show_photo_picker(instance):
        if platform != 'ios':
            print("Photo selection is only available on iOS.")
            return

        from rubicon.objc.eventloop import EventLoop
        from rubicon.objc.runtime import objc_method

        UIApplication = autoclass('UIApplication')
        UIImagePickerController = autoclass('UIImagePickerController')
        root_view_controller = UIApplication.sharedApplication().keyWindow.rootViewController

        @objc_method
        def handle_photo_pick(_self, _cmd, picker, info):
            selected_image = info.objectForKey_(UIImagePickerController.InfoKey.originalImage)
            # Process the selected image
            print("Selected Photo:", selected_image)

        image_picker = UIImagePickerController.alloc().init()
        image_picker.setSourceType_(UIImagePickerController.SourceTypePhotoLibrary)
        image_picker.setDelegate_(None)

        EventLoop.main().run_until_complete(
            root_view_controller.presentViewController_animated_completion_(image_picker, True, None)
        )


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