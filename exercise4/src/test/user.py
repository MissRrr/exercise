'''
Created on Nov 12, 2020

@author: Celia
'''
#！/usr/bin/python3.6

class User():
    def __init__(self, first_name ,last_name):
        self.first_name = first_name
        self.last_name = last_name
        
        
    def describe_user(self):
      print(f'User:{self.first_name} {self.last_name}')
        