import json
org_list = json.load(open('cmf_tp_student_old.json',encoding='utf-8'))
new_list = []
trans_dict = {
    '全国三等奖':"CountryBronze",
    '全国二等奖':"CountrySilver",
    '全国一等奖':"CountryGold",
    '其他':      "Other",
    '省级一等奖':"ProvinceGold",
    '省级二等奖':"ProvinceSilver",
    '省级三等奖':"ProvinceBronze",
    "":"Other",
}
for item in org_list:
    new_list.append(dict(
        id = item['id'],
        user_id = item['user_id'],
        name = 'studentname'+str(2*abs(hash(item['name'])) + 1 if hash(item['name']) < 0 else 2*abs(hash(item['name'])))[-8:],
        school= item['school'],
        grade = item['grade'],
        prize = trans_dict[item['prize']],
    ))
# Now, let's write the new list into the file.
with open('cmf_tp_student.json', 'w', encoding='utf-8') as f:
    # json.dump(new_list, f)
    # pretty print.
    json.dump(new_list, f, indent=4)