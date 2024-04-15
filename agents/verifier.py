from agents.base import BaseAgent
from utils.pdf_utils import SemanticSearch, load_recommender
from utils.other_utils import sql_prompt as sql_prompt_
from utils.mysql_execute_utils import mysql_execute, get_operation_from_str

def get_VALID_or_INVALID(answer_str):
    try:
        if "INVALID" in answer_str.split('|||')[0]:
            return False
        else:
            return True
    except Exception as e:
        print('at get_VALID_or_INVALID:',e)
        return False
    

class Verifier(BaseAgent):
    def __init__(self,agent_config):
        super().__init__(agent_config)
        print("Verifier is ready!")
        self.commit_changes_if_valid = agent_config['commit_changes_if_valid']
        self.executable_instruction_list = []
        with open(agent_config['executable_instructions_path'],'r') as f:
            executable_instructions = f.readlines()
        for line in executable_instructions:
            line = line.replace('\n','')
            print(line.split(':'))
            # print(line.split(','))
            self.executable_instruction_list.append((line.split(':')[0],line.split(':')[1][:-6],line.split(':')[2]))
        self.no_verify = agent_config['no_verify']
    def verify_and_reply(self,user_nickname, question, classifier_result, executor_result,added_prompt,current_iter,total_iter,invalid_reasons):
        print("Current executor result is:",executor_result)
        if 'A' in classifier_result[1] or 'N' in classifier_result[1] or 'C' in classifier_result[1] or classifier_result[0] == False:
            valid, reason =  self.verify_question(user_nickname,question,classifier_result,executor_result,current_iter,total_iter)
            if valid:
                return True, None, self.summarize_QA(user_nickname,question,classifier_result,executor_result,added_prompt)
            else:
                if current_iter == total_iter:
                    return True, None, self.summarize_last_QA(user_nickname,question,classifier_result,executor_result,invalid_reasons)
                return False, reason, None
        elif 'B' in classifier_result[1]:
            print("fbjskliewfjriuefejreirufjs")
            valid, reason_or_answer = self.verify_operation(user_nickname,question,classifier_result,executor_result,current_iter,total_iter)
            if valid:
                return True, None, reason_or_answer
            else:
                return False, reason_or_answer, None
        else:
            print("fjsnklgfiewjdnswije")
        
    def verify_question(self,user_nickname,question,classifier_result,executor_result,current_iter,total_iter):
        if self.no_verify:
            print("Currently Not verifying.")
            return True, ''
        my_prompt = f"There is a QA pair: Q: {question}, A:{executor_result}."\
            "Instruction: The Classifier think this is a question rather than an operation, or a query to the database. Please verify whether this is indeed a question rather than an operation. Also verify the QA pair is responded based on the knowledge known by the executor. Return VALID,valid_score(1-10) or INVALID,valid_score(1-10) and tell the reason. ATTENTION! The answerer do not know every information, so it may give some possibility or only relavant information, or it is very honest to say that it does not know related information and recommend to contact human customer service: this is VALID. But if the answerer gives irrelavant answer, then it is INVALID. Attention! The answer could be either very simple or very complicated, the length of the answer is not what you should consider for valid or invalid. You need to follow these formats:"\
                "Example0:"\
                "Q: Please modify my age in the system. A: I cannot answer the question. Please contact human customer service. Judgement: INVALID, 3|||Is invalid, since this is not a question! This is an instruction."\
                "Example1:"\
                "Q:why I cannot use the system? A: you need to be approved into the system first. Judgement: VALID,8|||Is valid answer, since the question is why it cannot use the system, and the answer is that the user needs to be approved."\
                "Example2:"\
                "Q:how to add student info? A: you must be approved before you could do anything in the system. Judgement: VALID,7|||Is valid answer, since the question is how to add student info, and the answer is that the user needs to be approved until it can add student."\
                "Example3:"\
                "Q: Why I am not approved yet? A: Weather is good today. Judgement: INVALID,1|||Is invalid answer, since the question is why it is not approved yet, but the answer is about weather today, which is irrelavant."\
                "Example4:"\
                "Q: How is the weather today? A: Please contact human customer service for more information.VALID,9|||Is valid answer, since the answerer is honest and says that it does not know the answer and recommends to contact human customer service."\
                "Do NOT add any other information. Make sure the answer is exactly with the previous instructions. Only output VALID,score|||reason or INVALID,score|||reason. Do NOT output any error or extra information."\
                "Judgement: "
        answer = self.ask_llm(my_prompt)
        print("Verifier:",answer)
        try:
            if ("invalid" not in answer.split("|||")[1]) and ("INVALID" not in answer.split("|||")[0]):
                return True, answer.split('|||')[-1]
            else:
                try:
                    score = int(answer.split("|||")[0].split(',')[-1])
                    score += float(current_iter)/float(total_iter)*3
                    if score > 6:
                        return True, 'Added.'
                    else:
                        return False, answer.split('|||')[-1]
                except Exception as e:
                    return False, answer.split('|||')[-1]
        except Exception as e:
            print("at verify_question:",e)
            return False, e
    def summarize_QA(self,user_nickname,question,classifier_result,executor_result,added_prompt):
        my_prompt = f"There is a QA pair: Q: {question}, A:{executor_result}."\
            "Instruction: The final answer is valid. Please summarize the final Answer. Return the summary."
        my_prompt += added_prompt
        my_prompt += 'Summarization: '
        answer = self.ask_llm(my_prompt)
        print('final answer is:',answer)
        return answer
    
    def summarize_last_QA(self,user_nickname,question,classifier_result,executor_result,invalid_reasons):
        my_prompt = f"There is a QA pair: Q: {question}, A:{executor_result}."\
            "Instruction: The final answer is on of these. Please choose one and return it.\n"
        for (answer, reason) in invalid_reasons:
            print("answer==",answer)
            print("reason==",reason)
            try:
                answer_str = str(answer)
            except Exception:
                continue
            my_prompt += 'One Possibel Choice: ' + answer + '\n\n'
        my_prompt += 'The correct one should be: '
        answer = self.ask_llm(my_prompt)
        print('final answer is:',answer)
        return answer
        
    
        
    def verify_operation(self,user_nickname,instruction,classifier_result,executor_result,current_iter,total_iter):
        sql_prompt = sql_prompt_(user_nickname)
        operation_dict = get_operation_from_str(executor_result,self.executable_instruction_list)
        # print("operation_dict==",operation_dict)
        # print("operation_dict['operation_name']==",operation_dict['operation_name'])
        # print("operation_dict['args']==",operation_dict['args'])
        # if operation_dict['description'] == 'Not Executable Operation':
        #     return False, 'Not Executable Operation in the executable operations.'
        operation_name = operation_dict['operation_name']
        myargs = operation_dict['args']
        print("bjkloiefwjdnfawe",myargs)
        success_flag,reason = mysql_execute(instruction_name=operation_name,myargs=myargs,user_wechat_nickname=user_nickname,commit=False)
        if self.no_verify:
            success_flag, result_or_reason = mysql_execute(operation_name,myargs,user_nickname, True and self.commit_changes_if_valid)
            if not success_flag:
                # print("!!sfiulhaedbfhsddj")
                my_prompt = "There is an UserCommand-Operation pair. Command: {}, Operation: {}. Executed failed because {}"\
                    "Instruction: Please tell the user why the operation failed. Return the reason. Reply: In short, ".format(instruction,executor_result,result_or_reason)
                final_result = self.ask_llm(my_prompt)
                print("final result given by verifier:",final_result)
                return True, final_result
            else:
                my_prompt = "There is an UserCommand-Operation pair. Command: {}, Operation: {}. Executed successfully with result {}."\
                    "Instruction: Please tell the user the result, in short. Reply: In short, ".format(instruction,executor_result, result_or_reason)
                final_result = self.ask_llm(my_prompt)
                print("final result given by verifier:",final_result)
                return True, final_result
        
        
        
        success_str = 'succeess' if success_flag else "fail"
        description = operation_dict['description']
        print(description)
        my_prompt = f"There is an UserText. The Classifier think this is an operation, instruction or a query to the database rather than a question, and the executor gives the following instruction. Command: {instruction}, UserStatus: {sql_prompt}, Operation: {executor_result}, Description: {description}."\
            "Instruction: Please verify whether the Operation is VALID or INVALID given the UserText. Return VALID,valid_score(1-10) or INVALID,valid_score(1-10). Note that, some UserText may be out of the system's control, so it is VALID even if the answer does not address the user's request as long as it gives an appropriate reason. Some UserText is a question rather than an instruction, which should not be viewed as valid. Some UserText may not give enough information, where the Args should not be hallucinated."\
                "Examples:"\
                "Example1: UserText: Change my marking subject into 7, Operation: ChangeAllTypesMarkingSubject|||Args==7|||Reason==the user asked for a change of its marking subject. Judge: VALID,9|||The marking subject is changed into 7."\
                "Example2: UserText: Change my marking subject, Operation: ChangeAllTypesMarkingSubject|||Args==?. Judge: VALID,10|||The user did not give valid command."\
                "Example3: UserText: Change my student number, Operation: ChangeAllTypesMarkingSubject|||Args==7|||Reason==change marking subject. Judge: INVALID,2|||The command is irrelavent."\
                "Example4: UserText: Change my student number, Operation:?|||?|||Reason==user is not in the system yet. Judge: VALID,8|||The command is out of the system's control."\
                "Example5: UserText: Change my marking subject, Operation: ChangeAllTypesMarkingSubject|||Args==7. Judge: INVALID,1|||The user did not specify a marking subject, but the command specifies it without the user's information."\
                "Example6: UserText: How to change my student number, Operation:?|||?|||Reason==there are no executable commands that satisfy the users' request. Judge: INVALID,2|||The user text is not a command, the classifier made a mistake!"\
                "Example7: UserText: Complete my application with Name Name240393,Reason==user wants to complete the approval of their application as a team leader.Please provide the view problem index (int) for the operation to be completed., this operation would invalid literal for int(). with base 10: 'ViewProblem(int)'. Judge:VALID,7,|||The executor points out that the user need to provide more information." \
                f"UserText:{instruction}, Operation=={executor_result}, this operation would {description}.Judge: "

        llm_answer = self.ask_llm(my_prompt)
        print("Current verifier prompt:",my_prompt)
        print("Verifier:",llm_answer)
        is_VALID = get_VALID_or_INVALID(llm_answer)
        try:
            reason = llm_answer.split('|||')[-1]
        except Exception as e:
            reason = llm_answer
        
        if not is_VALID:
            try:
                score = int(llm_answer.split("|||")[0].split(',')[-1])
                score += float(current_iter)/float(total_iter)*3
                print("Current score is :", score)
                if score < 6:
                    return False, reason
                else:
                    pass
            except Exception as e:
                try:
                    return False, llm_answer.split('|||')[-1]
                except:
                    return False, llm_answer
        
        success_flag, result_or_reason = mysql_execute(operation_name,myargs,user_nickname, True and self.commit_changes_if_valid)
        if not success_flag:
            # print("!!sfiulhaedbfhsddj")
            my_prompt = "There is an UserCommand-Operation pair. Command: {}, Operation: {}. Executed failed because {}"\
                "Instruction: Please tell the user why the operation failed. Return the reason. Reply: In short, ".format(instruction,executor_result,result_or_reason)
            final_result = self.ask_llm(my_prompt)
            print("final result given by verifier:",final_result)
            return True, final_result
        else:
            my_prompt = "There is an UserCommand-Operation pair. Command: {}, Operation: {}. Executed successfully with result {}."\
                "Instruction: Please tell the user the result, in short. Reply: In short, ".format(instruction,executor_result, result_or_reason)
            final_result = self.ask_llm(my_prompt)
            print("final result given by verifier:",final_result)
            return True, final_result
        
            