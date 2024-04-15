from agents.base import BaseAgent
from utils.pdf_utils import SemanticSearch, load_recommender
from utils.other_utils import sql_prompt as sql_prompt_

from db_api.DataQueryApis import *

def obtain_choice(answer_str, choices = ['A','B','C','a','b','c']):
    answer = answer_str.replace('\"','').replace('\'','').replace(' ','').replace('\n','').replace('\t','').replace('  ','')
    for choice in choices:
        if choice in answer:
            return True,choice.upper()
    return False,None

class Classifier(BaseAgent):
    def __init__(self,agent_config):
        super().__init__(agent_config)
        self.recommender = SemanticSearch()
        load_recommender(self.recommender, agent_config['guidefile_path'],word_length = agent_config['word_length'],topk = agent_config['topk_chunks'])
        self.executable_instructions = ''
        self.use_multilayer = agent_config['use_multilayer']
        with open(agent_config['executable_instructions_path'],'r') as f:
            self.executable_instructions = f.read()
        print("Classifier is ready!")
    def classify_question_naive(self,user_nickname,question,added_prompt=''):
        # return True, 'B'
        topn_chunks_from_pdf = []
        topn_chunks_prompt = ''
        sql_prompt = sql_prompt_(user_nickname)
        topn_chunks_prompt += 'query_result[0]:'+sql_prompt
        for idx,chunk in enumerate(topn_chunks_from_pdf):
            topn_chunks_prompt += 'query_result[' + str(idx+1) + ']:'+ chunk + ''\
                ''\
                ''
        
        my_prompt = "Instruction: Classify the user's texts."\
                    "Answer A If the user is asking a question that you are confident to answer based on such query information:"\
                    "Begin of query information:" + topn_chunks_prompt + "End of query information. If the user is asking a question that can be answered by these query information, answer A."\
                    "Answer B otherwise."\
                    "Do NOT add any other information. Make sure the answer is exactly with the previous instructions. Do NOT output any error or extra information. Only output A,B or C."\
                    "Note only output A if you are very confident that the question can be perfectly answered by the query information!"\
                        
        my_prompt += added_prompt
        my_prompt += "User's texts:"+question+". Answer should be "
        llm_answer = self.ask_llm(my_prompt)
        llm_answer = llm_answer
        success_flag, choice = obtain_choice(llm_answer, ['A','B','C','a','b','c'])
        return success_flag, choice
    def classify_question(self,user_nickname,question, added_prompt = '',cycle_times=0):
        if self.use_multilayer:
            if cycle_times <= 1:
                naive_classify, naive_choice = self.classify_question_naive(user_nickname,question,added_prompt)
                if naive_classify and naive_choice == 'A':
                    return True, 'N'
        # return True, 'B'
        topn_chunks_from_pdf = self.recommender(question)
        topn_chunks_prompt = ''
        sql_prompt = sql_prompt_(user_nickname)
        topn_chunks_prompt += 'query_result[0]:'+sql_prompt
        for idx,chunk in enumerate(topn_chunks_from_pdf):
            topn_chunks_prompt += 'query_result[' + str(idx+1) + ']:'+ chunk + ''\
                ''\
                ''
        
        my_prompt = "Instruction: Classify the user's texts."\
                    "Answer A If the user is asking a question that is likely to be answered by these query information:"\
                    "Begin of query information:" + topn_chunks_prompt + "End of query information. If the user is asking a question that is likely to be answered by these query information, answer A."\
                    "Answer B If the user is making instruction to modify or add information or status or profile in the system, or if the user wants to use the following api to query information from the database, with operations listed below"+self.executable_instructions+". Answer B in this case."\
                    "Answer C otherwise."\
                    "Do NOT add any other information. Make sure the answer is exactly with the previous instructions. Do NOT output any error or extra information. Only output A,B or C."\
                        
        my_prompt += added_prompt
        my_prompt += "User's texts:"+question+". Answer should be "
        llm_answer = self.ask_llm(my_prompt)
        llm_answer = llm_answer
        success_flag, choice = obtain_choice(llm_answer, ['A','B','C','a','b','c'])
        return success_flag, choice
    