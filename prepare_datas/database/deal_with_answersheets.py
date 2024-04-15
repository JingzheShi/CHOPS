import json
import random
org_list = json.load(open('cmf_tp_correct_old.json'))
new_list = list()
for item in org_list:
    new_list.append(dict(
        id = item['id'],
        user_id = item['user_id'],
        p_id = item['p_id'],
        grade = item['grade'],
        status = item['status'],
        create_time = item['create_time'],
    ))
# Now, let's write the new list into the file.
with open('cmf_tp_correct.json', 'w', encoding='utf-8') as f:
    # json.dump(new_list, f)
    # pretty print.
    json.dump(new_list, f, indent=4)

org_list = json.load(open('cmf_tp_subject_old.json'))
new_list = list()
for item in org_list:
    new_list.append(dict(
      id = item['id'],
      p_id = item['p_id'],
      subject = item['subject'],
      image =  "" if item['image'] == "" else item["image"][13:],
      grade = item["grade"],
      status = item["status"],
      create_time = item["create_time"],
    ))
# Now, let's write the new list into the file.
with open('cmf_tp_subject.json', 'w', encoding='utf-8') as f:
    # json.dump(new_list, f)
    # pretty print.
    json.dump(new_list, f, indent=4)

org_list = json.load(open('cmf_tp_test_paper_old.json'))
new_list = list()
for item in org_list:
    new_list.append(dict(
      id = item['id'],
      p_id = item['p_id'],
      user_id = item['user_id'],
      student_id = item['student_id'],
      score = item['score'],
      eight = item['eight'],
      two = item['two'],
      create_time = item["create_time"],
    ))
# Now, let's write the new list into the file.
with open('cmf_tp_test_paper.json', 'w', encoding='utf-8') as f:
    # json.dump(new_list, f)
    # pretty print.
    json.dump(new_list, f, indent=4)
print("Done!")