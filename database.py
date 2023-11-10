    #abhishek
import mysql.connector
class db:
    

    def __init__(self,host, user, password, database_name, ):
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
                    CREATE TABLE IF NOT EXISTS personal_details(username varchar(30) unique,password varchar(30),name varchar(25),phone_no varchar(10),primary key (acc_id),acc_id int auto_increment
                    )
                    """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS accounts(acc_id int primary key,balance int ,foreign key (acc_id) refrences personal_details(acc_id)
                    
                    )
                    """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS loan(bank_account int primary key,acc_id int,amount int,foreign key (acc_id) refrences personal_details(acc_id)
                    
                    )
                    """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS history(transaction_id int primary key,date varchar(20),from int ,to int ,amount int, foreign key (from) refrences accounts(acc_id), foreign key (to) refrences accounts(acc_id)
                    )
                    """)
                
            
                self.cursor.execute('insert into personal_details values("admin","admin","admin","0")')
                self.cursor.execute('insert into accounts values(0,1000000000000000)')

                
            
        except Exception as vardhan:
            print('vardhan')

    def user_check(username,password,cursor):
        try:
            cursor.execute(f'SELECT * FROM personal_details WHERE username ={username} AND password = {password}')
            return True
        except Exception:
            return False
        
        #return True if correct or False

    def acc_id(username):
        pass
        #return int 

    def name(acc_id:int):
        pass
        #return tuple
        
    def transact(from_id,to_id,amount):
        pass
        #no tuple

    def sign_up():
        pass
        #no tuple

    def history():
        pass
        #return tuple(tuple)

    def loan(self,acc_id,amount):
        #create new account for loan bank account thing
        self.transact(0,acc_id,amount)
        #create new record 