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
#^ fix this comment later

def integerize(prompt):
     while True:
            try:
                 return int(input(f"{prompt}:"))
            except ValueError:
                 print("enter number")

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

def login(server):

    #Asks user if they want to Login/Signup
    #Returns Error/Confirmation message send from server
    os.system('cls')
    YesAccount=input("Login or Signup(L/S):")


    if YesAccount.lower() == "l":
        server.send(pickle.dumps('L'))
        #Login: Sends username and password
        username = input("Enter username")
        password = input("Enter password")
        server.send(pickle.dumps((username,password)))
        serverResponse = pickle.loads(server.recv(4096))
        if serverResponse[0]:
            return (True,"Login Successful")
        else:            
            logout()
            return serverResponse #returns error too
              
    else:
        #Signup: Creates account and sends request
            
            print("You are creating a new account")
            username    = input("Enter username:")
            password    = input("Enter password:")
            name        = input("Enter your name:")
            number      = input("Enter your number:")
            l_details   = (username,password,name,number)

            while True:
                if not username.isnumeric():
                    break
                else:
                    print("Username can't be purely numeric.")
                    username = input("Enter username:")
            server.send(pickle.dumps("S"))
            server.send(pickle.dumps(l_details))
            os.system('cls')

            return pickle.loads(server.recv(6940))
            #note to vardhan - implement existing user check case

def transact(reciever:int,amount:float):
    os.system('cls')
    #Sends Transact request with Reciever's Acc_ID and amount to be transferred
    server.send(pickle.dumps(("transact",(reciever,amount))))
    response =  pickle.loads(server.recv(4096))  # returns whatever the server sends
    if response[0]:
        print('transaction succesful')
    else:
        print(response[1])

def withdraw():
    os.system('cls')
    amount = integerize("Enter amount to be withdrawn")
    #sends withdraw request with amount to be withdrawn
    server.send(pickle.dumps(("withdraw",amount)))
    response_withdraw = pickle.loads(server.recv(4096))
    if response_withdraw[0]:
        print(f"Withdrew ${amount}")
    else:
        print(response_withdraw[1])

def deposit():
    os.system('cls')

    amount=integerize("Enter amount to be deposited")
    #sends deposit request with amount to be deposited
    server.send(pickle.dumps(("deposit",amount)))
    deposit_Response = pickle.loads(server.recv(4096)) 
    if deposit_Response[0]:
        print(f"Deposited ${amount}")
    else:
        print(deposit_Response[1])

def loan():
    os.system('cls')
    while True:
        os.system('cls')
        try:
            n = input('1.show current loans \n2.take new loan \n3.pay\n4.return')
            if n == '1':
                server.send(pickle.dumps(('show_loan',)))
                response = pickle.loads(server.recv(1000))
                if response[0]:
                    print('loan id\tamount\tpaid\tleft')
                    for i in response[1]:
                        for j in i:
                            print(j,'\t',end='')
                        print('')

            elif n == '2':
                amount = integerize('enter amount')
                server.send(pickle.dumps(('loan',amount)))
                response = pickle.loads(server.recv(1000))
                if response[0]:
                    print('loan applied succesfuly')
                else:
                    print(response[1])

            elif n == '3':
                l_id = integerize('enter loan id')
                amount = integerize('enter amount to be paid')
                server.send(pickle.dumps(('loan_acc',l_id)))
                response = pickle.loads(server.recv(100))
                if response[0]:
                    l_acc = response[1]
                    transact(l_acc,amount)
                else:
                    print('invalid loan id')
           
            elif n =='4':
                return None
                
        
        except Exception as e:
            print(e)
            
        n = input('enter any key to continue')

def balance():
    os.system('cls')
    #sends balance request
    server.send(pickle.dumps(("balance",)))
    response_Balance = pickle.loads(server.recv(4096))
    print(response_Balance[1])

def history(): #inorder to make it in pages just give offsett as 0 and limit as 100 for now 
    os.system('cls')
    #sends history request
    offset,limit=0,100 # for now
    server.send(pickle.dumps(('history',(offset,limit))))
    response_History = pickle.loads(server.recv(8192))  # returns whatever the server sends
    if response_History[1-1]:
        #print('transaction id\tdate\tfrom acc\tname\t\tto acc\tname\t\tamount')
        for row in response_History[2-1]:
            
            for i in range(len(row)):
                print(row[i],end="\t")

            print('')

def lookup(value:int or str):
    #returns corresponding name/acc_id of input value

    #Checks if value is an integer(acc_id); returns corresponding username
    if isinstance(value,int):
        server.send(pickle.dumps(("name",value)))
        name = pickle.loads(server.recv(4096))
        if not name[0]:
            raise ValueError("Invalid acc_ID")
        else:
            return name[1]
    
    #checks if value is a string(username); returns corresponding acc_id
    elif isinstance(value,str):
        server.send(pickle.dumps(("acc_id",value)))
        name = pickle.loads(server.recv(4096))
        if not name[0]:
            raise ValueError("Invalid acc_ID")
        else:
            return name[1]

def logout():
    os.system('cls')
    #sends disconnect request
    server.send(pickle.dumps(("disconnect",)))
    return "Logged out."

#Main Loop
while True:        
    try:
        server=connect(host,port)
        responseLogin = login(server)
        
        if responseLogin[0]:
            print(responseLogin)
            while True:
                os.system('cls')
                print("""Bank Window
                1.Show Balance
                2.Deposit
                3.Withdraw
                4.Send money
                5.Show Transaction History
                6.loan
                7.Logout""")

                ch=int(input("Select Action:"))

                #Checks and calls selected functions along with proper arguments
                if ch == 1:
                    balance()
                        
                elif ch == 2:
                    deposit()
                
                elif ch == 3:
                    withdraw()
                
                elif ch == 4:
                    #User inputs reciever as either acc id or username
                    #runs transact() with proper arguments depending on user input


                    value = input("Enter reciever's Account ID or username:")
                    
                    if value.isnumeric():
                        #Incase user enters acc_id

                        surity = input(f"Are you sure you want to transact to username @{lookup(int(value))}(Y/N):")
                        if surity.lower() in ["yes","y"]:
                            amt = integerize(f"Enter amount to be transferred to {lookup(int(value))}:")
                            transact(value,amt)

                    else:
                        #Incase user enters username

                        surity = input(f"Are you sure you want to transact to Account ID @{lookup(value)}(Y/N):")
                        if surity.lower() in ["yes","y"]:
                            amt = integerize(f"Enter amount to be transferred to {value}:")
                            transact(lookup(value),amt)

                elif ch == 5:
                    history()
    
                elif ch == 6:
                    loan()

                elif ch == 7:
                    print(logout())  
                    break        

                a = input('enter any key to continue')             

        else:
            print(responseLogin[1])
            ContinueLoop=input("Press Enter to Continue.")
            break
        os.system('cls')

            
    #If any error occurs, print Error and continue the loop
    except Exception as E:
        print(f"Error: {E}")
        inp=input("Press Enter to Continue.")

