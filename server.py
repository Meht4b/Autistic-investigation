import database 
import socket 
import pickle
import threading 


#initialise server 

host ='localhost'
port = 8080

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))

server.listen()



def handleClient(conn):


    try:

        loginSignup = pickle.loads(conn.recv(100))

        if loginSignup == 'L':
       
            #checks username and password;closes if they do not match
            username,password = pickle.loads(conn.recv(100))

            if database.user_check(username,password):
                conn.send(pickle.dump(True))
                acc_id = database.acc_id(username)

            else:
                conn.send(pickle.dump(False))
                conn.close()
                return None
            
        if loginSignup == 'S':
            
            #sign up
            signupdetail = pickle.load(conn.recv(100))
            database.sign_up(signupdetail)
            acc_id = database.acc_id(signupdetail[0])
           

        
        #request cycle 
        while True:
            req = pickle.load(conn.recv())

            #request = ('transaction','to acc_id','amount')
            if req[0]=='transact':
                conn.send(pickle.dump(database.transact(acc_id,req[1],req[2])))
            
            #withdraw = (withdraw,amount)
            if req[0]=='withdraw':
                conn.send(pickle.dump(database.transact(acc_id,0,req[1])))

            #deposit
            if req[0]=='balance':
                conn.send(pickle.dump(database.balance(acc_id)))

            #history 
            if req[0]=='history':
                conn.send(pickle.dump(database.history(acc_id)))
          
                
    except Exception as e:
        print((addr,username),e)
        conn.send(pickle.dump(False))
        return None        

#accept connections
while True:
    
    conn,addr = server.accept()

    #create new thread once connnected
    thread = threading.Thread(target=handleClient,args=(conn))
    thread.start()
    