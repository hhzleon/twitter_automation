import sys
sys.path.append('d:/code/twitterAuto')
from unittest import TestCase,skip
import unittest
from ddt import ddt,unpack,file_data
from twitterAuto import TwitterAuto
from core.database.User import User
from core.database.Task import Task
import webview

import logging
logging.basicConfig(filename="app_errors.log",level=logging.ERROR)

@ddt
class TestTwitterAuto(TestCase):
    pass
    # @file_data(r"D:\code\twitterAuto\testUserData_1.json")
    # @unpack
    # # @skip("测试过了")
    # def test_login(self,id,username,password,key,auth_token,email):
    #     print ("Test User",username)
    #     user = User()
    #     task = Task()
    #     user.username = username
    #     user.password = password
    #     user.twoFaKey = key 
    #     user.id = id
    #     user.email = email
    #     TwitterAuto(user=user,task=task).login()
    @file_data(r"D:\code\twitterAuto\testUserData_1.json")
    @unpack
    # @skip("测试过了")
    def test_modify_info(self,id,username,password,key,auth_token,email):
        print ("Test User",username)
        user = User()
        user.cookies = auth_token 
        user.avatar_url = r"C:\Users\work\Pictures\PixPin_2024-11-23_19-16-58.png"
        user.id = id
        user.nickname = "Hello"
        user.signature = "HelloWorld1"
        task = Task()
        ot = TwitterAuto(user=user,task=task)
        self.assertTrue(ot.error_handler(ot.modify_info()))
    # @skip("测试过了")
    # def test_checkRequestIsTrue(self):
    #     user = User()
    #     user.avatar_url = r"C:\Users\work\Pictures\PixPin_2024-11-23_19-16-58.png"
    #     user.id = id
    #     task = Task()
    #     ot = TwitterAuto(user=user,task=task)
    #     def wrapper():
    #         ot.modify_info()
    #     self.assertTrue(ot.error_handler(wrapper))

if __name__ == "__main__":
    unittest.main()


