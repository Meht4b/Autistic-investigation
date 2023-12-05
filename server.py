import database as data_base
import socket 
import pickle
import threading 


#initialise server 

host ='localhost'
port = 8080

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))

#disconnect function:
def disconnect(conn,message):
    conn.send(pickle.dumps(("Disconnect",message)))
    conn.close
    return True

server.listen()
#(self,host, user, password, database_name, )
database = data_base.db('localhost','root','chungus','doraemon')

print('listening')

def handleClient(conn,addr):


    try:

        loginSignup = pickle.loads(conn.recv(100))
        print(loginSignup)

        if loginSignup == 'L':
            print("L recieved")
            #checks username and password;closes if they do not match
            username,password = pickle.loads(conn.recv(100))

            if database.user_check(username,password):
                conn.send(pickle.dumps(True))
                acc_id = database.acc_id(username)

            else:
                conn.send(pickle.dumps(False))
                conn.close()
                return None
            
        if loginSignup == 'S':
            print("S recieved")
            #sign up
            signupdetail = pickle.loads(conn.recv(100))
            conn.send(pickle.dumps(database.sign_up(signupdetail)))
            acc_id = database.acc_id(signupdetail[0])
            #note to mehtab-> implement check for existing user while signup
           

        
        #request cycle 
        while True:
            req = pickle.loads(conn.recv(5000))

            #request = ('transaction',('to acc_id','amount'))
            if req[0]=='transact':
                conn.send(pickle.dumps(database.transact(acc_id,req[1][1],req[1][2])))
            
            #withdraw = (withdraw,amount)
            elif req[0]=='withdraw':
                conn.send(pickle.dumps(database.transact(acc_id,0,req[1])))

            #deposit = (deposit,amount)
            elif req[0]=='deposit':
                conn.send(pickle.dumps(database.transact(0,acc_id,req[1])))
            
            #balance
            elif req[0]=='balance':
                conn.send(pickle.dumps(database.balance(acc_id)))

            #history 
            elif req[0]=='history':
                conn.send(pickle.dumps(database.history(acc_id)))

            elif req[0]=='name':
                conn.send(pickle.dumps(database.name(req[1])))
            
            elif req[0]=='acc_id':
                conn.send(pickle.dumps(database.acc_id(req[1])))
            
            elif req[0]=='loan':
                conn.send(pickle.dumps(database.loan(database,acc_id,req[1])))

            elif req[0]=='disconnect':
                disconnect(conn,"Connection Terminated")
            
            else:
                conn.send(pickle.dumps((False,'bad request')))
                
    except Exception as e:
        print(e)
        return None        

#accept connections
while True:
    
    conn,addr = server.accept()
    print(conn,addr)
    #create new thread once connnected
    thread = threading.Thread(target=handleClient,args=(conn,addr))
    thread.start()
    