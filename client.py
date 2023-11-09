import socket
import pickle

username=None
password=None

host ='localhost'
port = 8080

#Connect to server
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((host,port))
socket.setdefaulttimeout(18.5)


try:

    #Check if user has an account, if not create account and save in binary file
    try:
        f = open('localdat','rb')
        data = pickle.load(f)                  #data=(username,password)
        username = pickle.load(f)[0]
        password = pickle.load(f)[1]

        server.send(pickle.dump(username,password,"L"))
        response = pickle.load(server.recv(6940))


        
        #attempts to read local file and login

    except FileNotFoundError:
        f = open('locahost','wb')
        print("You are creating a new account")
        username = input("Enter username:")
        password = input("Enter password:")
        name = input("Enter your name:")
        number = input("Enter your number:")
        l_details = (username,password,name,number)
        server.recv()

        pickle.dump(l_details,f)
        server.send(pickle.dump(username,password,"S"))
        server.send(pickle.dump(l_details))
        #Creates account and sends request

    while True:
        pass        
except Exception as doramon:
    print(doramon)

