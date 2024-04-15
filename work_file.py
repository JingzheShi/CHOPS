from agents.classifier import Classifier
from agents.executor import Executor
from agents.verifier import Verifier
from configs import total_config as current_config

from utils.other_utils import add_previous_prompts

classifier = Classifier(current_config["agent_config"]["classifier_config"])
executor = Executor(current_config["agent_config"]["executor_config"])
verifier = Verifier(current_config["agent_config"]["verifier_config"])
MAX_TRY = current_config['max_try']

def answer_user_question(user_wechat_nickname, user_question, max_try=MAX_TRY):
    cycle_times = 0
    print(user_wechat_nickname+':',end=' ')
    print(user_question)
    answer_InvalidReason_list = []
    total_iter = max_try
    while True:
        added_prompt = ''
        if len(answer_InvalidReason_list) > 0:
            added_prompt += add_previous_prompts(answer_InvalidReason_list)
        classified_success, classifier_result = classifier.classify_question(user_wechat_nickname, user_question, added_prompt, cycle_times)
        classifier_result = 'B' if not classified_success else classifier_result
        executor_result = executor.execute(user_wechat_nickname, user_question, added_prompt, (classified_success,classifier_result))
        verifier_valid, invalid_reason, replied_result = verifier.verify_and_reply(user_wechat_nickname, user_question,  (classified_success,classifier_result), executor_result, added_prompt, cycle_times, total_iter, answer_InvalidReason_list)
        
        if verifier_valid:
            return replied_result
        else:
            answer_InvalidReason_list.append((executor_result, invalid_reason))
            cycle_times += 1
            if cycle_times > max_try:
                return 'I cannot answer the question. Please contact human customer service.'
                