import pymysql
import json
# localhost
# 3306
# root
# CPHOS_dataset_2
PASSWORD = 'BaOyy95GG6OC'
cmf_tp_area_json = json.load(open('cmf_tp_area.json',encoding='utf-8'))
cmf_tp_exam_json = json.load(open('cmf_tp_exam.json',encoding='utf-8'))
cmf_tp_member_json = json.load(open('cmf_tp_member.json',encoding='utf-8'))
cmf_tp_school_json = json.load(open('cmf_tp_school.json',encoding='utf-8'))
cmf_tp_student_json = json.load(open('cmf_tp_student.json',encoding='utf-8'))

cmf_tp_correct = json.load(open('cmf_tp_correct.json'))
cmf_tp_subject = json.load(open('cmf_tp_subject.json'))
cmf_tp_test_paper = json.load(open('cmf_tp_test_paper.json'))

cmf_tp_admin = json.load(open('cmf_tp_admin.json'))

# Connect to the database.
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password=PASSWORD,
    db='CPHOS_dataset_2',
    charset='utf8',
)
cursor = conn.cursor()
# create cmf_tp_area.
cursor.execute('drop table if exists cmf_tp_area')
cursor.execute('create table cmf_tp_area(id int primary key,area_name varchar(255))')
# create cmf_tp_exam.
cursor.execute('drop table if exists cmf_tp_exam')
cursor.execute('create table cmf_tp_exam(id int primary key,title varchar(255),status int, type int, `show` int, create_time int)')
# create cmf_tp_member.
cursor.execute('drop table if exists cmf_tp_member')
cursor.execute('create table cmf_tp_member(id int primary key,p_id int,user_name varchar(255),school_id int,subject int,status int,type int,`limit` int,create_time int,nickname varchar(255))')

# create cmf_tp_school.
cursor.execute('drop table if exists cmf_tp_school')
cursor.execute('create table cmf_tp_school(id int primary key,area int,school_name varchar(255))')
# create cmf_tp_student.
cursor.execute('drop table if exists cmf_tp_student')
cursor.execute('create table cmf_tp_student(id int primary key, user_id int, name varchar(255), school int, grade varchar(255), prize varchar(255))')

# create cmf_tp_correct.
cursor.execute('drop table if exists cmf_tp_correct')
cursor.execute('create table cmf_tp_correct(id int primary key,user_id int,p_id int,grade float,status int,create_time int)')

# create cmf_tp_subject.
cursor.execute('drop table if exists cmf_tp_subject')
cursor.execute('create table cmf_tp_subject(id int primary key,p_id int,subject int,image varchar(255),grade float,status int,create_time int)')

# create cmf_tp_test_paper.
cursor.execute('drop table if exists cmf_tp_test_paper')
cursor.execute('create table cmf_tp_test_paper(id int primary key,p_id int,user_id int,student_id int,score float,eight float,two float,create_time int)')  

cursor.execute('drop table if exists cmf_tp_admin')
cursor.execute('create table cmf_tp_admin(id int primary key, user_id int)')



# Insert data into the database.
for item in cmf_tp_area_json:
    cursor.execute('insert into cmf_tp_area(id,area_name) values(%s,%s)', (item['id'],item['area']))
for item in cmf_tp_exam_json:
    cursor.execute('insert into cmf_tp_exam(id,title,status,type,`show`,create_time) values(%s,%s,%s,%s,%s,%s)', (item['id'],item['title'],item['status'],item['type'],item['show'],item['create_time']))
for item in cmf_tp_member_json:
    cursor.execute('insert into cmf_tp_member(id,p_id,user_name,school_id,subject,status,type,`limit`,create_time,nickname) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (item['id'],item['p_id'],item['user_name'],item['school_id'],item['subject'],item['status'],item['type'],item['limit'],item['create_time'],item['nickname']))
for item in cmf_tp_school_json:
    cursor.execute('insert into cmf_tp_school(id,area,school_name) values(%s,%s,%s)', (item['id'],item['area'],item['school_name']))
for item in cmf_tp_student_json:
    cursor.execute('insert into cmf_tp_student(id,user_id,name,school,grade,prize) values(%s,%s,%s,%s,%s,%s)', (item['id'],item['user_id'],item['name'],item['school'],item['grade'],item['prize']))
for item in cmf_tp_correct:
    cursor.execute('insert into cmf_tp_correct(id,user_id,p_id,grade,status,create_time) values(%s,%s,%s,%s,%s,%s)', (item['id'],item['user_id'],item['p_id'],item['grade'],item['status'],item['create_time']))
for item in cmf_tp_subject:
    cursor.execute('insert into cmf_tp_subject(id,p_id,subject,image,grade,status,create_time) values(%s,%s,%s,%s,%s,%s,%s)', (item['id'],item['p_id'],item['subject'],item['image'],item['grade'],item['status'],item['create_time']))
for item in cmf_tp_test_paper:
    cursor.execute('insert into cmf_tp_test_paper(id,p_id,user_id,student_id,score,eight,two,create_time) values(%s,%s,%s,%s,%s,%s,%s,%s)', (item['id'],item['p_id'],item['user_id'],item['student_id'],item['score'],item['eight'],item['two'],item['create_time']))
for item in cmf_tp_admin:
    cursor.execute('insert into cmf_tp_admin(id,user_id) values(%s,%s)', (item['id'],item['user_id']))


# commit the transaction.
conn.commit()
# close the cursor.
cursor.close()