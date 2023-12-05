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
                password=password,
                auth_plugin='mysql_native_password' #can delete if not work
            )

            if self.connection.is_connected():
                

                # Create a database
                self.cursor = self.connection.cursor()
                #fix later (abhiske)
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
                self.connection.database = database_name
                self.cursor.execute("SET FOREIGN_KEY_CHECKS=0") #According to google
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS personal_details(acc_id int auto_increment primary key,username varchar(30) unique,password varchar(30),name varchar(25),phone_no varchar(10)
                    )
                    """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS accounts(acc_id int primary key,balance int ,foreign key (acc_id) references personal_details(acc_id)
                    
                    )
                    """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS loan(L_id int auto_increment primary key,bank_account int ,acc_id int,amount int,foreign key (acc_id) references personal_details(acc_id)
                    
                    )
                    """)
                self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS history(transaction_id int primary key,date varchar(20),from_acc int ,to_acc int ,amount int, foreign key (from_acc) references accounts(acc_id), foreign key (to_acc) references accounts(acc_id)
                    )
                    """)
                print("Successfuly initialized tables.")
            
                self.cursor.execute('insert into personal_details values(0,"admin","admin","admin","0")')
                print("Admin Accounts into personal value.")
                self.cursor.execute('insert into accounts values(0,100000000)')
                print("Admin Accounts into accounts")
                self.connection.commit()
                
                self.cursor.execute("SET FOREIGN_KEY_CHECKS=1") #According to google
                print('hello')
            
        except Exception as e:
            print(e)

    def user_check(self,username,password):
        try:
            self.cursor.execute("SELECT password FROM personal_details WHERE username = %s",(username,))
            if self.cursor.fetchone()[0] == password:
                return (True,'correct password')
            else:
                return (False,'incorrect password')
        except Exception as e:
            return (False,e)
        
        
        #return True if correct or False

    def acc_id(self,username):
        try:
            self.cursor.execute(f'select acc_id from personal_details where username={username}')
            return (True,self.cursor.fetchone()[0])
        except Exception as e:
            return (False,e)
        #return tuple(True/False,acc_id)

    def get_account_info(self, username):
        try:
            query = f"SELECT * FROM personal_details WHERE username = '{username}'"
            self.cursor.execute(query)
            result = self.cursor.fetchone()

            if result:
                account_info = {
                    'username': result[0],  
                    'full_name': result[4],  
                    'email': result['?'],  
                    
                }
                return (True,account_info)
            else:
                return (False,None)
        except Exception as e:
            return (False,e)
        
    def name(self,acc_id:int):
        try:
            self.cursor.execute(f'select username from personal_details where acc_id ={acc_id}')
            return (True,self.cursor.fetchone()[0])
        except Exception as e:
            return (False,e)
        #return tuple(True/False,name)
        
    def transact(self,from_id,to_id,amount):
        try:
            self.cursor.execute(f'update accounts set balance = balance + {amount} where acc_id = {to_id}')
            self.cursor.execute(f'update accounts set balance = balance - {amount} where acc_id = {from_id}')
            return (True,)
        except Exception as e:
            return (False,e)

    def sign_up(self,details):  
        try: #details= (username,password,name,number)
            self.cursor.execute('INSERT INTO personal_details (username,password,name,phone_no) VALUES (%s, %s,%s,%s)',details)
            id = self.cursor.lastrowid
            self.cursor.execute('INSERT INTO accounts values (%s,%s)',(str(id),str(0)))
            self.connection.commit()
            return (True,id)
        except Exception as e:
            self.connection.rollback()
            return (False,e)

    def history(self,acc_id,offset,lim):
        try:
            self.cursor.execute(f'select transaction_id,date,from_acc,a.name,to_acc,b.name where from_acc = {acc_id} or to_acc = {acc_id} join personal_details as a on from_acc = a.acc_id join personal_details as b on to_acc = b.acc_id limit {lim} offset {offset}')#not sure if works
            return (True,self.cursor.fetchall())
        except Exception as e:
            return (False,e)

    def loan(self,acc_id,amount):

        try:
            self.cursor.execute(f'insert into loan (acc_id,amount) values ({acc_id},{amount})')
            
            l_id = self.cursor.lastrowid #code to get L_id of last added record
            l_acc = self.sign_up((f'LOAN_{l_id}','admin',f'bank_loan_{l_id}','NULL')) #code to get bank account of loan use fetchone

            self.transact(0,l_acc,amount)
            self.transact(l_acc,acc_id,amount)

            return (True,)
        except Exception as e:
            return (False,e)
        
    def balance(self,acc_id):
        try:
            self.cursor.execute(f'select balance from accounts where acc_id = "{acc_id}"')
            return (True,self.cursor.fetchall()[0][0])
        except Exception as e:
            return (False, e)