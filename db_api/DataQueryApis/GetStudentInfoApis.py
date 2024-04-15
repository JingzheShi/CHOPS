from db_api import *
class GetStudentInfoByName(CustomOperation):
    def __init__(self,Name:str):
        self.MySQLCommand = "select * from cmf_tp_student where `name` = \'{}\' ; ".format(Name)
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'teacher_id':item[1],'student_name':item[2],'school_id':item[3]})
            return returned_lst
        except Exception as e:
            print('-13'+str(e))
            raise e

class GetStudentInfoByFlexibleName(CustomOperation):
    def __init__(self,Name:str):
        self.MySQLCommand = "select * from cmf_tp_student where `name` like \'%{}%\' ; ".format(Name)
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'teacher_id':item[1],'student_name':item[2],'school_id':item[3]})
            return returned_lst
        except Exception as e:
            print('-12'+str(e))
            raise e

class GetStudentInfoBySchoolId(CustomOperation):
    def __init__(self,SchoolId:int):
        self.MySQLCommand = "select * from cmf_tp_student where `school` = {}".format(SchoolId)
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'teacher_id':item[1],'student_name':item[2],'school_id':item[3]})
            return returned_lst
        except Exception as e:
            print('-13'+str(e))
            raise e