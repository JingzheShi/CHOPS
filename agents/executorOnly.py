from agents.base import BaseAgent
from utils.pdf_utils import SemanticSearch, load_recommender
from utils.other_utils import sql_prompt as sql_prompt_
from utils.mysql_execute_utils import mysql_execute, get_operation_from_str

class ExecutorOnly(BaseAgent):
    def __init__(self,agent_config):
        super().__init__(agent_config)
        self.guidefile_recommender = SemanticSearch()
        self.executable_instructions = ''
        with open(agent_config['executable_instructions_path'],'r') as f:
            self.executable_instructions = f.read()
        load_recommender(self.guidefile_recommender, agent_config['guidefile_path'],word_length = agent_config['word_length'],topk = agent_config['topk_chunks'])
        self.executable_instruction_list = []
        with open(agent_config['executable_instructions_path'],'r') as f:
            executable_instructions = f.readlines()
        for line in executable_instructions:
            line = line.replace('\n','')
            print(line.split(':'))
            # print(line.split(','))
            self.executable_instruction_list.append((line.split(':')[0],line.split(':')[1][:-6],line.split(':')[2]))
        print("Executor is ready!")
    def execute(self, user_nickname,question):
        topn_chunks_from_pdf = self.guidefile_recommender(question)
        topn_chunks_prompt = ''
        sql_prompt = sql_prompt_(user_nickname)
        print('sql_prompt:',sql_prompt)
        topn_chunks_prompt += 'query_result[0]:'+sql_prompt+'\n\n'
        for idx,chunk in enumerate(topn_chunks_from_pdf):
            topn_chunks_prompt += 'query_result[' + str(idx+1) + ']:'+ chunk + '\n\n'
        query_info = "Begin of query information:" + topn_chunks_prompt + "End of query information."
        
        my_prompt = f"Instruct: Given the user's Question or Operation, Please answer the question FROM THE QUERY or give an executable operation FROM THE OPERATION that can help answer the user question or can execute the user instruction. If no op is found, simply reply 'I cannot answer the question. Please contact human customer service.'\n"\
            "return in the format following TYPE==Answer|||Answer==... or TYPE==Instruction|||Operation==...|||Args==...|||Reason==...\n"\
            "Begin of query information:" + topn_chunks_prompt + "End of query information. Answer the user's question based on the query information.\n"\
            "Do NOT add any other information. Make sure the answer is exactly with the previous instructions. Do NOT output any error or extra information.\n"\
            "Do NOT say something like 'refer to section II of the query answer for answer', state the detailed answer directly.\n"\
            f"Operations:{self.executable_instructions}\n"\
            "\n For example:"\
                    "User's Text: AddNewSchoolByName. TYPE==Instruction|||Operation==AddNewSchoolByName|||Args==NewSchoolName,AreaName|||Reason==user wants to add a new school by name and provide school name and area name\n"\
                    "User's Text: please change my marking subject into 7. The operation should be: Operation==ChangeAllTypesMarkingSubject|||Args==7|||Reason==user wants to change marking subject and provide marking subject is 7\n"\
                    "User's Text: I want something to eat. The operation should be: Operation==?|||Args==?|||Reason==there are no executable commands that satisfy the users' request\n"\
                    "User's Text: please change my marking subject into 7. but the user is not in the systemm. The operation should be: Operaion==?|||Args==?|||Reason==user is not in the system, cannot execute command.\n"\
                    "User's Text: please chagne my marking subject into 7. The operation should be: Operation==ChangeAllTypesMarkingSubject|||Args==?|||Reason==user wants to change marking subject but did not provide its marking subject\n"\
                    "User's Text: please add a new school called TIUDJDH. The operation should be: Operation==AddNewSchoolByName|||Args==TIUDJDH,?|||Reason==user wants to add a new school but did not provide area name.\n"\
            "Do NOT add any other information. Make sure the answer is exactly with the previous instructions. Do NOT output any error or extra information. Do NOT hallucinate Args if the user does not provide it.\n"\
                "If there is no executable instructions, please answer 'Operation==?|||Args==?|||Reason==there are no executable commands that satisfy the users' request' Be honest. Not Knowing is much better than Cheating! If no args is needed, just set Args==None.DO NOT modify the name of the apis! DO NOT modify the name of the operations and instructions!\n"
        my_prompt += "User Text:"+question+".Answer: TYPE=="
        llm_answer = self.ask_llm(my_prompt)
        print("Current executor prompt",my_prompt)
        try:
            llm_answer_list = llm_answer.split('|||')
            text_type = llm_answer_list[0].replace('=','').replace('TYPE','')
            if text_type == 'Answer' or 'Answer' in text_type or 'answer' in text_type:
                answer = llm_answer_list[1].replace('answer==','').replace("Answer==",'')
                return answer
            elif text_type == 'Instruction' or 'instruction' in text_type:
                executor_result = '|||'.join(llm_answer_list[1:])
                operation_dict = get_operation_from_str(executor_result, self.executable_instruction_list)
                operation_name = operation_dict['operation_name']
                myargs = operation_dict['args']
                print("djkfdsajsdrwajr",myargs)
                success_flag, result_or_reason = mysql_execute(operation_name, myargs, user_nickname,)
                if not success_flag:
                    # print("!!sfiulhaedbfhsddj")
                    my_prompt = "There is an UserCommand-Operation pair. Command: {}, Operation: {}. Executed failed because {}"\
                        "Instruction: Please tell the user why the operation failed. Return the reason. Reply: In short, ".format(operation_name,executor_result,result_or_reason)
                    final_result = self.ask_llm(my_prompt)
                    print("final result given by verifier:",final_result)
                    return final_result
                else:
                    my_prompt = "There is an UserCommand-Operation pair. Command: {}, Operation: {}. Executed successfully with result {}."\
                        "Instruction: Please tell the user the result, in short. Reply: In short, ".format(operation_name,executor_result, result_or_reason)
                    final_result = self.ask_llm(my_prompt)
                    print("final result given by verifier:",final_result)
                    return final_result
            else:
                return 'Fail to answer or carry out operation. beause of '+str(e)
                
                
        except Exception as e:
            print(e)
            return 'Fail to answer or carry out operation. beause of '+str(e)
            
        
        
        
        
        
    #     # print("classifier_result=",classifier_result)
    #     if classifier_result[1] == 'A' or classifier_result[1] == 'C' or classifier_result[0] == False:
    #         return self.execute_question(user_nickname,question,added_prompt)
    #     elif classifier_result[1] == 'B':
    #         return self.execute_instruction(user_nickname,question,added_prompt)
    #     elif classifier_result[1] == 'N':
    #         return self.execute_question_naive(user_nickname,question,added_prompt)
    # def execute_question_naive(self,user_nickname,question,added_prompt=''):
    #     topn_chunks_from_pdf = []
    #     # assert False
    #     topn_chunks_prompt = ''
    #     sql_prompt = sql_prompt_(user_nickname)
    #     print('sql_prompt:',sql_prompt)
    #     topn_chunks_prompt += 'query_result[0]:'+sql_prompt+'\n\n'
    #     for idx,chunk in enumerate(topn_chunks_from_pdf):
    #         topn_chunks_prompt += 'query_result[' + str(idx+1) + ']:'+ chunk + '\n\n'
    #     query_info = "Begin of query information:" + topn_chunks_prompt + "End of query information." 
    #     my_prompt = "Instruction: Answer the user's question based on the query information.\n"\
    #         "Begin of query information:" + topn_chunks_prompt + "End of query information. Answer the user's question based on the query information.\n"\
    #         "Do NOT add any other information. Make sure the answer is exactly with the previous instructions. Do NOT output any error or extra information.\n"\
    #         "If you cannot answer the question, please answer 'I cannot answer the question. Please contact human customer service.' Be honest. Not Knowing is much better than Cheating!\n"\
    #         "Do NOT say something like 'refer to section II of the query answer for answer', state the detailed answer directly.\n"
    #     my_prompt += added_prompt
    #     print("Current executor prompt",my_prompt)
    #     my_prompt += "User's question:"+question+".Answer: The query information is all that I can see, and "
    #     llm_answer = self.ask_llm(my_prompt)
    #     return llm_answer
    # def execute_question(self,user_nickname,question,added_prompt=''):
    #     topn_chunks_from_pdf = self.guidefile_recommender(question)
    #     # assert False
    #     topn_chunks_prompt = ''
    #     sql_prompt = sql_prompt_(user_nickname)
    #     print('sql_prompt:',sql_prompt)
    #     topn_chunks_prompt += 'query_result[0]:'+sql_prompt+'\n\n'
    #     for idx,chunk in enumerate(topn_chunks_from_pdf):
    #         topn_chunks_prompt += 'query_result[' + str(idx+1) + ']:'+ chunk + '\n\n'
    #     query_info = "Begin of query information:" + topn_chunks_prompt + "End of query information." 
    #     my_prompt = "Instruction: Answer the user's question based on the query information.\n"\
    #         "Begin of query information:" + topn_chunks_prompt + "End of query information. Answer the user's question based on the query information.\n"\
    #         "Do NOT add any other information. Make sure the answer is exactly with the previous instructions. Do NOT output any error or extra information.\n"\
    #         "If you cannot answer the question, please answer 'I cannot answer the question. Please contact human customer service.' Be honest. Not Knowing is much better than Cheating!\n"\
    #         "Do NOT say something like 'refer to section II of the query answer for answer', state the detailed answer directly.\n"
    #     my_prompt += added_prompt
    #     print("Current executor prompt",my_prompt)
    #     my_prompt += "User's question:"+question+".Answer: The query information is all that I can see, and "
    #     llm_answer = self.ask_llm(my_prompt)
    #     return llm_answer
    
    # def execute_instruction(self,user_nickname,instruction,added_prompt=''):
    #     sql_prompt = sql_prompt_(user_nickname)
    #     print('sql_prompt:',sql_prompt)
    #     my_prompt = f"Instruction: Give operation,args and reason in the format Operation==operation|||Args==arg1,arg2,etc|||Reason==reason from the following operations based on user's instruction. If some args cannot be give, please use ? to replace it. Note that the user info in the database is {sql_prompt}. DO NOT add exgtra information!!!"
    #     my_prompt += 'Operations:' + self.executable_instructions
    #     my_prompt += "\n For example:"\
    #                 "User's Instruction: AddNewSchoolByName. Operation==AddNewSchoolByName|||Args==NewSchoolName,AreaName|||Reason==user wants to add a new school by name and provide school name and area name\n"\
    #                 "User's Instruction: please change my marking subject into 7. The operation should be: Operation==ChangeAllTypesMarkingSubject|||Args==7|||Reason==user wants to change marking subject and provide marking subject is 7\n"\
    #                 "User's Instruction: I want something to eat. The operation should be: Operation==?|||Args==?|||Reason==there are no executable commands that satisfy the users' request\n"\
    #                 "User's Instruction: please change my marking subject into 7. but the user is not in the systemm. The operation should be: Operaion==?|||Args==?|||Reason==user is not in the system, cannot execute command.\n"\
    #                 "User's Instruction: please chagne my marking subject into 7. The operation should be: Operation==ChangeAllTypesMarkingSubject|||Args==?|||Reason==user wants to change marking subject but did not provide its marking subject\n"\
    #                 "User's Instruction: please add a new school called TIUDJDH. The operation should be: Operation==AddNewSchoolByName|||Args==TIUDJDH,?|||Reason==user wants to add a new school but did not provide area name.\n"\
    #             "Do NOT add any other information. Make sure the answer is exactly with the previous instructions. Do NOT output any error or extra information. Do NOT hallucinate Args if the user does not provide it.\n"\
    #             "If there is no executable instructions, please answer 'Operation==?|||Args==?|||Reason==there are no executable commands that satisfy the users' request' Be honest. Not Knowing is much better than Cheating! If no args is needed, just set Args==None.DO NOT modify the name of the apis! DO NOT modify the name of the operations and instructions!\n"

    #     my_prompt += added_prompt
    #     my_prompt += "User's instruction:"+instruction+".The operation should be: Operaion=="
    #     llm_answer = self.ask_llm(my_prompt).replace("Operation==","")
        
        
    #     return llm_answer
