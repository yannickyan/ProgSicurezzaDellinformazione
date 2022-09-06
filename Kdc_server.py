from cryptography.fernet import Fernet

class KdcServer:
    "KDC SERVER"
    registered_users= {}
    def __init__(self) -> None:
        pass
    def add_user_key(self,user,secret_key):
        self.registered_users[user]=secret_key
    def get_session_key(self,sender,receiver):
        session_key= Fernet.generate_key()
        f_r= Fernet(self.registered_users[receiver])
        f_s= Fernet(self.registered_users[sender])

        receiver_message=f_r.encrypt(session_key)
        return f_s.encrypt(session_key), f_s.encrypt(receiver_message)   