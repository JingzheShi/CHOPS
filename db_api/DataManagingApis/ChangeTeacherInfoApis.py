from db_api import *
reverse_typedict={"arbiter":2,"vice_teamleader":3,"teamleader":1}
class MakeAllTypesToBeArbiter(CustomOperation):
    def __init__(self,ChangedUserId:int):
        super().__init__()
        self.ArbiterId=ChangedUserId
    def execute(self, cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where id = %i and status != 0" % self.ArbiterId)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("User is not in the system!")
        if len(result) > 1:
            raise Exception("More than one User!")
        if result[0][6] == 1:
            #Then it is currently a leader。
            #Firstly check: if there are answer sheets to be marked as leader
            cursor.execute("select * from cmf_tp_exam where status = 2")
            exam_id = cursor.fetchall()
            if len(exam_id) >= 1:
                if len(exam_id)>1:
                    raise Exception("What is happening? Two Tests are happening!")
                # exists answer sheets to be marked
                exam_id = exam_id[0][0]
                cursor.execute("select count(*) from cmf_tp_correct as a join cmf_tp_subject as b on a.p_id = b.id join cmf_tp_test_paper as c on b.p_id = c.id where c.p_id = {} and a.user_id = {} and a.status = 1".format(exam_id, self.ArbiterId))
                returned = cursor.fetchall()
                # print(returned)
                # print("alkdfhas;lkdfs")
                # if the counting result > 0, then raise exception.
                if returned[0][0] > 0:
                    raise Exception("The user has not finished correcting the test papers !")
        cursor.execute("update cmf_tp_member set type = 2 where id = %i;" % self.ArbiterId)
        cursor.execute("update cmf_tp_member set p_id = 0 where id = %i;"% self.ArbiterId)
        cursor.fetchall()
        







import openpyxl
class MakeAllTypesToBeSubCoach(CustomOperation):
    def __init__(self,ChangedUserId:int, ItsNewSupName:str):
        '''
            This api takes into ChangedUserId and ItsNewSupId.
            After being executed, it will make the subcoachid to be the subcoach of the supteacherid.
            Notice that this will raise an exception when the one becoming the subcoach is a arbiter.
        '''
        super().__init__()
        self.NewSupName = ItsNewSupName
        # self.SupTeacherId = ItsNewSupId
        self.SubCoachId = ChangedUserId
    def execute(self, cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where user_name = \'{}\' and status != 0".format(self.NewSupName))
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such team leader!")
        if len(result) > 1:
            raise Exception("More than one team leader!")
        if result[0][6] != 1:
            raise Exception("This is not a team leader!")
        supTeacherId = result[0][0]
        
        cursor.execute("select * from cmf_tp_member where id = %i and status != 0" % self.SubCoachId)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such user!")
        if len(result) > 1:
            raise Exception("More than one user!")
        
        if result[0][6] == 1:
            #Then it is currently a leader。
            
            
            cursor.execute("select * from cmf_tp_exam where status = 2")
            exam_id = cursor.fetchall()
            if len(exam_id) >= 1:
                if len(exam_id)>1:
                    raise Exception("What is happening? Two Tests are happening!")
                exam_id = exam_id[0][0]
                cursor.execute("select count(*) from cmf_tp_correct as a join cmf_tp_subject as b on a.p_id = b.id join cmf_tp_test_paper as c on b.p_id = c.id where c.p_id = {} and a.user_id = {} and a.status = 1".format(exam_id, self.SubCoachId))
                returned = cursor.fetchall()
                # print(returned)
                # print("alkdfhas;lkdfs")
                # if the counting result > 0, then raise exception.
                if returned[0][0] > 0:
                    raise Exception("The user has not finished correcting the test papers !")
        
        
        
        cursor.execute("update cmf_tp_member set type = 3 where id = %i;" % self.SubCoachId)
        cursor.fetchall()
        assert supTeacherId != self.SubCoachId, "The user cannot be its own team leader!"
        cursor.execute("update cmf_tp_member set p_id = %i where id = %i;" % (supTeacherId, self.SubCoachId))
        cursor.fetchall()
        
                
class MakeAllTypesToBeSupTeacher(CustomOperation):
    def __init__(self,Id:int):
        super().__init__()
        self.Id = Id
    def execute(self, cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where id = %i and status != 0" % self.Id)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such Id!")
        if len(result) > 1:
            raise Exception("More than one Id!")
        cursor.execute("update cmf_tp_member set type = 1 where id = %i;" % self.Id)
        cursor.execute("update cmf_tp_member set p_id = 0 where id = %i;" % self.Id)
        cursor.fetchall()
        

class MakeArbiterToBeSupTeacher(CustomOperation):
    def __init__(self,Id:int):
        super().__init__()
        self.Id = Id
    def execute(self,cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where id = %i and status != 0" % self.Id)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such Id!")
        if len(result) > 1:
            raise Exception("More than one Id!")
        if result[0][6] != 2:
            raise Exception("This is not a arbiter!")
        cursor.execute("update cmf_tp_member set type = 1 where id = %i;" % self.Id)
        
        cursor.execute("update cmf_tp_member set p_id = 0 where id = %i;" % self.Id)
        cursor.fetchall()

class ChangeAllTypesMarkingSubject(CustomOperation):
    def __init__(self,ChangedUserId:int, ItsNewMarkingSubject:int):
        self.Id=ChangedUserId
        self.NewMarkingSubject=ItsNewMarkingSubject
        assert self.NewMarkingSubject in [1,2,3,4,5,6,7,8,9,10], "Marking subject must be in [1,2,3,4,5,6,7,8,9,10]"

    def execute(self,cursor: pymysql.cursors.Cursor):
        # assert False,' system down!'
        cursor.execute("select * from cmf_tp_member where (id = %i and status != 0)" % self.Id)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such Id!")
        if len(result) > 1:
            raise Exception("More than one Id!")
        if result[0][6] == 1:
            pass
            cursor.execute("select * from cmf_tp_exam where status = 2")
            exam_id = cursor.fetchall()
            if len(exam_id) >= 1:
                # print("Current exam_id is > 1.adufifidjsndjhfio")
                if len(exam_id)>1:
                    raise Exception("What is happening? Two Tests are happening!")
                #存在未批改的考试
                exam_id = exam_id[0][0]
                cursor.execute("select count(*) from cmf_tp_correct as a join cmf_tp_subject as b on a.p_id = b.id join cmf_tp_test_paper as c on b.p_id = c.id where c.p_id = {} and a.user_id = {} and a.status = 1".format(exam_id, self.Id))
                returned = cursor.fetchall()
                # print(returned)
                # print("alkdfhas;lkdfs")
                # if the counting result > 0, then raise exception.
                # print("Current not viewed problem number is:",returned[0][0],'dsfjlafoei;jawneshjiud')
                if returned[0][0] > 0:
                    raise Exception("The user has not finished correcting the test papers !")
        
        cursor.execute("update cmf_tp_member set subject = %i where id = %i;" % (self.NewMarkingSubject, self.Id))
        cursor.fetchall()
        
class ChangeAllTypesSchool(CustomOperation):
    def __init__(self,ChangedUserId:int, NewSchoolName:str):
        self.Id=ChangedUserId
        self.NewSchoolName = NewSchoolName
    def execute(self,cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where (id = %i and status != 0)" % self.Id)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such TeacherId!")
        if len(result) > 1:
            raise Exception("More than one TeacherId!")
        cursor.execute("select * from cmf_tp_school where school_name = \'{}\'".format(self.NewSchoolName))
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such School!")
        if len(result) > 1:
            raise Exception("More than one School of the name!")
        newSchoolId = result[0][0]
        cursor.execute("update cmf_tp_member set school_id = %i where id = %i;" % (newSchoolId, self.Id))
        cursor.fetchall()

class ChangeAllTypesUploadLimit(CustomOperation):
    def __init__(self,ChangedUserId:int, NewUploadLimit:int):
        self.Id=ChangedUserId
        self.NewUploadLimit = NewUploadLimit
        assert (NewUploadLimit >=0 and NewUploadLimit<=200), 'UploadLimit must be non-negative and <= 200!'
    def execute(self, cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where (id = %i and status != 0)" % self.Id)
        result = cursor.fetchall()
        if len(result) == 0:
            raise Exception("No such TeacherId!")
        if len(result) > 1:
            raise Exception("More than one TeacherId!")
        cursor.execute("update cmf_tp_member set `limit` = %i where id = %i;" % (self.NewUploadLimit, self.Id))
        cursor.fetchall()
        
class VerifyTeacherUserToBeSupTeacher(CustomOperation):
    def __init__(self,ToBeVerifiedId:int,Name:str,ViewProblem:int=1,SchoolId:int=3, UploadLimit:int=1):
        self.Id = ToBeVerifiedId
        self.Name = Name
        self.SchoolId = SchoolId
        self.ViewProblem = ViewProblem
        assert self.ViewProblem in [1,2,3,4,5,6,7,8,9,10], 'marking subject must be in [1,2,3,4,5,6,7,8,9,10]'
        self.UploadLimit = UploadLimit
    def execute(self,cursor:pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_member where (id = %i)" % self.Id)
        result = cursor.fetchall()
        if len(result) == 0 :
            raise Exception("In users who are approved into the system and in users who are waiting to be approved into the system, no such id exists.")
        if len(result) > 1:
            raise Exception("In users who are approved into the system and in users who are waiting to be approved into the system, multiple such id exist.")
        if result[0][-4] == 1:
            print("Attention! The user whose userid={}, user_name={}, has already been approved! No changes made!!".format(self.Id,self.Name))
        else:
            cursor.execute("update cmf_tp_member set `user_name` = \'{}\', `school_id` = {}, `subject`={}, `limit`={}, `status`=1 where id = {}".format(self.Name,self.SchoolId,self.ViewProblem,self.UploadLimit,self.Id))
            cursor.fetchall()
            print("The user whose userid={}, name={}, has been approved!".format(self.Id,self.Name))
    



