from db_api import *
class GetAreaInfoByName(CustomOperation):
    def __init__(self,Name:str):
        self.MySQLCommand = "select * from cmf_tp_area where `area` = \'{}\' ; ".format(Name)
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'area_name':item[1]})
            return returned_lst
        except Exception as e:
            print('-5'+str(e))
            raise e

class GetAllAreaNamesAndAreaIdsAsDict(CustomOperation):
    def __init__(self):
        self.MySQLCommand = "select * from cmf_tp_area ; "
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_dict = {}
            for item in returned:
                returned_dict.update({item[1]:item[0]})
            return returned_dict
        except Exception as e:
            print('-8'+str(e))
            raise e





