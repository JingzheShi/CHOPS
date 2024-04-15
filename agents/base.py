from utils.llm_utils import get_answer_func_based_on_config_configs
import time
class BaseAgent():
    def __init__(self,agent_configs):
        self.agent_configs = agent_configs
        self._get_answer = get_answer_func_based_on_config_configs(agent_configs)
        self.output_to_log = agent_configs['output_to_log']
        if self.output_to_log:
            self.output_to_log_file_input = agent_configs['llm_log_file_input']
            self.output_to_log_file_output = agent_configs['llm_log_file_output']
            # create empty files.
            with open(self.output_to_log_file_input, 'w') as f:
                pass
            with open(self.output_to_log_file_output, 'w') as f:
                pass
    def ask_llm(self,prompt):
        # return self._get_answer(prompt)
        for idx in range(20):
            try:
                llm_answer = self._get_answer(prompt)
                if self.output_to_log:
                    # continue writing to the log file. do NOT overwrite previous logs.
                    with open(self.output_to_log_file_input, 'a') as f:
                        f.write(prompt+'\n')
                    with open(self.output_to_log_file_output, 'a') as f:
                        f.write(llm_answer+'\n')
                return self._get_answer(prompt)
            except Exception as e:
                print('Error in ask_llm',e)
                print('Retrying...')
                time.sleep(5.0)
    