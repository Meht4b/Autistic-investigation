    #abhishek
import mysql.connector
class db:
    

    def __init__(self,host, user, password, database_name):
        self.host=host
        self.user=user
        self.password=password
        self.database_name=database_name
        try:
            # connection making
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )

            if self.connection.is_connected():
                

                # Create a database
                self.cursor = self.connection.cursor()
                #fix later (abhiske)
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
                self.connection.database = database_name
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS personal_details(username varchar(30) unique,password varchar(30),name varchar(25),phone_no varchar(10),acc_id auto_increment,primary key (acc_id)
                    )
                    """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS accounts(acc_id int primary key,balance int ,foreign key (acc_id) references personal_details(acc_id)
                    
                    )
                    """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS loan(L_id auto_increment ,bank_account int ,acc_id int,amount int,foreign key (acc_id) references personal_details(acc_id),primary key (L_id)
                    
                    )
                    """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS history(transaction_id int primary key,date varchar(20),from_acc int ,to_acc int ,amount int, foreign key (from_acc) references accounts(acc_id), foreign key (to_acc) references accounts(acc_id)
                    )
                    """)
                
            
                self.cursor.execute('insert into personal_details values("admin","admin","admin","0")')
                self.cursor.execute('insert into accounts values(0,1000000000000000)')

                
            
        except Exception as e:
            print(e)

    def user_check(username,password,cursor):
        try:
            cursor.execute(f'SELECT * FROM personal_details WHERE username ={username} AND password = {password}')
            return True
        except Exception:
            return False
        
        #return True if correct or False

    def acc_id(self,username,password,name,phoneno):
        pass
        #return int 

    def name(self,acc_id:int):
        pass
        #return tuple
        
    def transact(self,from_id,to_id,amount):
        pass
        #no tuple

    def sign_up(self,username,passwd,):
        pass
        #no tuple

    def history():
        pass
        #return tuple(tuple)

    def loan(self,acc_id,amount):

        self.cursor.execute(f'insert into loan (acc_id,amount) values ({acc_id},{amount})')
        
        l_id = None #code to get L_id of last added record
        self.sign_up(f'LOAN_{l_id}','admin')
        
        l_acc = None #code to get bank account of loan
        self.transact(0,l_acc,amount)
        self.transact(l_acc,acc_id,amount)