from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from datetime import datetime
from pathlib import Path
import glob
import random
from hoverable import HoverBehavior #to make logout button hoverable
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file("design.kv")

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "sign_up_screen"
    def login(self, uname, pword):
        #convert json to python
        with open("users.json") as file:
            users = json.load(file)
        #check if the username and password match those in the dictionary loaded from users.json
        if uname in users and users[uname]["password"] == pword:
            self.manager.current = "login_success_screen"
        else:
            self.ids.login_wrong.text = "Wrong username or password"  '''self refer to this class, THE PYTHON CLASS COMMUNICATE AND SHARE DATA 
                                                                        WITH THE KIVY CLASS OF THE SAME NAME .text change the old text value 
                                                                        of empty string'''



class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        try: #use try except to avoid decoding error caused by empty file
            with open("users.json",'r') as file:
                users = json.load(file) #users signed up already. JSON.LOAD Converts from JSON to Python
        except: #in case user.json is empty, we need to define users so we can add key and value to it later.
            users = {}

        #add new users using python dictionary, preparing data to dump later.
        users[uname] = {'username':uname, 'password': pword,
                            'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")} #2020-11-12 12-59-30 

        with open("users.json", "w") as file:    
            #Convert from Python to JSON
            json.dump(users,file) 
        #there is a bug in visual studio code:json file does not update. Try open json with other app like textedit or note

        #show a new screen
        self.manager.current = "sign_up_success_screen"

class SignUpSuccessScreen(Screen):
    def go_to_login(self):
        #to make it looks like going back to previous page
        self.manager.transition.direction = "right" #default is "left"
        self.manager.current = "login_screen"

class LoginSuccessScreen(Screen):
    def log_out(self):
        #to make it looks like going back to previous page
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    
    def show_one_quote(self,mood):
        mood = mood.lower() #in case user put upper case
        
        moods = glob.glob("quotes/*txt") # a list of all possible files
        moods = [Path(i).stem for i in moods] # this list comprehension extracts the last component of file paths and put them in a list
        

        if mood in moods:
            with open(f"quotes/{mood}.txt") as file:
                quotes = file.readlines()  # this return a list of all the lines in the file
            self.ids.quote.text = random.choice(quotes) #random imported at the begining. 
        else:
            self.ids.quote.text = "Try another feeling"


class ImageButton(ButtonBehavior, HoverBehavior, Image): # inherit from 3 classes. BUTTONBEHAVIOR NEED TO BE THE FIRST OTHERWISE IT MAY NOT BE CLICKEABLE because the order may hide its methods
    pass


class RootWidget(ScreenManager):
    pass



class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()






