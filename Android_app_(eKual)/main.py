#made_by_sameer_kaushik

from __future__ import division, absolute_import
from __future__ import print_function, unicode_literals

import webbrowser
import random
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex

from arithmetic import Arithmetic
from json_settings import json_settings

sc=0

#registering font
LabelBase.register(name="My_Font", fn_regular="./fonts/med.ttf", fn_bold="./fonts/med.ttf" )

##############################################
class eKualRoot(BoxLayout):
    """
    Root of all widgets
    """
    math_screen = ObjectProperty(None)

    # ------------
    def __init__(self, **kwargs):
        super(eKualRoot, self).__init__(**kwargs)
        # List of previous screens
        self.screen_list = []
        self.is_mix = False
        self.math_popup = MathPopup()

    # -------------
    def changeScreen(self, next_screen):
        operations = "addition subtraction multiplication division".split()
        question = None
        
        # If screen is not already in the list fo prevous screens
        if self.ids.kivy_screen_manager.current not in self.screen_list:
            self.screen_list.append(self.ids.kivy_screen_manager.current)

        if next_screen == "about this app":
                self.ids.kivy_screen_manager.current = "about_screen"
                
        else:
            if next_screen == "mix":
                self.is_mix = True
                index = random.randint(0, len(operations) - 1)
                next_screen = operations[index]
            else:
                self.is_mix = False
            for operation in operations:
                if next_screen == operation:
                    question = "self.math_screen.get_{}_question()".format(
                        operation
                    )
            self.math_screen.question_text.text = eKualRoot.prepQuestion(
                eval(question) if question is not None else None
            )
            self.ids.kivy_screen_manager.current = "math_screen"

    # ---------------
    @staticmethod
    def prepQuestion(question):
        " Prepares a math question with markup "
        if question is None:
            return "ERROR"
        text_list = question.split()
        text_list.insert(2, "[b]")
        text_list.insert(len(text_list), "[/b]")
        return " ".join(text_list)

    # ----------------
    def onBackBtn(self):
        if self.screen_list:
            # Check if there are any scresn to go back to
            # if there are screens we can go back to, the just do it
            self.ids.kivy_screen_manager.current = self.screen_list.pop()
            # So we don't want to close
            return True
        # No more screens to go back to
        return False
    

#################################################

class MathScreen(Screen, Arithmetic):
    # Widget that will hold questions and keypad
    def __init__(self, *args, **kwargs):
        super(MathScreen, self).__init__(*args, **kwargs)


##################################################

class MathPopup(Popup):
    #Popup for telling user whether he got it right or wrong
    GOOD = "{}\n\nScore : [b]{}[/b]"
    BAD = "{}\n\nAnswer : [b]{}[/b]\n\nScore : [b]{}[/b]"
    GOOD_LIST = ["[b]Excellent ![/b]" ,"[b]Correct ![/b]", "[b]Good ![/b]"]
    BAD_LIST = ["[b]Wrong !!![/b]", "[b]OOPS !!![/b]"]

    message = ObjectProperty()
    wrapped_button = ObjectProperty()

    # ---------------------------
    def __init__(self, *args, **kwargs):
        super(MathPopup, self).__init__(*args, **kwargs)

    # ---------------------------
    def open(self, correct=True or False):
        # Set up text message
        self.message.text = self._prep_text(correct)

        # display popup
        super(MathPopup, self).open()
        Clock.schedule_once(self.dismiss, 1.0)

    # --------------------------
    def _prep_text(self, correct):
        if correct:
            global sc
            sc=sc+2
            index = random.randint(0, len(self.GOOD_LIST) - 1)
            return self.GOOD.format(self.GOOD_LIST[index],sc)
        

        else:
            sc=sc-1
            index = random.randint(0, len(self.BAD_LIST) - 1)
            math_screen = App.get_running_app().root.math_screen
            answer = math_screen.get_answer()
            return self.BAD.format(self.BAD_LIST[index],answer,sc)


##############################################
class KeyPad(GridLayout):
    # Keypad interface
    # --------------------------
    def __init__(self, *args, **kwargs):
        super(KeyPad, self).__init__(*args, **kwargs)
        self.cols = 3
        self.spacing = 10
        self.createButtons()

    # -------------------------
    def createButtons(self):
        _list=[1,2,3,4,5,6,7,8,9]
       
        for num in _list:
            self.add_widget(Button(text=str(num),background_normal="./images/button_normal.png", on_release=self.onBtnPress))

        self.add_widget(Button(text="GO",background_color=[0,0.5,0.1,1],background_normal="./images/button_normal.png", on_release=self.onBtnPress))
        self.add_widget(Button(text="0",background_normal="./images/button_normal.png", on_release=self.onBtnPress))
        self.add_widget(Button(text="C",background_color=[0.7,0,0,1],background_normal="./images/button_normal.png", on_release=self.onBtnPress))

    # --------------------------
    def onBtnPress(self, btn):
        math_screen = App.get_running_app().root.ids.math_screen
        answer_text = math_screen.answer_text

        if btn.text.isdigit():
            answer_text.text += btn.text
        if btn.text == "GO" and answer_text.text != "":
            answer = math_screen.get_answer()
            root = App.get_running_app().root
            if int(answer_text.text) == answer:
                root.math_popup.open(True)
            else:
                root.math_popup.open(False)
            # Clear the answer text
            answer_text.text = ""
            # Prepare to get new question
            question = math_screen.question_text
            question.text = root.prepQuestion(
                math_screen.get_next_question(True if root.is_mix else False)
            )

        if btn.text == "C":
            answer_text.text = ""        


#############################################
class eKualApp(App):
    #App object
    # ----------------------------
    def __init__(self, **kwargs):
        super(eKualApp, self).__init__(**kwargs)
        self.use_kivy_settings = False
        Window.bind(on_keyboard=self.onBackBtn)
        
    # ----------------------------
    def onBackBtn(self, window, key, *args):
        # user presses back button
        if key == 27:
            return self.root.onBackBtn()
        

    # ---------------------------
    def build(self):
        return eKualRoot()

    # -----------------------------
    def getText(self):
        
        return ("Hey There!\n\n This App is created by \n"
                "[b][ref=sam][u]SAMEER KAUSHIK[/u][/ref][/b]\n"
                "using \n"
               "[b][ref=py_wiki][u]PYTHON[/u][/ref][/b] and [b][ref=kv_wiki][u]KIVY[/u][/ref][/b]\n\n\n\n\n\n"
                "[size=16]For more details click on the BOLD words\n\n  \xa9 2017 All rights reserved[/size]")

    # ----------------------------
    def on_ref_press(self, instance, ref):
        _dict = {
            "py_wiki": "https://en.wikipedia.org/wiki/Python_(programming_language)",
            "kv_wiki": "https://en.wikipedia.org/wiki/Kivy_(framework)",
            "sam":"https://www.linkedin.com/in/sameerkaushik02/"
        }

        webbrowser.open(_dict[ref])

    # ------------------------------------------
    def build_config(self, config):
        config.setdefaults("General", {"lower_num": 1, "upper_num": 100})

    # ------------------------------------------
    def build_settings(self, settings):
        settings.add_json_panel("Settings",self.config, data=json_settings)
        

    # ------------------------------------------
    def on_config_change(self, config, section, key, value):
        if key == "upper_num":
            self.root.math_screen.max_num = int(value)
        elif key == "lower_num":
            self.root.math_screen.min_num = int(value)

if __name__ == '__main__':
    eKualApp().run()
#MadeBy_SameerKaushik
#sam4python@gmail.com
