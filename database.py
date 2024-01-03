
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
                    CREATE TABLE IF NOT EXISTS history(transaction_id int auto_increment primary key,date DATETIME,from_acc int ,to_acc int ,amount int, foreign key (from_acc) references accounts(acc_id), foreign key (to_acc) references accounts(acc_id)
                    )
                    """)
                print("Successfuly initialized tables.")
            
                self.cursor.execute('insert into personal_details values(0,"admin","admin","admin","0")')
                print("Admin Accounts into personal value.")
                self.cursor.execute('insert into accounts values(1,100000000)')
                print("Admin Accounts into accounts")
                self.connection.commit()
                
                self.cursor.execute("SET FOREIGN_KEY_CHECKS=1") #According to google

        except Exception as e:
            print(e)

    def user_check(self,username,password):
        try:
            self.cursor.execute("SELECT password FROM personal_details WHERE username = %s",(username,))
            if self.cursor.fetchall()[0][0] == password:
                return (True,'correct password')
            else:
                return (False,'incorrect password')
        except Exception as e:
            return (False,e)
        
        
        #return True if correct or False

    def acc_id(self,username):
        try:
            self.cursor.execute(f'select acc_id from personal_details where username="{username}"')
            return (True,self.cursor.fetchall()[0][0])
        except Exception as e:
            return (False,e)
        #return tuple(True/False,acc_id)

    def get_account_info(self, acc_id): #returns (true/false,[acc_id,username,name,phone_no,balance])
        try:
            query = f"SELECT acc_id,username,name,phone_no,balance FROM personal_details join accounts on personal_details.acc_id = accounts.acc_id and personal_details.acc_id = {acc_id}"
            self.cursor.execute(query)
            result = self.cursor.fetchall()[0]
            self.cursor = self.connection.cursor()
            if result:
                return (True,result)
            else:
                return (False,None)
        except Exception as e:
            return (False,e)
        
    def name(self,acc_id:int):
        try:
            self.cursor.execute(f'select username from personal_details where acc_id ={acc_id}')
            return (True,self.cursor.fetchall()[0][0])
        except Exception as e:
            return (False,e)
        #return tuple(True/False,name)
        
    def transact(self,from_id,to_id,amount):
        try:
            print(self.balance(from_id)[1])
            if amount>self.balance(from_id)[1]:
                return (False,'insufficient balance')
            self.cursor.execute(f'update accounts set balance = balance + {amount} where acc_id = {to_id}')           
            self.cursor.execute(f'update accounts set balance = balance - {amount} where acc_id = {from_id}')
            self.cursor.execute(f'insert into history (date,from_acc,to_acc,amount) values (now(),{from_id},{to_id},{amount})')
            self.connection.commit()
            return (True,)
        except Exception as e:
            return (False,e)

    def sign_up(self,details):  #details= (username,password,name,number) returns (True/false,)
        try: 
            self.cursor.execute('INSERT INTO personal_details (username,password,name,phone_no) VALUES (%s, %s,%s,%s)',details)
            id = self.cursor.lastrowid
            self.cursor.execute('INSERT INTO accounts values (%s,%s)',(str(id),str(0)))
            self.connection.commit()
            self.cursor = self.connection.cursor()
            return (True,id)
        except Exception as e:
            self.connection.rollback()
            return (False,e)

    def history(self,acc_id,offset,lim): #returns (True,list[list[]]) where each list represents transaction 
        try:
            self.cursor.execute(f'select transaction_id,date,from_acc,a.name,to_acc,b.name,amount from history join personal_details as a on from_acc = a.acc_id and (from_acc = {acc_id} or to_acc = {acc_id}) join personal_details as b on to_acc = b.acc_id limit {lim} offset {offset}')#not sure if works
            return (True,self.cursor.fetchall())
        
        except Exception as e:
            return (False,e)

    def loan(self,acc_id,amount):

        try:
            self.cursor.execute(f'insert into loan (acc_id,amount) values ({acc_id},{amount})')
            
            l_id = self.cursor.lastrowid #code to get L_id of last added record
            l_acc = self.sign_up((f'LOAN_{l_id}','admin',f'bank_loan_{l_id}','NULL'))[1] #code to get bank account of loan use 
            self.cursor.execute(f'update loan set bank_account = {l_acc} where L_id = {l_id}')
            self.transact(1,l_acc,amount)
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
        
    def current_loans(self,acc_id):
        try:
            self.cursor.execute(f'select L_id,amount,balance,amount-balance from loan join accounts where bank_account = accounts.acc_id and loan.acc_id = {acc_id}')
            return (True,self.cursor.fetchall())
        except Exception as e:
            return (False,e)

    def loan_bank_acc(self,l_id):
        try:
            self.cursor.execute(f'select bank_account from loan where L_id = {l_id}')
            return (True,self.cursor.fetchall()[0][0])
        except Exception as e:
            return (False,e)

#d = db('localhost','root','password','tt')
#print(d.balance(2))