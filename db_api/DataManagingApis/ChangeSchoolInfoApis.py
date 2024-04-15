from db_api import *
class AddNewSchoolByName(CustomOperation):
    def __init__(self,userId:int,Name:str,AreaName:str):
        self.userId = userId
        self.Name = Name
        self.AreaName = AreaName
    def execute(self, cursor: pymysql.cursors.Cursor):
        cursor.execute("select * from cmf_tp_admin where user_id = {}".format(self.userId))
        result = cursor.fetchall()
        assert len(result) == 1, "The user is not an admin!"
        cursor.execute("select * from cmf_tp_area where area_name = \'{}\'".format(self.AreaName))
        result = cursor.fetchall()
        assert len(result) == 1, "The area does not exist!"
        areaID = result[0][0]
        try:
            cursor.execute("select * from cmf_tp_area where id = {}".format(areaID))
            result = cursor.fetchall()
            if len(result) == 0:
                raise Exception("No such Id!")
            if len(result) > 1:
                raise Exception("More than one Id!")
            cursor.execute("select * from cmf_tp_school where `school_name` = '{}' and `area` = {}".format(self.Name,areaID))
            result = cursor.fetchall()
            if len(result) > 0:
                print("School Named {} in Area {} already exists!".format(self.Name,self.AreaName))
                print("Now just return the id of the school.")
                return result[0][0]
            
            # obtain max school id.
            cursor.execute("select max(id) from cmf_tp_school")
            id_list = cursor.fetchall()
            max_id = id_list[0][0]
            current_id = max_id + 1
            cursor.execute("insert into cmf_tp_school (`id`,`school_name`,`area`) values ({},'{}',{})".format(current_id,self.Name,areaID))
            cursor.execute("select * from cmf_tp_school where `school_name` = '{}' and `area` = {}".format(self.Name,areaID))
            result = cursor.fetchall()
            return f"Successfully added a new school with school_id{result[0][0]}"
        except Exception as e:
            print('-4'+str(e))
            raise e