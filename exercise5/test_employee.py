#!/usr/bin/python3.6
#coding = utf-8

import unittest

from employee import Employee

'''
题目:
  编写一个名为 Employee 的类,其方法 __init__() 接受名、姓和年薪,并将它们都存储在属性中。编写一个名为 give_raise() 的方法,它默认将年薪增加 5000 美元,但也能够接受其他的年薪增加量。
  为 Employee 编写一个测试用例,其中包含两个测试方法: test_give_default_raise() 和 test_give_custom_raise() 。使用方法 setUp() ,以免在每个测试方法中都创建新的雇员实例。运行这个测试用例,确认两个测试都通过了。
'''

class TestEmployee(unittest.TestCase):
   #该函数是unittest内置函数，函数名是固定的，在每个测试case运行前运行
   def setUp(self):
    #存储Employee实例对象在属性中,因此可在这个类的任何地方使用
    self.test_employee = Employee('Jane','Li',7000)
   
   
   def test_give_default_raise(self):
     self.assertEqual(12000,self.test_employee.give_raise())
  
   
   def test_give_custom_raise(self):
     self.assertEqual(15000,self.test_employee.give_raise(8000))

if __name__ == '__main__':
  unittest.main()
