from cryptography.fernet import Fernet
from django.dispatch import receiver

class User:
    "USER"
    session_keys={}

    def __init__(self,name,secret_key):
        self.name=name
        self.secret_key= secret_key
        self.f= Fernet(secret_key)

    def add_session_key(self,session_key,receiver):
        self.session_keys[receiver]=self.f.decrypt(session_key)

    def obtain_session_key(self,sender,message):
        self.session_keys[sender]=self.f.decrypt(message)
    
    def decrypt(self,message):
       return self.f.decrypt(message)

    def send_message(self,message,receiver):
        f_r=Fernet(self.session_keys[receiver])
        return f_r.encrypt(message)
