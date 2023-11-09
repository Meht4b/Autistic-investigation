import database 
import socket 
import pickle
import threading 

host ='localhost'
port = 8080

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))

server.listen()

def handleClient(conn):

    try:
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


while True:
    
    conn,addr = server.accept()
    thread = threading.Thread(target=handleClient,args=(conn))
    thread.start()
    