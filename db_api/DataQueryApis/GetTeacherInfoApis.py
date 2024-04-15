#CustomOperation is defined in db_api\CustomOperation.py
from db_api import *
typedict={2:'arbiter',3:'vice_teamleader',1:'teamleader'}
class GetAllTeacherInfo(CustomOperation):
    def __init__(self):
        super().__init__()
        self.MySQLCommand = "select * from cmf_tp_member where status != 0"
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'p_id':item[1],'wechat_nickname':item[9],'user_name':item[2],'school_id':item[3],'upload_limit':item[7],'viewing_problem':item[4],'type':typedict[item[6]]})
            return returned_lst
        except Exception as e:
            print('-14'+str(e))
            raise e
class GetTeacherInfoByName(CustomOperation):
    def __init__(self, Name:str):
        super().__init__()
        self.MySQLCommand = "select * from cmf_tp_member where user_name = '%s' and status != 0 " % Name
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'p_id':item[1],'wechat_nickname':item[9],'user_name':item[2],'school_id':item[3],'upload_limit':item[7],'viewing_problem':item[4],'type':typedict[item[6]]})
            return returned_lst
        except Exception as e:
            print('-15'+str(e))
            raise e
        
class GetTeacherInfoByNameByUser(CustomOperation):
    def __init__(self, userID:int, Name:str):
        super().__init__()
        self.userID = userID
        self.name = Name
        self.MySQLCommand = "select * from cmf_tp_member where user_name = '%s' and status != 0 " % Name
    def execute(self, cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_admin where user_id = {}".format(self.userID))
        result = cursor.fetchall()
        assert len(result) == 1, "The user giving such query is not an admin and you do not have the right to see information in the system!"
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'p_id':item[1],'wechat_nickname':item[9],'user_name':item[2],'school_id':item[3],'upload_limit':item[7],'viewing_problem':item[4],'type':typedict[item[6]]})
            if len(returned_lst) == 0:
                    return "There is no such user in the system whose name is "+self.name
            return returned_lst
        except Exception as e:
            print('-15'+str(e))
            raise e
class GetTeacherInfoByWechatName(CustomOperation):
    def __init__(self, Name:str):
        super().__init__()
        self.MySQLCommand = "select * from cmf_tp_member where `nickname` = '%s' and status != 0" % Name
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            # print(returned)
            for item in returned:
                returned_lst.append({'id':item[0],'p_id':item[1],'wechat_nickname':item[9],'user_name':item[2],'school_id':item[3],'upload_limit':item[7],'viewing_problem':item[4],'type':typedict[item[6]]})
            return returned_lst
        except Exception as e:
            print('-16'+str(e))
            raise e
class GetTeacherInfoByFlexibleName(CustomOperation):
    def __init__(self, Name:str):
        '''
        Name: str
        return: list, each element is a dictionary.
            item in list: dictionary with 
        '''
        super().__init__()
        self.MySQLCommand = "select * from cmf_tp_member where user_name like '%%%s%%' and status != 0" % Name
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'p_id':item[1],'wechat_nickname':item[9],'user_name':item[2],'school_id':item[3],'upload_limit':item[7],'viewing_problem':item[4],'type':typedict[item[6]]})
            return returned_lst
        except Exception as e:
            print('-17'+str(e))
            raise e

class GetTeacherInfoBySchoolId(CustomOperation):
    def __init__(self,SchoolId:int):
        self.MySQLCommand = "select * from cmf_tp_member where school_id = %d and status != 0" % SchoolId
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'p_id':item[1],'wechat_nickname':item[9],'user_name':item[2],'school_id':item[3],'upload_limit':item[7],'viewing_problem':item[4],'type':typedict[item[6]]})
            return returned_lst
        except Exception as e:
            print('-18'+str(e))
            raise e

class GetTeacherInfoBySchoolNameByUser(CustomOperation):
    def __init__(self, userID:int, schoolName:str):
        self.userID = userID
        self.schoolName = schoolName
    def execute(self, cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_admin where user_id = {}".format(self.userID))
        result = cursor.fetchall()
        assert len(result) == 1, "The user giving such query is not an admin and you do not have the right to see information in the system!"
        cursor.execute("select * from cmf_tp_school where school_name = \'{}\'".format(self.schoolName))
        result = cursor.fetchall()
        if len(result) == 0:
            return "There is no such school whose name is" + self.schoolName
        school_id = result[0][0]
        try:
            cursor.execute("select * from cmf_tp_member where school_id = %d and status != 0" % school_id)
            returned = cursor.fetchall()
            returned_list = []
            for item in returned:
                returned_list.append({'id':item[0],'p_id':item[1],'wechat_nickname':item[9],'user_name':item[2],'school_id':item[3],'upload_limit':item[7],'viewing_problem':item[4],'type':typedict[item[6]]})
            return returned_list
        except Exception as e:
            print('-18' + str(e))
            raise e




class GetToBeVerifiedTeacherInfoByWechatName(CustomOperation):
    def __init__(self, WechatName:str):
        self.MySQLCommand = "select * from cmf_tp_member where `nickname` = \'{}\' and status = 0".format(WechatName)
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'wechat_nickname':item[3]})
            return returned_lst
        except Exception as e:
            print('-19'+str(e))
            raise e

class GetToBeVerifiedTeacherInfoByFlexibleWechatName(CustomOperation):
    def __init__(self, WechatName:str):
        self.MySQLCommand = "select * from cmf_tp_member where `nickname` like \'%{}%\' and status = 0".format(WechatName)
    def execute(self, cursor: pymysql.cursors.Cursor):
        try:
            cursor.execute(self.MySQLCommand)
            returned = cursor.fetchall()
            returned_lst = []
            for item in returned:
                returned_lst.append({'id':item[0],'wechat_nickname':item[3]})
            return returned_lst
        except Exception as e:
            print('-20'+str(e))
            raise e

# class GetTeacherNotViewdProblemNumber(CustomOperation):
#     def __init__(self,TeacherId:int):
#         self.TeacherId = TeacherId
#         self.MySQLCommand = None
#     def execute(self,cursor:pymysql.cursors.Cursor):
#         try:
#             cursor.execute("select * from cmf_tp_member where id = %i and status != 0" % self.TeacherId)
#             result = cursor.fetchall()
#             if len(result) == 0:
#                 raise Exception("No such Teacher!")
#             if len(result) > 1:
#                 raise Exception("More than one Teacher!")
#             cursor.execute("select * from cmf_tp_not_viewed_number where id = %i" % self.TeacherId)
#             result = cursor.fetchall()
#             number = result[0][1]
#             return True, number
#         except Exception as e:
#             print("Error!",'-21'+str(e))
#             return False, 0

class GetTeacherNotViewdProblemNumber(CustomOperation):
    def __init__(self,TeacherId:int):
        self.TeacherId = TeacherId
        self.MySQLCommand = None
    def execute(self,cursor:pymysql.cursors.Cursor):
        try:
            cursor.execute("select * from cmf_tp_member where id = %i and status != 0" % self.TeacherId)
            result = cursor.fetchall()
            if len(result) == 0:
                raise Exception("No such Teacher!")
            if len(result) > 1:
                raise Exception("More than one Teacher!")
            cursor.execute("select * from cmf_tp_exam where status = 2")
            exam_id = cursor.fetchall()
            if len(exam_id) >= 1:
                if len(exam_id)>1:
                    raise Exception("What is happening? Two tests are happening!")
                exam_id = exam_id[0][0]
                cursor.execute("select count(*) from cmf_tp_correct as a join cmf_tp_subject as b on a.p_id = b.id join cmf_tp_test_paper as c on b.p_id = c.id where c.p_id = {} and a.user_id = {} and a.status = 1".format(exam_id, self.TeacherId))
                returned = cursor.fetchall()
                return True, returned[0][0] # This is an int number, and an int number. The first int is number of problems not viewed, the second is the teacher type.
            else:
                return True, 0
        except Exception as e:
            print(e)
            raise e