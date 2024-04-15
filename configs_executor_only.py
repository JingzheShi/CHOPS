from tokens import LLAMA_TOKEN, GPT_TOKEN, GLM_TOKEN
'''
llm:
    gpt: gpt-3.5-turbo, gpt-4-0125-preview
    glm: GLM-3-Turbo, GLM-4
    llama: llama-2-70b-chat
'''
EXP = 'MAIN_EXP_for_INs'

LOG_DIR = '0329logs_'+EXP+'\\'
import os
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

TAG = 'ExecutorOnly_gpt3.5_24032901'
DATA = 'newQAs'

TAG_DATA = TAG+'_'+DATA
total_config = dict(
    userText_csv_path = 'QAs/'+DATA+'.csv',
    result_csv_path = 'result/'+TAG_DATA+'_result.csv',
    agent_config = dict(
        classifier_config = None,
        executor_config = dict(
            llm = 'gpt-4-0125-preview',
            token = GPT_TOKEN,
            guidefile_path = ['guidefiles\\LeaderGuide_Eng.pdf','guidefiles\\Exam Paper Transmission questions.pdf','guidefiles\\Exam-related questions.pdf','guidefiles\\Grading-related questions.pdf','guidefiles\\Identity Change issues.pdf','guidefiles\\Score Release-related questions.pdf'],
            executable_instructions_path = 'guidefiles\\executable_operations.txt',
            word_length = 240,
            topk_chunks = 6,
            output_to_log = True,
            llm_log_file_input = LOG_DIR+TAG_DATA+'executor_input_words.txt',
            llm_log_file_output = LOG_DIR+TAG_DATA+'executor_output_words.txt',
            
        ),
        verifier_config = None,
    ),
    max_try = 5,
    auto_score_config = dict(
        auto_score = True,
        llm = 'gpt-4-0125-preview',
        token = GPT_TOKEN,
        output_to_log = False,
    )
    
)