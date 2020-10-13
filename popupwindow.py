
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup


class LoginPopup(FloatLayout):
    pass

class RegisterPopup(FloatLayout):
    pass
class RegisterPopupSuccess(FloatLayout):
    pass
class RegisterPopupFailed(FloatLayout):
    pass
class RegisterPopupFailed_no_info(FloatLayout):
    pass
class AddFriendSuccess(FloatLayout):
    pass

class AddFriendFailed(FloatLayout):
    pass
class AddEventSuccess(FloatLayout):
    pass

def show_AddEventSuccess():
    window = AddEventSuccess()
    popwindow = Popup(title='Login Error',content= window,size_hint=(None,None),
                    size=(400,400))
    popwindow.open() 

def show_AddFriendFailed():
    window = AddFriendFailed()
    popwindow = Popup(title='Login Error',content= window,size_hint=(None,None),
                    size=(400,400))
    popwindow.open() 

def show_AddFriendSuccess():
    window = AddFriendSuccess()
    popwindow = Popup(title='Login Error',content= window,size_hint=(None,None),
                    size=(400,400))
    popwindow.open()   
def show_LoginPop():
    window = LoginPopup()
    popwindow = Popup(title='Login Error',content= window,size_hint=(None,None),
                    size=(400,400))
    popwindow.open()

def show_RegisterPopup():
    window = RegisterPopup()
    popwindow = Popup(title='Registration Error',content= window,
                        size_hint=(None,None),size=(400,400))
    popwindow.open()

def show_RegisterPopupSuccess():
    window = RegisterPopupSuccess()
    popwindow = Popup(title='Registration completed',content= window,
                        size_hint=(None,None),size=(400,400))
    popwindow.open()

def show_RegisterPopupFailed():
    window = RegisterPopupFailed()
    popwindow = Popup(title='Registration completed',content= window,
                        size_hint=(None,None),size=(400,400))
    popwindow.open()

def show_RegisterPopupFailed_no_info():
    window = RegisterPopupFailed_no_info()
    popwindow = Popup(title='Registration completed',content= window,
                        size_hint=(None,None),size=(400,400))
    popwindow.open()