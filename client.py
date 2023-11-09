import socket
import pickle

username=None
password=None

host ='localhost'
port = 8080

def connect(host,port):

    #Connect to server
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((host,port))
    socket.setdefaulttimeout(18.5)

    return server

def login():

    #Check if user has an account, if not create account and save in binary file
    try:
        f           = open('localdat','rb')

        username    = pickle.load(f)[0]
        password    = pickle.load(f)[1]

        server.send(pickle.dump(username,password,"L"))
        response    = pickle.load(server.recv(6940))

        if response[0]==True:
            print(response[1])
        elif response[0]==False:
            print(response[1])


        
        #attempts to read local file and login

    except FileNotFoundError:
        f = open('locahost','wb')
        print("You are creating a new account")
        username    = input("Enter username:")
        password    = input("Enter password:")
        name        = input("Enter your name:")
        number      = input("Enter your number:")
        l_details   = (username,password,name,number)

        pickle.dump(l_details,f)
        server.send(pickle.dump(username,password,"S"))
        server.send(pickle.dump(l_details))
        response    = pickle.load(server.recv(6940))



        #Creates account and sends request

def transact(reciever,amount):
    server.send(pickle.dump("transact",(to,amount)))

def withdraw()
        



(withdraw,(amount))
(deposit,(amount))
(history,())
(loan,(amount))