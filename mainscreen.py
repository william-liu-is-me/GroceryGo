from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ObjectProperty,StringProperty,ListProperty#,NumericProperty
import json
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
import requests
#from kivy.lang import Builder
from firebase import firebase
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
import re


#Builder.load_file('FriendEventScreen.kv')


class MainScreen(Screen):
    def refresh_friend_list(self):
       
        bye = self.parent.ids['FriendListScreen'].ids['ScrollView']
        #something like this 
        bye.clear_widgets()
        my_id = self.parent.ids['LoginScreen'].account
        target = self.parent.ids['FriendListScreen'].ids['ScrollView']
        url = f'https://kivypractice.firebaseio.com/{my_id}.json'
        result = requests.get(url, timeout=30) 
        data = json.loads(result.content.decode())#
        for k in data['friend']:
            url = f'https://kivypractice.firebaseio.com/'+k+'.json'
            result = requests.get(url,timeout= 30)
            data = json.loads(result.content.decode())
            B = BoxLayout()
            imagebutton = Special_ImageButton(source= 'icon_px32/'+data['avator']+'.png',text = '%s'%k)
            B.add_widget(imagebutton)
            B.add_widget(Label(text = '%s'%k,font_size= 20,color= (66/255,76/255,80/255,1)))
            
            target.add_widget(B)
    

    def config_dropdown(self):
        
        location = self.parent.ids['AddEventScreen'].ids['desti2']
        location.clear_widgets()
        
        self.target2 = MyDropDown2()
        self.Mainbutton2 = ImageButton(source= 'icon_px32/gear.png',id='firstdropdown')#,text='choose one')#,pos_hint={'top':0.6,'right':0.6})
        self.Mainbutton2.bind(on_release = self.target2.open)
        location.add_widget(self.Mainbutton2)
        self.target2.bind(on_select=lambda instance, x: setattr(self.Mainbutton2, 'source', x))

        
        self.target = MyDropDown()
        self.Mainbutton = ImageButton(source= 'icon_px32/gear.png',id = 'seconddropdown')#,text='choose one')#,pos_hint={'top':0.6,'right':0.6})
        self.Mainbutton.bind(on_release = self.target.open)
        location.add_widget(self.Mainbutton)
        self.target.bind(on_select=lambda instance, x: setattr(self.Mainbutton, 'source', x))
    
    

class Special_ImageButton(Image,Button):
    pass
class ImageButton(ButtonBehavior,Image):
    pass
class LabelButton(ButtonBehavior,Label):
    pass
class MyDropDown(DropDown):
    pass
class MyDropDown2(DropDown):
    pass