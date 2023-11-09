    #abhishek
import mysql.connector
class db:
    

    def __int__(self,host, user, password, database_name, ):
        try:
            # connection making
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )

            if connection.is_connected():
                

                # Create a database
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS personal_details(username varchar(30) unique,password varchar(30),name varchar(25),phone_no varchar(10),primary key (acc_id),acc_id int auto_increment
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS accounts(acc_id int primary key,balance int ,foreign key (acc_id) refrences personal_details(acc_id)
                    
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS loan(bank_account int primary key,acc_id int,amount int,foreign key (acc_id) refrences personal_details(acc_id)
                    
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS history(transaction_id int primary key,date varchar(20),from int ,to int ,amount int, foreign key (from) refrences accounts(acc_id), foreign key (to) refrences accounts(acc_id)
                    )
                    """,
                    )
                
            
                cursor.execute('insert into personal_details values("admin","admin","admin","0")')
                cursor.execute('insert into accounts values(0,1000000000000000)')
                return cursor

                
            
        except Exception as vardhan:
            print('vardhan')

    def user_check(username,password):
        
        pass
        #return True or False

    def acc_id(username):
        pass
        #return int 

    def transact(from_id,to_id,amount):
        pass
        #no return

    def sign_up():
        pass
        #no return

    def history():
        pass
        #return tuple(tuple)