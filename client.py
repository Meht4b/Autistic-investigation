import socket
import pickle
import os

username=None
password=None

#default host,port
host ='localhost'
port = 8080

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#function defenitions; most functions returns whatever the server sends 

def connect(def_host,def_port):
    os.system('cls')
    #Connect to server and returns server object
    print("Leave blank for default")
    host = input("Enter host IP Address:")
    port = input("Enter host port:")

    if host == "":
        host=def_host
    if port == "":
        port=def_port

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.connect((host,int(port)))
    socket.setdefaulttimeout(18.5)
    waitForInput=input("Connected. Press Enter to Continue.")
    return server

def login():

    #Asks user if they want to Login/Signup
    #Returns Error/Confirmation message send from server
    os.system('cls')
    YesAccount=input("Login or Signup(L/S):")
    
    if YesAccount.lower() == "l":
        #Login: Sends username and password
        username = input("Enter username")
        password = input("Enter password")
        server.send(pickle.dumps((username,password)))
        serverResponse = pickle.loads(server.recv(4096))
        if serverResponse:
            return ("Login Successful")
        else:
            return ("Error")
              
    else:
        #Signup: Creates account and sends request
            server.send(pickle.dumps("S"))
            print("You are creating a new account")
            username    = input("Enter username:")
            password    = input("Enter password:")
            name        = input("Enter your name:")
            number      = input("Enter your number:")
            l_details   = (username,password,name,number)
            server.send(pickle.dumps(l_details))
            os.system('cls')

            return pickle.loads(server.recv(6940))
            #note to vardhan - implement existing user check case

def transact(reciever:int,amount:float):
    os.system('cls')
    #Sends Transact request with Reciever's Acc_ID and amount to be transferred
    server.send(pickle.dumps(("transact",(reciever,amount))))
    return pickle.loads(server.recv(4096))  # returns whatever the server sends

def withdraw(amount:float):
    os.system('cls')
    #sends withdraw request with amount to be withdrawn
    server.send(pickle.dumps(("withdraw",amount)))
    return pickle.loads(server.recv(4096))  # returns whatever the server sends

def deposit(amount:float):
    os.system('cls')
    #sends deposit request with amount to be deposited
    server.send(pickle.dumps(("deposit",amount)))
    return pickle.loads(server.recv(4096))  # returns whatever the server sends

def loan(amount:float):
    os.system('cls')
    #sends loan request with amount of loan
    server.send(pickle.dumps(("loan",amount)))
    return pickle.loads(server.recv(4096))  # returns whatever the server sends

def balance():
    os.system('cls')
    #sends balance request
    server.send(pickle.dumps(("balance",)))
    return pickle.loads(server.recv(4096))  # returns whatever the server sends

def history():
    os.system('cls')
    #sends history request
    server.send(pickle.dumps((history,())))
    return pickle.loads(server.recv(8192))  # returns whatever the server sends

def lookup(value:int or str):
    #returns corresponding name/acc_id of input value

    #Checks if value is an integer(acc_id); returns corresponding username
    if isinstance(value,int):
        server.send(pickle.dumps(("name",value)))
        return pickle.loads(server.recv(4096))
    
    #checks if value is a string(username); returns corresponding acc_id
    elif isinstance(value,str):
        server.send(pickle.dumps(("acc_id",value)))
        return pickle.loads(server.recv(4096))

def logout():
    os.system('cls')
    #sends disconnect request
    server.send(pickle.dumps(("disconnect",)))
    return "Logged out."

#Main Loop
while True:        
    try:
        while True:

            connect(host,port)
            login()

            print("""Bank Window
            1.Show Balance
            2.Deposit
            3.Withdraw
            4.Send money
            5.Show Transaction History
            6.Logout""")

            ch=int(input("Select Action:"))

            #Checks and calls selected functions along with proper arguments
            if ch == 1:
                print(balance())

            elif ch == 2:
                amt=float(input("Enter amount to be deposited:"))
                print(deposit(amt))
            
            elif ch == 3:
                print(withdraw())
            
            elif ch == 4:
                #User inputs reciever as either acc id or username
                #runs transact() with proper arguments depending on user input


                value = print("Enter reciever's Account ID or username:")
                
                if isinstance(value,int):
                    #Incase user enters acc_id

                    surity = input(f"Are you sure you want to transact to username @{lookup(value)}(Y/N):")
                    if surity.lower in ["yes","y"]:
                        amt = int(input(f"Enter amount to be transferred to {lookup(value)}:"))
                        print(transact(value,amt))

                else:
                    #Incase user enters username
                    surity = print(f"Are you sure you want to transact to Account ID @{lookup(value)}(Y/N):")
                    if surity.lower in ["yes","y"]:
                        amt = int(input(f"Enter amount to be transferred to {value}:"))
                        print(transact(lookup(value),amt))

            elif ch == 5:
                print(history())     
   
            elif ch == 6:
                print(logout())                       

            

    #If any error occurs, print Error and continue the loop
    except Exception as E:
        print(E)
        inp=input("Press Enter to continue.")

