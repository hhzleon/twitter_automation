import sys
sys.path.append('d:/code/twitterAuto')
from unittest import TestCase,skip
import unittest
from ddt import ddt,unpack,file_data
from twitterAuto import TwitterAuto
from core.database.User import User
import webview
@ddt
class TestTwitterAuto(TestCase):
    pass
    @file_data("../../testUserData_1.json")
    @unpack
    @skip("测试过了")
    def test_login(self,id,username,password,key,auth_token):
        print ("Test User",username)
        user = User()
        user.username = username
        user.password = password
        user.twoFaKey = key 
        user.id = id
        self.assertTrue(TwitterAuto(user=user).login())
    @file_data("../../testUserData_1.json")
    @unpack
    @skip("测试过了")
    def test_modify_info(self,id,username,password,key,auth_token):
        print ("Test User",username)
        user = User()
        user.cookies = auth_token 
        user.id = id
        self.assertTrue(TwitterAuto(user=user).modify_info())

if __name__ == "__main__":
    unittest.main()


