from db_api import *
class GetSchoolInfoByName(CustomOperation):
    def __init__(self,Name:str):
        self.MySQLCommand = "select * from cmf_tp_school where `school_name`='{}'".format(Name)
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'school_name':item[1],'area_id':item[2]})
            return returned_lst
        except Exception as e:
            print('-10'+str(e))
            raise e

class GetSchoolInfoByFlexibleName(CustomOperation):
    def __init__(self,Name:str):
        self.MySQLCommand = "select * from cmf_tp_school where `school_name` like '%{}%'".format(Name)
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'school_name':item[1],'area_id':item[2]})
            return returned_lst
        except Exception as e:
            print('-11'+str(e))
            raise e