GPT_TOKEN = '...'
ENGINE = 'gpt-4'

import csv
qa_list = []
with open('QAs/instructions.csv', 'r') as f:
    reader = csv.reader(f)
    
    for row in reader:
        if len(row) <= 1:
            continue
        if row[0] == 'nickname':
            continue
        
        qa_list.append(row)


print(qa_list)
new_qa_list = []
import openai
def get_answer_from_gpt(prompt,
                        openAI_key=GPT_TOKEN,
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
def augment_questions(old_question_or_instruction):
    prompt = f"""Here is an user question or instruction. Please think of several (3 to 5) equivalent expressions, and separate using |||. DO NOT OUTPUT user_question_or_instruction==, DO NOT OUTPUT equivalen_expressions==, starting with your answer.
                For example:
                user_question_or_instruction==How many problems left do I have to mark?
                equivalent_expressions==How many problems left do I have to mark?|||How many remaining problems do I need to mark?|||What is the count of unmarked problems left for me?|||Can you tell me how many problems I still have to mark?|||How many problems are there still awaiting my marking?
                Another example:
                user_question_or_instruction==Do you charge fees for the exam?
                equivalent_expressions==Do you charge fees for the exam?|||Is there a fee associated with the exam?|||Are there any charges for taking the exam?|||Do I need to pay for the exam?|||Is the exam free, or is there a charge?
                Output according to the format and do NOT output any other things.
                user_question_or_instruction=={old_question_or_instruction}
                equivalen_expressions=={old_question_or_instruction}|||"""
    answer = get_answer_from_gpt(prompt)
    return answer.split('|||')

from copy import deepcopy

new_qa_list = []
from tqdm import tqdm
writer = csv.writer(open("QAs/instructions_augmented.csv", 'w', newline=''))
for idx,qa in tqdm(enumerate(qa_list)):
    if idx == 0:
        writer.writerow(qa)
        continue
    question = qa[1]
    # new_questions = augment_questions(question)
    for _ in range(4):
        new_qa = deepcopy(qa)
        new_qa[1] = question
        new_qa_list.append(new_qa)
        print(new_qa)
        writer.writerow(new_qa)
# save file into newQA.csv.
