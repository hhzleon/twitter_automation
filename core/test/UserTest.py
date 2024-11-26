import unittest
import sys
sys.path.append('d:/code/twitterAuto')
from core.user import User
class UserTest(unittest.TestCase):
    def test_user_to_dict(self):
        user = User()
        user.id = 1
        user.username = 'test_user'
        user.password = 'password123'
        user.twoFa = 1234
        user.twoFaKey = 'key1234'
        user.cookies = 'cookie123'
        user.nickname = 'Test User'
        
        user_dict = user.to_dict()
        
        self.assertEqual(user_dict['id'], 1)
        self.assertEqual(user_dict['username'], 'test_user')
        self.assertEqual(user_dict['password'], 'password123')
        self.assertEqual(user_dict['twoFa'], 1234)
        self.assertEqual(user_dict['twoFaKey'], 'key1234')
        self.assertEqual(user_dict['cookies'], 'cookie123')
        self.assertEqual(user_dict['nickname'], 'Test User')

if __name__ == "__main__":
    unittest.main()


