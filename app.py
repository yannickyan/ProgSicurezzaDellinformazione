from pydoc import plain
from cryptography.fernet import Fernet
from django.dispatch import receiver
from Kdc_server import KdcServer
from user import User

if __name__ == "__main__":
    kdc=KdcServer()

    alice_key=Fernet.generate_key()
    f_alice= Fernet(alice_key)
    alice= User("alice",alice_key)


    bob_key= Fernet.generate_key()
    f_bob= Fernet(bob_key)
    bob=User("bob",bob_key)

    # Registred users
    kdc.add_user_key(alice.name,alice_key)
    kdc.add_user_key(bob.name,bob_key)

    #Obtain session key
    session_key, receiver_message= kdc.get_session_key(alice.name,bob.name)
    alice.add_session_key(session_key,bob.name)
    receiver_message= alice.decrypt(receiver_message)
    bob.obtain_session_key(alice.name,receiver_message)

    # send a confidential message
    chiper_text=alice.send_message(b"I LOVE U",bob.name)
    print("%s is sending a confidential message to %s: %s" %  (alice.name,bob.name,chiper_text))
    plain_text=bob.get_message(chiper_text, alice.name)
    print("%s got the following message from %s: %s" % (bob.name,alice.name,plain_text))
    