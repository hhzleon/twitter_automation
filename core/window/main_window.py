import sys
sys.path.append('d:/code/twitterAuto')

from core.database.User import User
from core.database.Task import Task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.TFA import getTwoFa

class Main_Window:
    Session = None 
    def __init__(self) -> None:
        engine = create_engine('sqlite:///data.db')
        self.Session = sessionmaker(bind=engine)

    # 获取用户列表
    def getUserList(self):
        session = self.Session()
        try:
            users = session.query(User).all()
            user_list = [
                {
                    'UserID': user.id, 
                    'Username': user.username, 
                    'Password': user.password, 
                    'TwoFactorAuth': user.twoFa, 
                    'TwoFaKey': user.twoFaKey, 
                    'Cookies': user.cookies, 
                    'Nickname': user.nickname, 
                    'Signature': user.signature, 
                    'AvatarURL': user.avatar_url, 
                    'BackgroundURL': user.background_url
                } 
                for user in users
            ]
            return user_list
        finally:
            session.close()

    # 修改用户信息
    def changeUserData(self, user_id, new_data):
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                for key, value in new_data.items():
                    setattr(user, key, value)
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            print("An error occurred while updating user data:", e)
            return False
        finally:
            session.close()
    # 获取用户的2FA
    def getUser2FACode(self, key):
        return getTwoFa(key)
    # 查询用户信息
    def selectUserData(self, user_id):
        session = self.Session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                user_data = {
                    'UserID': user.id,
                    'Username': user.username,
                    'Password': user.password,
                    'TwoFa': user.twoFa,
                    'TwoFaKey': user.twoFaKey,
                    'Cookies': user.cookies,
                    'Nickname': user.nickname,
                    'Signature': user.signature,
                    'AvatarUrl': user.avatar_url,
                    'BackgroundUrl': user.background_url,
                }
                return user_data
            else:
                return None
        except Exception as e:
            print("An error occurred while fetching user data:", e)
            return None
        finally:
            session.close()


    # 导出账户

    # 导入账户



    # 获取任务列表
    def getTaskList(self):
        session = self.Session()
        try:
            tasks = session.query(Task).all()
            task_list = [
                {
                    'TaskID': task.id,
                    'UserID': task.userid,
                    'Status': task.status,
                    'TaskType': task.task_type,
                    'Args': task.args,
                    'Notes': task.notes
                }
                for task in tasks
            ]
            return task_list
        finally:
            session.close()

    # 新建任务列表
        # 关联账户id
        # 任务状态
        # 任务类型
        # 参数
        # 备注
    def insertTask(self, TaskDictData):
        session = self.Session()
        try:
            new_task = Task(
                userid=TaskDictData['userid'],
                status=TaskDictData['status'],
                task_type=TaskDictData['task_type'],
                args=TaskDictData['args'],
                notes=TaskDictData['notes']
            )
            session.add(new_task)
            session.commit()
            return new_task.id
        except Exception as e:
            print("An error occurred while inserting task:", e)
            session.rollback()
            return None
        finally:
            session.close()

    # 获取任务列表

if __name__=="__main__":
    # L = Main_Window().getTaskList()
    # for i in L:
    #     print (i)
    L = Main_Window().getUser2FACode("BA6U6YT5XYDJNCZD")
    print(L)