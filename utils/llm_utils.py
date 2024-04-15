#调用glm使用的函数
import zhipuai
def get_answer_from_glm(AI_key,prompt,engine='chatglm_130b'):
    zhipuai.api_key=AI_key
    messages = [
        {
            'role':'user',
            'content':prompt,
        }
    ]
    response = zhipuai.model_api.invoke(
                model = engine,
                prompt = messages,
            )
    # print(response)
    return response['data']['choices'][-1]['content']




import openai
def get_answer_from_gpt(openAI_key,
                        prompt,
                        engine='gpt-3.5-turbo',
                        ):
    openai.api_key = openAI_key
    messages = [
        {
            'role': 'user',
            'content':prompt,
        }
    ]
    completions = openai.ChatCompletion.create(
        model = engine,
        messages = messages,
        max_tokens = 2048,
        n=1,
        stop=None,
        temperature=0.7
    )
    # print(completions)
    message = completions.choices[-1]['message']['content']
    return message
import replicate
import os
from tqdm import tqdm
def get_answer_from_llama(llama_key,
                          prompt,
                          engine='llama-2-70b-chat'):
    engine = 'meta/' + engine
    if 'chat' in engine:
        answer_list = list()
        os.environ["REPLICATE_API_TOKEN"] = llama_key
        for event in replicate.stream(
                    engine,
                    input = dict(
                        debug = False,
                        top_p = 0.9,
                        prompt = prompt,
                        temperature = 0.5,
                        system_prompt = "You are a helpful, respectful and honest assistant.",
                        max_new_tokens = 500,
                        min_new_tokens = -1,
                        prompt_template = "[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]",
                        repetition_penalty = 1.15,
                    )
                ):
            answer_list.append(event)
        # answer_str: join the answer_list into a string.
        answer_str = ""
        for answer in answer_list:
            answer_str += str(answer)
        return answer_str
    else:
        answer_list = list()
        os.environ["REPLICATE_API_TOKEN"] = llama_key
        for event in replicate.stream(
                    engine,
                    input = dict(
                        debug = False,
                        top_p = 0.9,
                        prompt = prompt,
                        temperature = 0.7,
                        max_new_tokens = 500,
                        min_new_tokens = -1,
                        prompt_template = "{prompt}",
                        presence_penalty = 0,
                    )
                ):
            answer_list.append(event)
        # answer_str: join the answer_list into a string.
        answer_str = ""
        for answer in answer_list:
            answer_str += str(answer)
        return answer_str

def get_answer_func_based_on_config_configs(
    agent_config,
):
    # print(agent_config)
    if 'GLM'in agent_config['llm'] or 'glm' in agent_config['llm']:
        func = get_answer_from_glm
        # print('glm1')
    elif 'gpt' in agent_config['llm']:
        func = get_answer_from_gpt
        # print("gpt2")
    elif 'llama'in agent_config['llm'] or 'LLaMa'in agent_config['llm'] or 'LLAMA' in agent_config['llm']:
        func = get_answer_from_llama
        # print('llama3')
    else:
        raise ValueError('No such engine found!')
    def new_func(prompt):
        return func(agent_config['token'],prompt,agent_config['llm'])
    return new_func


if __name__ == '__main__':
    from tokens import LLAMA_TOKEN, GPT_TOKEN, GLM_TOKEN
    prompt = "Hello!"
    
    
    
    question = 'Who am I?'

    my_prompt = "Query from database:" + 'This user is a team leader' + "Instruction: answer user's question based on the previous query information from database。"\
                    "Do not add additional information. Ensure the answer is consistent with the query information, and do not output errors or extra content."\
                    "If the user's question is irrelevant to the query information, simply answer Unable to query related information. Ignore query results irrelevant to the question."\
                    "The answer should be short and accurate. Address the user as 'You'."

    my_prompt += 'User question:'+question+'Answer: In short, '
    print("Our input prompt is:", my_prompt)
    print("Now testing LLaMa-2-70b-chat.")
    try:
        answer = get_answer_from_llama(LLAMA_TOKEN,my_prompt,'llama-2-70b-chat')
        print("Answer is:")
        print(answer)
    except Exception as e:
        print('1',e)
    
    print("\nNow testing gpt-3.5-turbo")
    try:
        answer = get_answer_from_gpt(GPT_TOKEN,my_prompt,'gpt-3.5-turbo')
        print("Answer is:")
        print(answer)
    except Exception as e:
        print('2',e)
    
    print("\nNow testing GLM-3-Turbo")
    try:
        answer = get_answer_from_glm(GLM_TOKEN,my_prompt,'GLM-3-Turbo')
        print("Answer is:")
        print(answer)
    except Exception as e:
        print('3',e)

    