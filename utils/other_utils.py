from db_api import customTransaction
from db_api.DataQueryApis.GetTeacherInfoApis import *
from db_api.DataManagingApis.ChangeTeacherInfoApis import *
from db_api.DataQueryApis.GetSchoolInfoApis import *


def add_previous_prompts(answer_InvalidReason_list):
    added_str = "\nAttention! Some of the reference answers to this question are considered inappropriate for the following reasons and have been filtered out: "
    try:
        for (answer, reason) in answer_InvalidReason_list:
            added_str += '\n' + 'Invalid Answer:' + answer + 'Invalid Reason:' + reason
        added_str += '\n'
    except Exception as e:
        added_str = 'Error in adding previous prompts: ' + str(e)
    return added_str

def GetUserState(user_nickname):
    user_id_returned_list = customTransaction.executeOperation(GetTeacherInfoByWechatName(user_nickname))
    user_id_to_be_verified_list = customTransaction.executeOperation(GetToBeVerifiedTeacherInfoByWechatName(user_nickname))
    # print(user_id_returned_list)
    # print(user_id_to_be_verified_list)
    extra_info = str(None)
    if len(user_id_returned_list) == 0 and len(user_id_to_be_verified_list) == 0:
        state = "Not in the system: not approved and not in the process of being approved."
    elif len(user_id_returned_list) == 0 and len(user_id_to_be_verified_list) >= 1:
        state = "In the process of being approved."
    elif len(user_id_returned_list) == 1:
        state = "Has been approved and is in the system."
        extra_info += "Type of user is: {0}, The user is {0}".format(user_id_returned_list[0]['type'])
        check_success, not_viewed_problem_num = customTransaction.executeOperation(GetTeacherNotViewdProblemNumber(user_id_returned_list[0]['id']))
        
        if check_success:
            extra_info += "Not viewed problem number: " + str(not_viewed_problem_num) + '. Problems to be marked is ' + str(not_viewed_problem_num) + "That is the number of problem or answer sheets that the user need to mark."
        else:
            extra_info += "Not able to get the not viewed problem number."
        
    # print(state)
    return state, extra_info

def sql_prompt(user_nickname):
    state, extra_info = GetUserState(user_nickname)
    
    # if state == '不在系统中':
    #         sql_prompt = '该用户“不在系统中”，尚未提交审核，所以没有通过。无法提交试卷、阅卷、也无法完成领队或者副领队相关操作。该用户未按要求在报名时登陆，因此尚未提交审核。'
    #     elif state == '待审核':
    #         sql_prompt = '该用户的状态是“待审核”，需要等待审核，这也是该用户审核没有通过的原因。审核完成之后，才能提交试卷或阅卷、才能完成领队或者副领队相关操作。'
    #     elif state == '审核通过且在系统中':
    #         sql_prompt = '该用户在系统中、已经审核通过了。'
    sql_prompt = ''
    if state == 'Not in the system: not approved and not in the process of being approved.':
        sql_prompt += 'This user is \'not in the system\', has not uploaded the request for approval, so the user has not been approved. The user cannot submit the paper, mark the paper, or complete the operation related to the leader or vice leader. The user did not log in as required when registering, so the user has not been approved. ATTENTION !THE USER MUST BE APPROVED BEFORE ANY OPERATION! If the user is asking about how to do some operation or questiosn related to it, for example, how to edit things, YOU SHOULD TELL THE USER THAT HE OR SHE NEED TO BE APPROVED FIRST!'
    elif state == 'In the process of being approved.':
        sql_prompt += 'The user\'s status is \'in the process of being approved\', and the user needs to wait for approval, which is also the reason why the user has not been approved. After the approval is completed, the user can submit the paper or mark the paper, and complete the operation related to the leader or vice leader. ATTENTION !THE USER MUST BE APPROVED BEFORE ANY OPERATION! If the user is asking about how to do some operation or questiosn related to it, for example, how to edit things, YOU SHOULD TELL THE USER THAT HE OR SHE NEED TO BE APPROVED FIRST!'
    elif state == 'Has been approved and is in the system.':
        sql_prompt += 'The user is in the system and has been approved.'
    sql_prompt = "In the database, the user's status is: " + sql_prompt + extra_info
    return sql_prompt
    