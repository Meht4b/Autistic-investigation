import socket
import pickle

username=None
password=None

#Check if user has an account, if not create account and save in binary file

try:
    f = open('localdat','rb')
    data = pickle.load(f)                  #data=(username,password)
    username,password=pickle.load(f)[0],pickle.load(f)[1]

except FileNotFoundError:
    f=open('locahost','wb')
        

#Login
def login():
