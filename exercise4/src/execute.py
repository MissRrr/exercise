'''
Created on Nov 12, 2020

@author: Celia
'''
#coding=UTF-8
'''导入test包,需要在test包的__init__.py里面导入test包的user模块或者在导入包时准确导入user模块,e.g.import test.user as u'''
import test

'''题目：创建一个名为 User 的类,其中包含属性 first_name 和 last_name 。在类 User 中定义一个名为 describe_user() 的方法,
      它打印用户信息,再创建一个文件,在其中创建一个 User 实例并对其调用方法 describe_user() ,以确认一切都能正确地运行。'''
      
if __name__ == '__main__':
    user = test.user.User('Herry','Tang')
    user.describe_user()