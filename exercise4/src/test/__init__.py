#coding=utf-8
#需要在package的__init__.py里面导入该package的module,不然将test这个包导入到别的文件时不会自动导入user模块
import test.user

'''
笔记记录：
    Q：如何在不改动execute.py文件的前提下，test包还可以放在哪里，能使程序正常运行？
       （execute.py文件中，test包的导入语句是import test）
    A：可以利用sys模块的path成员量，使用sys.path.append(),添加加test包所在路径，
       因为Python搜索模块的路径是由四部分构成的：程序的主目录、PATHONPATH目录、标准链接库目录
       和.pth文件的目录，这四部分的路径都存储在sys.path列表中，从而不需要修改import test语句
       来说明test的存放路局径，Python也能搜索到test包
'''