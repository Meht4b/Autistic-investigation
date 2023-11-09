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
        #checks username and password;closes if they do not match
        username,password = pickle.loads(conn.recv(100))

        if database.user_check(username,password):
            conn.send(pickle.dump(True))
            acc_id = database.acc_id(username)

        else:
            conn.send(pickle.dump(False))
            conn.close()
            return None
        
        #request cycle 
        while True:
            req = pickle.load(conn.recv())

            #request = ('transaction','to acc_id','amount')
            if req(0)=='transaction':
                database.transaction(acc_id,req[1],req[2])


    
    except:
        conn.send(pickle.dump(False))
        return None        

#accept connections
while True:
    
    conn,addr = server.accept()

    #create new thread once connnected
    thread = threading.Thread(target=handleClient,args=(conn))
    thread.start()
    