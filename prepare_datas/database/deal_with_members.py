import json
org_list = json.load(open('cmf_tp_member_old.json',encoding='utf-8'))
new_list = []
import random
for item in org_list:
    print(item['user_name'])
    if item['user_name'] is not None:
        new_list.append(dict(
            id = item['id'],
            p_id = item['p_id'],
            user_name = 'name'+str(2*abs(hash(item['user_name'])) + 1 if hash(item['user_name']) < 0 else 2*abs(hash(item['user_name'])))[-7:],
            school_id = item['school_id'],
            subject = item['subject'],
            status = item['status'],
            type = item['type'],
            limit = item['limit'],
            create_time = item['create_time'],
            nickname = 'nickname'+str(abs(hash(item['nickname'])) + 1 if hash(item['nickname']) < 0 else abs(hash(item['nickname'])))[-7:],
        ))
# Now, let's write the new list into the file.
with open('cmf_tp_member.json', 'w', encoding='utf-8') as f:
    # json.dump(new_list, f)
    # pretty print.
    json.dump(new_list, f, indent=4)