
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
import requests
from kivy.network.urlrequest import UrlRequest
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
import re
from functools import partial


class MainScreen(Screen):
    def refresh_friend_list(self):
        
        to_be_remove = self.parent.ids['FriendListScreen'].ids['ScrollView']
        
        to_be_remove.clear_widgets()
        my_id = self.parent.ids['LoginScreen'].account
        target = self.parent.ids['FriendListScreen'].ids['ScrollView']
        
        url = f'https://kivypractice.firebaseio.com/{my_id}.json'
        result = requests.get(url, timeout=30)
        data = json.loads(result.content.decode())
        
        if 'friend' in data.keys():
            for k in data['friend']:
                url = f'https://kivypractice.firebaseio.com/' + k + '.json'
                self.response = UrlRequest(url,timeout=10,on_success= partial(self.get_result,k,target))
        else:
            pass

            
    def get_result(self,k,target,thread,args):
        #print(self.parent)#之所以找不到parent是因为这个方法没有在kv里面调用!!!!又搞清楚了一个问题

        data = thread.result
        B = BoxLayout()
        imagebutton = Special_ImageButton(
            source='icon_px32/' + data['avator'] + '.png', text='%s' % k)
        B.add_widget(imagebutton)
        B.add_widget(Label(text='%s' % k, font_size=20,
                           color=(66 / 255, 76 / 255, 80 / 255, 1)))
        target.add_widget(B)
        
       
    def config_dropdown(self):

        location = self.parent.ids['AddEventScreen'].ids['desti2']
        location.clear_widgets()

        self.target2 = MyDropDown2()
        # ,text='choose one')#,pos_hint={'top':0.6,'right':0.6})
        self.Mainbutton2 = ImageButton(
            source='icon_px32/gear.png', id='firstdropdown')
        self.Mainbutton2.bind(on_release=self.target2.open)
        location.add_widget(self.Mainbutton2)
        self.target2.bind(on_select=lambda instance,
                          x: setattr(self.Mainbutton2, 'source', x))

        self.target = MyDropDown()
        # ,text='choose one')#,pos_hint={'top':0.6,'right':0.6})
        self.Mainbutton = ImageButton(
            source='icon_px32/gear.png', id='seconddropdown')
        self.Mainbutton.bind(on_release=self.target.open)
        location.add_widget(self.Mainbutton)
        self.target.bind(on_select=lambda instance,
                         x: setattr(self.Mainbutton, 'source', x))


class Special_ImageButton(Image, Button):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class LabelButton(ButtonBehavior, Label):
    pass


class MyDropDown(DropDown):
    pass


class MyDropDown2(DropDown):
    pass
