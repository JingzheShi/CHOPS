import pymysql
class CustomOperation():
    def __init__(self):
        self.MySQLCommand = None
        pass
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            return cursor.fetchall()
        except Exception as e:
            print('-1'+str(e))
            raise e
        
    
    


class CustomTransaction():
    def __init__(self):
        self.is_connecting = False
        print("CustomTransaction init")
        print("Please enter the following database information:")
        self.host = '0' # input("host:")
        if self.host == str(0):
            import os
            with open (("db_api/dbinformation.txt")) as f:
                self.host = f.readline().strip()
                self.port = int(f.readline().strip())
                self.user = f.readline().strip()
                self.db  = f.readline().strip()
                self.password = f.readline().strip()
                print("host:", self.host)
                print("port:", self.port)
                print("user:", self.user)
                print("db:", self.db)

        else:
            self.port = int(input("port:"))
            self.user = input("user:")
            self.db = input("db:")
            self.password = input("password:")

        # connect to database
        self.conn = None
        self.cursor = None
        self.connect()
        
    def connect(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db)
        except:
            raise Exception("Connect to database failed.")
        print("Connect to database successfully.")
        self.cursor = self.conn.cursor()
        
        self.is_connecting = True
        #Obtain the tables in the database
        self.cursor.execute("show tables")
        tables = self.cursor.fetchall()
        print("The tables in the database are:")
        print(tables)
    
    def executeOperation(self,operation:CustomOperation):
        if not self.is_connecting:
            print("Not connecting!")
            return Exception("Not connecting!")

        
        try:
            result = operation.execute(self.cursor)
            return result
        except Exception as e:
            #first catch the exception
            print("Execute operation failed.")
            #rollback
            self.conn.rollback()
            self.conn.close()
            print("Rollback. Remote Closed.")
            raise e
    def executeOperationwitherror(self,operation: CustomOperation):
        if not self.is_connecting:
            print("Not connecting!")
            return Exception("Not connecting!")
        result = operation.execute(self.cursor)
        return result
        
    def __call__(self,*args,**kwargs):
        return self.executeOperation(*args,**kwargs)
    
    def commit(self):
        if not self.is_connecting:
            print("Not connecting!")
            return Exception("Not connecting!")
        try:
            self.conn.commit()
            self.conn.close()
            self.is_connecting = False
            print("Commit successfully. Remote Closed.")
            print("You need to call customTransaction.connect() again to connect to the database.")
        except Exception as e:
            print("Commit failed.")
            raise e
    
    def rollBack(self):
        if not self.is_connecting:
            print("Not connecting!")
            return Exception("Not connecting!")
        try:
            self.conn.rollback()
            self.conn.close()
            self.is_connecting = False
            print("Rollback successfully. Remote Closed.")
            print("You need to call customTransaction.connect() again to connect to the database again.")
        except Exception as e:
            print("Rollback failed.")
            raise e
    def __del__(self):
        if self.is_connecting:
            print("Notice that you have not rollBack or commited the transaction yet.")
            print("Quit without commiting. Roll back.")
            print("You must call customTransaction.commit() to commit your changes.")
            self.conn.rollback()
            self.conn.close()
            self.is_connecting = False
    def commit_and_reconnect(self):
        self.commit()
        self.connect()
    
    


customTransaction = CustomTransaction()

