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
        else:
            conn.send(pickle.dump(False))
            conn.close()
            return None
        
    
    except:
        conn.send(pickle.dump(False))
        return None        

#accept connections
while True:
    
    conn,addr = server.accept()

    #create new thread once connnected
    thread = threading.Thread(target=handleClient,args=(conn))
    thread.start()
    