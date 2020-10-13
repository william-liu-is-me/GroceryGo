import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
from kivy.properties import ObjectProperty,StringProperty,ListProperty#,NumericProperty
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
from loginscreen import LoginScreen
from registerscreen import RegisterScreen
from mainscreen import MainScreen
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
import re
from time import ctime


Builder.load_file('Popupwindow.kv')
Builder.load_file('LoginScreen.kv')
Builder.load_file('MainScreen.kv')
Builder.load_file('RegisterScreen.kv')
Builder.load_file('AddEventScreen.kv')
Builder.load_file('AddFriendScreen.kv')
Builder.load_file('SettingsScreen.kv')
Builder.load_file('ChangeAvatorScreen.kv')
Builder.load_file('FriendListScreen.kv')
Builder.load_file('FriendEventScreen.kv')

class GroceryGoApp(App):
    def build(self):
        
        return GroceryGoScreenManager(transition= FadeTransition())
    def on_start(self):
        #print(self.root.ids['ChangeAvatorScreen'].ids['ScrollViewChangeAvator'])
        #this is for avator change
        target_change_avator = self.root.ids['ChangeAvatorScreen'].ids['ScrollViewChangeAvator']
        for _,_,files in walk('C:/Users/William Liu/Desktop/python_code/kivy 练习册/Grocery Go!/icon_px32'):
            for pic in files:
                img=ImageButton(source='icon_px32/'+ pic
                                ,on_release= partial(self.change_avator,pic))
                #print(img)
                target_change_avator.add_widget(img)


    def change_avator(self,image,image_id):
        #change avator
        #这里pic参数是个tuple 需要用两个参数分开，不然会出错 2 positional but 3 given
        avator = self.root.ids['MainScreen'].ids['ImageButton1']
        avator_in_list = self.root.ids['FriendListScreen'].ids['ImageButton1']
        avator.source='icon_px32/'+image
        avator_in_list.source='icon_px32/'+image
        setting_avator = self.root.ids['ChangeAvatorScreen'].ids['avator']
        setting_avator.source = 'icon_px32/'+image
        #update firebase
        data = '{"avator":"%s"}'%image[:-4]
        requests.patch('https://kivypractice.firebaseio.com/'+self.root.ids['LoginScreen'].account+'.json',data= data)
        #print('https://kivypractice.firebaseio.com/'+self.root.ids['LoginScreen'].account+'.json')
    

class GroceryGoScreenManager(ScreenManager):
   def FriendGroceryBanner(self,data1):
        #print(self)
       
        url = 'https://kivypractice.firebaseio.com/'+data1+'.json'
        result = requests.get(url,timeout= 15)
        data = json.loads(result.content.decode())
        
        target = self.ids['FriendEventScreen'].ids['ScrollView']
        target.clear_widgets()
        self.ids['FriendEventScreen'].ids['image_to_set'].source = 'icon_px32/'+data['avator']+'.png'
        self.ids['FriendEventScreen'].ids['label_to_set'].text = 'Username: '+str(data1)
        if 'event' in data.keys():
            for k,v in data['event'].items():
                for event,value in v.items():
                    B0 = BoxLayout()
                    B0.add_widget(ImageButton(source='icon_px32/'+event+'.png'))
                    B0.add_widget(Label(text=str(value['comment']),font_size= 15,
                            color= (66/255,76/255,80/255,1)))
                    target.add_widget(B0)
                    
                    B = BoxLayout()
                    B.add_widget(ImageButton(source='icon_px32/'+value['unit']+'.png' ))
                    B.add_widget(Label(text=str(value['volumn']),font_size= 30,
                            color= (66/255,76/255,80/255,1)))
                    target.add_widget(B)
                    B2=BoxLayout()
                    test_button =ImageButton(source = 'icon_px32/like.png'
                                            ,on_release=lambda a :print('test')) #亮了
                    #test_button.bind(on_release=lambda a:print('test'))
                    B2.add_widget(test_button)
                    B2.add_widget(Label(text=str(value['like']),font_size= 30,
                            color= (66/255,76/255,80/255,1)))
                    target.add_widget(B2)



class AddEventScreen(Screen):
    
    def trytheprint(self,a,b,c,d):
        try:
            if not a:
                self.ids['volumn'].background_color =(1,0,0,1)
                return
            float(a)
        except Exception:
            self.ids['volumn'].background_color = (1,0,0,1)
            return
        else:
            self.time = ctime()
            self.pattern = re.compile(r'(?<=px32/)\w*')
            self.account = self.parent.ids['LoginScreen'].account
            url = 'https://kivypractice.firebaseio.com/'+self.account+'/event/'+self.time+'.json'
            result = re.findall(self.pattern,c)
            result2 = re.findall(self.pattern,d)
            data = '{"%s":{"volumn":"%s","like":"0","unit":"%s","comment":"%s"}}'%(result2[0],a,result[0],b)
            requests.patch(url,data = data)
            show_AddEventSuccess()


class AddFriendScreen(Screen):
    #if username exist, then add friend to list, return a popup.
    friend_id = ObjectProperty(None)
    def add_friend(self):
        info = self.friend_id.text 
        url = 'https://kivypractice.firebaseio.com/.json'
        result = requests.get(url,timeout=30)
        result = result.content
        data = json.loads(result.decode())
        #print (data)

        if info in data.keys():
            my_id = self.parent.ids['LoginScreen'].account
            data = '{"%s":"0"}'%info
            requests.patch('https://kivypractice.firebaseio.com/'+my_id+'/friend.json',data = data)
            show_AddFriendSuccess()
        else:
            show_AddFriendFailed()

class FriendEventScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass
class ChangeAvatorScreen(Screen):
    pass
class FriendListScreen(Screen):
    pass
class ImageButton(ButtonBehavior,Image):
    pass
class LabelButton(ButtonBehavior,Label):
    pass

if __name__== '__main__':
    GroceryGoApp().run()





