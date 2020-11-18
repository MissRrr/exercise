#!/usr/bin/python3.6
#coding=utf-8

import sqlite3

DB = sqlite3.connect('student.db')

QUERY_CURS = DB.cursor()

def init():
  '''初始化函数'''
  #判断students表是否已经创建，未创建则创建并初始化
  QUERY_CURS.execute('select count(*) from sqlite_master where type="table" and name="students"')
  is_exists = QUERY_CURS.fetchone()[0]
  #不存在创表
  if not is_exists:
    QUERY_CURS.execute('CREATE TABLE students (id INTEGER PRIMARY KEY,name TEXT,age INTEGER,sex TEXT)')
    add_new('Jane Li',12,'F')
    add_new('Jan Tong',11,'M')
    add_new('Mandy Jin',12,'F')
    add_new('Jack Chen',13,'M')
    DB.commit()
  else:
    return
    

def add_new(name,age,sex):
  '''新增学生信息'''
  if variable_is_Empty(name) or variable_is_Empty(age) or variable_is_Empty(sex):
    print('this add is invalid.')
    return
  else:
    QUERY_CURS.execute('''INSERT INTO students (name,age,sex) VALUES (?,?,?)''',(name,age,sex))
    print('add a new student successfully.')


def update_student(name,age,sex,student_id):
  '''根据学生ID进行更新学生信息'''
  #动态拼接参数和sql语句
  parameters=[]
  sql='update students set '
  if not variable_is_Empty(name):  
    parameters.append(name.strip())
    sql += 'name = ? ,'
  elif not variable_is_Empty(age):
    parameters.append(int(age))
    sql += 'age = ? ,'
  elif variable_is_Empty(sex):
    parameters.append(sex.strip())
    sql += 'sex = ? ,'
  else:
    sql = ''
  #判断三个参数是否都为空或者id为空
  if len(sql)==0:
    print('this update is invalid.')
  elif variable_is_Empty(student_id):
    print('this update is invalid.')
  else:
    parameters.append(student_id)
    sql = sql.strip(',') + ' where id = ? '
    #print(sql)
    QUERY_CURS.execute(sql,parameters)
    #DB.commit()
    print('this update is successful.') 


def search_student_by_name(name):
  '''根据学生姓名搜索，返回一个list'''
  return list(QUERY_CURS.execute('select * from students where name = ? ',[name]))


def delete_student_by_id(student_id):
  '''根据学生id删除学生信息'''
  if variable_is_Empty(student_id):
    print('this delete is invalid.')
    return
  else:
    QUERY_CURS.execute('delete from students where id = ? ',[student_id])
    #QUERY_CURS.execute('delete from students where id=1')
    print('this delete is successful')


def get_students_list():
  '''获取全部学生列表，返回一个list'''
  return list(QUERY_CURS.execute('select * from students '))


def print_list(students_list,list_title):
  '''打印查询结果列表'''
  #字段list下标
  k = 0
  for list_value in students_list:
    for value in list_value:
      print(f'{list_title[k]}:{value}')
      #最后一个字段打印一个分隔符分隔
      if(k==3): print('\n')
      #字段list下标自增
      if k<3: k+=1
      else: k = 0
      
      
def variable_is_Empty(variable):
  '''判断字符串是否为空，是否全为空格'''
  return (variable == '' or variable.strip() == '' or len(variable) == 0 or variable.isspace())

def main():
  
  init()
  print('1:add a student information')
  print('2:update a student information by id')
  print('3:search a student information by name')
  print('4:delete a student information by id')
  print('5:get all students information')
  
  list_title =['id','name','age','sex']
  while True:
    #输入'q'跳出最外层的循环
    input_number = input('select what you want to do!\n')
    if input_number == 'q':
      DB.close()
      break
    while input_number is not 'q':
      if input_number is '1':
        name = input('please enter the student name:')
        age = input('please enter the student age:')
        sex = input('please enter the student sex:')
        add_new(name,age,sex)
        break
      elif input_number is '2':
        student_id = input('please enter the id whose you want to update:')
        name = input('if you want to change this student\'s name,please enter a new student name or press enter to skip:')
        age = input('if you want to change this student\'s age,please enter a new student age or press enter to skip:')
        sex = input('if you want to change this student\'s sex,please enter a new student sex or press enter to skip:')
        update_student(name,age,sex,student_id)
        break
      elif input_number is '3':
        name = input('please enter the name whose you want to search:')
        students_list = search_student_by_name(name.strip())
        print_list(students_list, list_title)
        break
      elif input_number is '4':
        student_id = input('please enter the id whose you want to delete:')
        delete_student_by_id(student_id)
        break
      elif input_number is '5':
        students_list = get_students_list()
        print_list(students_list, list_title)
        break
      else:
        print('please enter a right number')
        break
    print('if you want to quit,please enter the "q"!')



if __name__=='__main__':
  main()
