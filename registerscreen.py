from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty,StringProperty#,NumericProperty
import json
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from popupwindow import *
import requests
from kivy.lang import Builder
from os import walk
from functools import partial
from firebase import firebase

class RegisterScreen(Screen):
    new_user = ObjectProperty(None)
    new_passw = ObjectProperty(None)
    confirm_new_passw = ObjectProperty(None)
    my_dict = dict()
    def add_new_account(self):
        url = 'https://kivypractice.firebaseio.com/.json'
        result = requests.get(url,timeout= 15)
        data = json.loads(result.content.decode())
        self.my_dict = data

        
        if self.new_user.text and self.new_passw.text:
            if self.new_user.text in self.my_dict.keys():
                show_RegisterPopup() 
                return False
            if self.confirm_new_passw.text != self.new_passw.text:
                show_RegisterPopupFailed()
                return False
            #result[self.new_user.text] = self.new_passw.text
            #patch to firebase using firebase module
            
            #update = firebase.FirebaseApplication(url,None)
            url2 = 'https://kivypractice.firebaseio.com/'+self.new_user.text+'.json'
            self.final_data = '{"avator":"woman","password":"%s"}'%self.new_passw.text
            requests.patch(url2,data = self.final_data)
            self.new_user.text = ''
            self.new_passw.text = ''
            show_RegisterPopupSuccess()
            return True
        show_RegisterPopupFailed_no_info()
        return False
    

class ImageButton(ButtonBehavior,Image):
    pass
class LabelButton(ButtonBehavior,Label):
    pass