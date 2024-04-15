from agents.executorOnly import ExecutorOnly
from configs_executor_only import total_config as current_config

from utils.other_utils import add_previous_prompts

executor = ExecutorOnly(current_config["agent_config"]["executor_config"])
MAX_TRY = current_config['max_try']

def answer_user_question(user_wechat_nickname, user_question, max_try=MAX_TRY):
    cycle_times = 0
    print(user_wechat_nickname+':',end=' ')
    print(user_question)
    answer_InvalidReason_list = []
    total_iter = max_try
    
    answer = executor.execute(user_wechat_nickname, user_question)
    return answer
                