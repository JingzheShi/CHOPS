from db_api import customTransaction
from db_api.DataQueryApis.GetTeacherInfoApis import *
from db_api.DataManagingApis.ChangeTeacherInfoApis import *
from db_api.DataQueryApis.GetSchoolInfoApis import *
from db_api.DataManagingApis.ChangeSchoolInfoApis import *
def instruction_name_and_args_to_instruction(instruction_name, args):
    print("Current args is", args)
    try:
        if 'ChangeAllTypesMarkingSubject' in instruction_name:
            return True, ChangeAllTypesMarkingSubject(args[0], args[1])
        elif 'VerifyTeacherUserToBeSupTeacher' in instruction_name:
            return True, VerifyTeacherUserToBeSupTeacher(args[0], args[1], args[2])
        elif 'MakeAllTypesToBeArbiter' in instruction_name:
            return True, MakeAllTypesToBeArbiter(args[0])
        elif 'MakeAllTypesToBeSupTeacher' in instruction_name:
            return True, MakeAllTypesToBeSupTeacher(args[0])
        elif 'MakeAllTypesToBeSubCoach' in instruction_name:
            return True, MakeAllTypesToBeSubCoach(args[0],args[1])
        elif 'ChangeAllTypesUploadLimit' in instruction_name:
            return True, ChangeAllTypesUploadLimit(args[0], args[1])
        elif 'ChangeAllTypesSchool' in instruction_name:
            return True, ChangeAllTypesSchool(args[0],args[1])
        elif 'AddNewSchoolByName' in instruction_name:
            return True, AddNewSchoolByName(args[0],args[1],args[2])
        elif 'GetTeacherInfoByName' in instruction_name:
            return True, GetTeacherInfoByNameByUser(args[0],args[1])
        elif 'GetTeacherInfoBySchoolName' in instruction_name:
            return True, GetTeacherInfoBySchoolNameByUser(args[0],args[1])
        else:
            return False, 'No such instruction'
    except Exception as e:
        # print('jdiufjsu5'+str(e))
        return False, '5'+str(e)


def mysql_execute(instruction_name, myargs, user_wechat_nickname, commit=False):
    # print("instruction_name,",instruction_name)
    print("my_args,",myargs)    
    # print("user_wechat_nickname,",user_wechat_nickname)
    user_id_returned_list = customTransaction.executeOperation(GetTeacherInfoByWechatName(user_wechat_nickname))
    # print(user_id_returned_list)
    if len(user_id_returned_list) == 0:
        return False, 'The user is not in the system.'
    elif len(user_id_returned_list) > 1:
        return False, 'There are more than one user with the same nickname.'
    assert len(user_id_returned_list) == 1
    user_id = user_id_returned_list[0]['id']
    if myargs is None:
        return False, 'The args is not complete.'
    success,instruction_or_reason = instruction_name_and_args_to_instruction(instruction_name, [user_id]+myargs)
    # print("instruction_or_reason",instruction_or_reason)
    if not success:
        return False, instruction_or_reason
    try:
        if not commit:
            result = customTransaction.executeOperationwitherror(instruction_or_reason)
        else:
            result = customTransaction.executeOperation(instruction_or_reason)
            customTransaction.commit_and_reconnect()
        print("current result is",result)
        return True, result
    except Exception as e:
        return False, '5' + str(e)
    
    
def convert_args_format(args_str, arg_description):
    print("bjnkslafiewjddsawejoi",args_str,arg_description)
    args_str_list = args_str.split(',')
    arg_description_list = arg_description.replace(' ','').replace(' ','').replace(')','').split(',')
    if len(args_str_list) > len(arg_description_list):
        return False, None, "Fail because Too many arguments provided"
    elif len(args_str_list) < len(arg_description_list):
        return False, None, "Fail because Not enough arguments provided"
    returned_list = []
    for (idx,arg) in enumerate(args_str_list):
        print("current arg_description_list==",arg_description_list)
        try:
            assert arg != '?', "Fail because Not enough arguments provided"
            to_type_str = arg_description_list[idx].split('(')[-1]
            if to_type_str == 'int':
                try:
                    int(arg)
                except Exception as e:
                    assert "?" not in arg, "Fail because Not enough arguments provided"
                arg = int(arg)
            elif to_type_str == 'str':
                arg = arg
            returned_list.append(arg)
        except Exception as e:
            return False, None, e
    print("Current returned_list is", returned_list)
    return True, returned_list, None

def get_operation_from_str(answer,executable_list):
    print("bjsgafuewijnwe")
    try:
        # print(answer)
        operation = answer.split('|||')[0]
        operation = operation.replace('\"','').replace('\'','').replace(' ','').replace('\n','').replace('\t','').replace('  ','').replace('\n','').split('==')[-1]
        print("operation",operation)
        args = answer.split('|||')[1].split('==')[-1]
    except Exception as e:
        print('ffjjdfwejd'+str(e))
        return dict(
            operation_name = None,
            args = None,
            description = 'Fail because Not Executable Operation'
        )
    print("Current executable list is:", executable_list)
    for (operation_name, operation_description, arg_description) in executable_list:
        if operation == operation_name:
            if args == '?':
                return dict(
                    operation_name = operation_name,
                    args = None,
                    description = operation_description + 'but the user did not provide corresponding arguments.'
                )
            else:
                success_flag, args_list, why = convert_args_format(args, arg_description)
                if success_flag:
                    return dict(
                        operation_name = operation_name,
                        args = args_list,
                        description = operation_description + 'with the given arguments: ' + ', '.join([str(item) for item in args_list])
                    )
                else:
                    return dict(
                        operation_name = operation_name,
                        args = None,
                        description = why,
                    )
    return dict(
            operation_name = None,
            args = None,
            description = 'Fail because Not Executable Operation'
        )