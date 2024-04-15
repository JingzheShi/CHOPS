import json
org_list = json.load(open('cmf_tp_school_old.json',encoding='utf-8'))
new_list = []
for item in org_list:
    new_list.append(dict(
        id = item['id'],
        area = item['area'],
        school_name = 'schoolname'+str(2*abs(hash(item['school_name'])) + 1 if hash(item['school_name']) < 0 else 2*abs(hash(item['school_name'])))[-6:],
    ))
# Now, let's write the new list into the file.
with open('cmf_tp_school.json', 'w', encoding='utf-8') as f:
    # json.dump(new_list, f)
    # pretty print.
    json.dump(new_list, f, indent=4)