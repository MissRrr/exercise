#!/usr/bin/python3.6
#coding = utf-8

class Employee():
  def __init__(self,first_name,last_name,annual_salary):
    self.first_name = first_name
    self.last_name = last_name
    self.annual_salary = annual_salary

  
  def give_raise(self,add_raise=5000):
    self.annual_salary += add_raise
    return self.annual_salary


