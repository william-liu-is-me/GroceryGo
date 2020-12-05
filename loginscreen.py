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
from kivy.network.urlrequest import UrlRequest
from kivy.lang import Builder

from functools import partial
#from firebase import firebase


class LoginScreen(Screen):
    user = ObjectProperty(None)
    passw = ObjectProperty(None)
    account = ''

    def check(self):
        avator = self.parent.ids['MainScreen'].ids['ImageButton1']
        avator_in_settings = self.parent.ids['ChangeAvatorScreen'].ids['avator']
        url = 'https://kivypractice.firebaseio.com/.json'
        result = requests.get(url,timeout= 15)

        data = json.loads(result.content.decode())
        #print(data)
        #so here is where we will config the app for each specific account.
        for k,v in data.items():
            if k == self.user.text and self.passw.text ==v['password']:# and v == self.passw.text:
                self.account = k
                self.user.text =''
                self.passw.text = ''
                self.parent.ids['MainScreen'].ids['test'].text = 'Username: '+k
                self.parent.ids['FriendListScreen'].ids['test'].text = 'Username: '+k
                if 'event' in v.keys():
                    self.GroceryBanner(v)
                image = v['avator']
                avator.source = 'icon_px32/'+image+'.png'
                #set avator change page avator image
                avator_in_settings.source = 'icon_px32/'+image+'.png'
                loca = self.parent.ids['FriendListScreen'].ids['ImageButton1']
                loca.source='icon_px32/'+image+'.png'
                return True
        show_LoginPop()
        return False
    def test(self):
        print('success')
    def GetAvator(self,args):
        url = f'https://kivypractice.firebaseio.com/{args}.json'
        try:
            r = requests.get(url, timeout=30)
            r.encoding = 'utf-8'
            return r.content
        except:
            print('error when requesting info from database')
        #以后这里需要改进？不一定，实际上只request了一次，然后就成为本地的资料了，
    def GroceryBanner(self,data):
        #this data is the orignial json dictionary
        target = self.parent.ids['MainScreen'].ids['ScrollView']
        for k,v in data['event'].items():
            for event,value in v.items():      
                B0 = BoxLayout()
                B0.add_widget(ImageButton(source='icon_px32/'+event+'.png'))
                B0.add_widget(Label(text=str(value['comment']),font_size= 15,
                        color= (66/255,76/255,80/255,1)))
                target.add_widget(B0)#
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

    def FriendBanner(self,data):
        pass

class ImageButton(ButtonBehavior,Image):
    pass
