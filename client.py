import socket
import pickle

username=None
password=None

host ='localhost'
port = 8080
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def connect(host,port):

    #Connect to server and returns server object
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((host,port))
    socket.setdefaulttimeout(18.5)

    return server

def login():

    #Check if user has an account, if not create account and save in binary file
    try:

        #attempts to read local file and login
        f = open('localdat','rb')

        username = pickle.load(f)[0]
        password = pickle.load(f)[1]

        server.send(pickle.dump(username,password,"L"))
        response = pickle.load(server.recv(6940))

        if response[0] == True:
            print(response[1])
        elif response[0] == False:
            print(response[1])
              
    except FileNotFoundError:
        
        #Creates account and sends request
        with open('locahost','wb') as f:
            print("You are creating a new account")
            username    = input("Enter username:")
            password    = input("Enter password:")
            name        = input("Enter your name:")
            number      = input("Enter your number:")
            l_details   = (username,password,name,number)

            pickle.dump(l_details,f)
            server.send(pickle.dump((username,password,"S")))
            server.send(pickle.dump(l_details))
            response = pickle.load(server.recv(6940))



def transact(reciever:int,amount:float):
    #Sends Transact request with Reciever's Acc_ID and amount to be transferred
    server.send(pickle.dump(("transact",(reciever,amount))))
    return pickle.load(server.recv)

def withdraw(amount:float):
    #sends withdraw request with amount to be withdrawn
    server.send(pickle.dump(("withdraw",amount)))
    return pickle.load(server.recv)

def deposit(amount:float):
    #sends deposit request with amount to be deposited
    server.send(pickle.dump(("deposit",amount)))
    return pickle.load(server.recv)

def loan(amount:float):
    #sends loan request with amount of loan
    server.send(pickle.dump(("loan",amount)))
    return pickle.load(server.recv)

def balance():
    #sends balance request
    server.send(pickle.dump(("balance",())))
    return pickle.load(server.recv)

def history():
    #sends history request
    server.send(pickle.dump((history,())))
    return pickle.load(server.recv)

def lookup(value:int or str):
    if isinstance(value,int):
        server.send(pickle.dump(("name",value)))
        return pickle.load(server.recv)
    
    elif isinstance(value,str):
        server.send(pickle.dump(("acc_id",value)))
        return pickle.load(server.recv)

def logout():
    server.send(pickle.dump("disconnect",()))
    return pickle.load(server.recv)


while True:        
    try:
        while True:
            print("""Bank Window
            1.Show Balance
            2.Deposit
            3.Withdraw
            4.Send money
            5.Show Transaction History
            6.Logout""")
            ch=int(input("Select Action"))


            if ch == 1:
                print(balance())

            elif ch == 2:
                amt=float(input("Enter amount to be deposited"))
                print(deposit(amt))
            
            elif ch == 3:
                print(withdraw())
            
            elif ch == 4:
                while True:
                    value = print("Enter reciever's Account ID or username:")
                    
                    if isinstance(value,int):
                        
                        surity = input(f"Are you sure you want to transact to username @{lookup(value)}(Y/N):")
                        if surity.lower in ["yes","y"]:
                            amt = int(input(f"Enter amount to be transferred to {lookup(value)}:"))
                            print(transact(value,amt))

                    else:

                        surity = print(f"Are you sure you want to transact to Account ID @{lookup(value)}(Y/N):")
                        if surity.lower in ["yes","y"]:
                            amt = int(input(f"Enter amount to be transferred to {value}:"))
                            print(transact(lookup(value),amt))

            elif ch == 5:
                print(history())        
            elif ch == 6:
                print(logout())                       

            


    except Exception as E:
        print(E)

