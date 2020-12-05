from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, SwapTransition, FadeTransition, FallOutTransition, RiseInTransition, CardTransition, NoTransition

from kivy.properties import ObjectProperty, StringProperty, ListProperty  # ,NumericProperty
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
# from firebase import firebase
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

        return GroceryGoScreenManager(transition=FadeTransition())


class GroceryGoScreenManager(ScreenManager):
    def FriendGroceryBanner(self, data1):
        # print(self)

        url = 'https://kivypractice.firebaseio.com/' + data1 + '.json'
        result = requests.get(url, timeout=15)
        data = json.loads(result.content.decode())

        target = self.ids['FriendEventScreen'].ids['ScrollView']
        target.clear_widgets()
        self.ids['FriendEventScreen'].ids['image_to_set'].source = 'icon_px32/' + \
            data['avator'] + '.png'
        self.ids['FriendEventScreen'].ids['label_to_set'].text = 'Username: ' + \
            str(data1)
        if 'event' in data.keys():
            for k, v in data['event'].items():
                for event, value in v.items():
                    B0 = BoxLayout()
                    B0.add_widget(ImageButton(
                        source='icon_px32/' + event + '.png'))
                    B0.add_widget(Label(text=str(value['comment']), font_size=15,
                                        color=(66 / 255, 76 / 255, 80 / 255, 1)))
                    target.add_widget(B0)

                    B = BoxLayout()
                    B.add_widget(ImageButton(
                        source='icon_px32/' + value['unit'] + '.png'))
                    B.add_widget(Label(text=str(value['volumn']), font_size=30,
                                       color=(66 / 255, 76 / 255, 80 / 255, 1)))
                    target.add_widget(B)
                    B2 = BoxLayout()
                    test_button = ImageButton(
                        source='icon_px32/like.png', on_release=lambda a: print('test'))  # 亮了
                    # test_button.bind(on_release=lambda a:print('test'))
                    B2.add_widget(test_button)
                    B2.add_widget(Label(text=str(value['like']), font_size=30,
                                        color=(66 / 255, 76 / 255, 80 / 255, 1)))
                    target.add_widget(B2)


class AddEventScreen(Screen):

    def trytheprint(self, a, b, c, d):
        try:
            if not a:
                self.ids['volumn'].background_color = (1, 0, 0, 1)
                return
            float(a)
        except Exception:
            self.ids['volumn'].background_color = (1, 0, 0, 1)
            return
        else:
            self.time = ctime()
            self.pattern = re.compile(r'(?<=px32/)\w*')
            self.account = self.parent.ids['LoginScreen'].account
            url = 'https://kivypractice.firebaseio.com/' + \
                self.account + '/event/' + self.time + '.json'
            result = re.findall(self.pattern, c)
            result2 = re.findall(self.pattern, d)
            show_AddEventSuccess()
            data = '{"%s":{"volumn":"%s","like":"0","unit":"%s","comment":"%s"}}' % (
                result2[0], a, result[0], b)
            requests.patch(url, data=data)


class AddFriendScreen(Screen):
    # if username exist, then add friend to list, return a popup.
    friend_id = ObjectProperty(None)

    def add_friend(self):
        info = self.friend_id.text
        url = 'https://kivypractice.firebaseio.com/.json'
        result = requests.get(url, timeout=30)
        result = result.content
        data = json.loads(result.decode())
        # print (data)

        if info in data.keys():
            my_id = self.parent.ids['LoginScreen'].account
            data = '{"%s":"0"}' % info
            requests.patch('https://kivypractice.firebaseio.com/' +
                           my_id + '/friend.json', data=data)
            show_AddFriendSuccess()
        else:
            show_AddFriendFailed()


class FriendEventScreen(Screen):
    pass


class SettingsScreen(Screen):
    def create_avator_list(self):
        self.my_icon_list = ['bird', 'boy', 'cat', 'crab', 'dog',
                             'fish', 'girl', 'man', 'panda', 'squid', 'woman', 'squid']
        target_change_avator = self.parent.ids['ChangeAvatorScreen'].ids['ScrollViewChangeAvator']
        target_change_avator.clear_widgets()
        for item in self.my_icon_list:
            img = ImageButton(source='icon_px32/' + f'{item}.png', id=item,
                              on_release=partial(self.change_avator, item))
            target_change_avator.add_widget(img)

    def change_avator(self, image, item_id):
        # change avator
        # 这里pic参数是个tuple 需要用两个参数分开，不然会出错 2 positional but 3 given
        self.app = App.get_running_app().root

        avator = self.app.ids['MainScreen'].ids['ImageButton1']
        avator_in_list = self.app.ids['FriendListScreen'].ids['ImageButton1']
        avator.source = 'icon_px32/' + image + '.png'
        avator_in_list.source = 'icon_px32/' + image + '.png'
        setting_avator = self.app.ids['ChangeAvatorScreen'].ids['avator']
        setting_avator.source = 'icon_px32/' + image + '.png'
        # update firebase

        data = '{"avator":"%s"}' % image
        requests.patch('https://kivypractice.firebaseio.com/' +
                       self.app.ids['LoginScreen'].account + '.json', data=data)


class ChangeAvatorScreen(Screen):
    pass


class FriendListScreen(Screen):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class LabelButton(ButtonBehavior, Label):
    pass


if __name__ == '__main__':
    GroceryGoApp().run()
