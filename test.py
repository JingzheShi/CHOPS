from configs import total_config
from work_file import answer_user_question
from agents.base import BaseAgent
if total_config['auto_score_config']['auto_score']:
    scorer = BaseAgent(total_config['auto_score_config'])
else:
    scorer = None
import csv
new_list = list()

def right_or_wrong(question, correct_answer, worker_answer, scorer = scorer):
    my_prompt = f'''
        Instruction: Given the UserText (either question or instruction) and the teacher's standard reply, Judge whether the student's reply is Right or Wrong, and give your reason.The student may give extra information than the teacher, in which case THE STUDENT can be seen as RIGHT! Do NOT judge WRONG when extra information is provided.
        For example:
        UserText==Please complete my application my name is Name240393 and my marking subject should be 5; Teacher Standard Reply==your application has been successfully completed and your marking subject has been set to 5.; Student Reply==the user's application has been successfully completed.;Judge:Right;Reason:the student reply success which aligns with the teacher in term of reply to the instruction.
        UserText==Please make me an arbiter;Teacher Standard Reply==failed because you have not corrected all the test papers;Student Reply==the operation failed because The SubCoach has not finished correcting the test papers.; Judge==Right;Reason:the student replies fail and give a same reason as the teacher.
        UserText==Please let me be an team leader;Teacher Standard Reply==successfully changed;Student Reply==the user's request to become a team leader has been successfully executed.;Judge==Right;Reason: the student reply success which aligns with the teacher in term of reply to the instruction.
        UserText==Tell me information about users whose name is Andy;Teacher Standard Reply==You are not admin;Student Reply==the operation failed because the user making the query is not an admin and does not have the necessary privileges to access information in the system.;Judge==Right;Reason:the student reply fail and give a same reason as the teacher.
        UserText==Tell me information about users in the school schoolname344263;Teacher Standard Reply==the user with the id 1786 nickname 'nickname3487828' and username 'name7736854' is a team leader at school schoolname344263 with an upload limit of 100 and viewing problem of 5.Student Reply==the user with ID 1786 in the school named schoolname344263 is a team leader with the WeChat nickname 'nickname3487828' and the username 'name7736854'. They have an upload limit of 100, can view 5 problems, and have a school ID of 96.;Judge==Correct;Reason:the student reply with the same information as the teacher.
        UserText==Tell me information about users in the school schoolname344263;Teacher Standard Reply==the operation failed because you are not an admin and do not have the right to view information about users in the system.;Studnet Reply==the operation failed because the arguments provided were not complete.;Judge==Wrong;Reason:the student gives different reason as the teacher
        UserText==Please change my marking subject into 8.;Teacher Standard Reply==,sorry we cannot change your marking subject before you mark all your problems assigned.;Studnet Reply==the operation failed because the SubCoach has not finished correcting the test papers yet, which is necessary before changing the marking subject to 8.;Judge:Right;Reason:the studnet outputs the necessary information (to correct all answer sheets).
        UserText==Please change me into a vice team leader of the teacher whose name is name7546895,;Teacher Standard Reply==Successfully changed;Student Reply==No such executable command.Judge==Wrong;Reason:the student reply no such executable command but the teacher reply success.
        UserText==Please complete my application: my name is Name240393 and my marking subject should be 5;Teacher Standard Reply==,your application has been successfully completed and your marking subject has been set to 5.,;Student Reply==the marking subject for your application has been successfully changed to 5.;Judge: correct since the successful result is the same with the teacher.
        UserText==Please complete my application my name is Name240393 with marking subject should be 5';Teacher Standard Reply== 'your application has been successfully completed and your marking subject has been set to 5.';Student Reply==the user's application with the name Name240393, marking subject as 5, has been successfully verified for the role of Substitute Teacher;Judge:Right;Reason:correct since the successful result is the same with the teacher.
        UserText=={question};Teacher Standard Reply=={correct_answer};Student Reply=={worker_answer};Judge==
    '''
    if scorer is not None:
        llm_answer = scorer.ask_llm(my_prompt)
        if 'Right' in llm_answer[:20] or 'right' in llm_answer[:20] or 'Correct' in llm_answer[:20] or 'correct' in llm_answer[:20]:
            return True,llm_answer
        else:
            return False,llm_answer
    
right_number = 0
wrong_number = 0
with open(total_config['userText_csv_path'], 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for idx,row in enumerate(reader):
        if idx == 0:
            continue
        print("=========================================================================================")
        print(row)
        
        answer = answer_user_question(row[0],row[1])
        
        question = row[1]
        correct_answer = row[2]
        worker_answer = answer
        if scorer is not None:
            right_flag,llm_reason = right_or_wrong(question,correct_answer,worker_answer)
            if right_flag:
                right_number += 1
            else:
                wrong_number += 1
            total_number = right_number + wrong_number
            print("auto checked:",llm_reason)
            print(f"=======Current Correctly answered number: {right_number}/{total_number}; Current Wrongly answered number: {wrong_number}/{total_number}===============")
            new_row = [row[0],row[1],row[2],answer,llm_reason]
        else:
            new_row = [row[0],row[1],row[2],answer]
        new_list.append(new_row)
total_number = right_number + wrong_number
with open(total_config['result_csv_path'], 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['user_wechat_nickname','user_question','answer'])
    writer.writerows(new_list)
    if scorer is not None:
        writer.writerow([f'Auto-checked Correctly answered number: {right_number}/{total_number}', f'Auto-checked Wrongly answered number: {wrong_number}/{total_number}'])
