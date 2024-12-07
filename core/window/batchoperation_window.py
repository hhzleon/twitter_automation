import sys
sys.path.append('d:/code/twitterAuto')
import webview
from core.database.User import User
from core.database.Task import Task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class batchoperation_api:
    Session = None 
    def __init__(self, users) -> None:
        engine = create_engine('sqlite:///data.db')
        self.Session = sessionmaker(bind=engine)
        
        self.users = users  # 接受传入的用户

    def selectNicknames(self): # 选择昵称文件 一行一个
        file_types = ('Image Files (*.bmp;*.jpg;*.gif;*.png)','All files (*.*)')
        w = webview.create_window("Hello",width=1,height=1,frameless=True)
        w.hide()
        result = w.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types
        )
        w.destroy()
        file_path = result[0]
        with open(file=file_path,mode="r",encoding="UTF-8") as f:
            text = f.read()
            f.close()
        return {
            "file_path": file_path,
            "text": text
        }

    def selectSignatures(self): # 选择签名文件 一行一个
        file_types = ('Image Files (*.bmp;*.jpg;*.gif;*.png)','All files (*.*)')
        w = webview.create_window("Hello",width=1,height=1,frameless=True)
        w.hide()
        result = w.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types
        )
        w.destroy()
        file_path = result[0]
        with open(file=file_path,mode="r",encoding="UTF-8") as f:
            text = f.read()
            f.close()
        return {
            "file_path": file_path,
            "text": text
        }

    def selectAvatarURL(self): # 选择头像 返回str path
        file_types = ('Image Files (*.bmp;*.jpg;*.gif;*.png)', 'All files (*.*)')
        w = webview.create_window("Hello",width=1,height=1,frameless=True)
        w.hide()
        result = w.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types
        )
        w.destroy()
        return result[0]

    def selectBackgroundUrl(self): # 选择背景 URL 返回str path
        file_types = ('Image Files (*.bmp;*.jpg;*.gif;*.png)', 'All files (*.*)')
        w = webview.create_window("Hello",width=1,height=1,frameless=True)
        w.hide()
        result = w.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types
        )
        w.destroy()
        return result[0]

    # 新建任务列表
        # 关联账户id
        # 任务状态
        # 任务类型
        # 参数
        # 备注
    def insertTask(self, TaskDictData):
        session = self.Session()
        # try:
        new_task = Task()
        print (TaskDictData)
        new_task.userid = TaskDictData['userid']
        new_task.status = TaskDictData['status']
        new_task.task_type = TaskDictData['task_type']
        new_task.args = TaskDictData['args']
        new_task.notes = TaskDictData['notes']
        session.add(new_task)
        session.commit()
        return new_task.id
        # except Exception as e:
            # print("An error occurred while inserting task:", e)
            # session.rollback()
            # return None
        # finally:
            # session.close()

        # session = self.Session()
        # try:
        #     new_task = Task()
        #     new_task.userid = TaskDictData['userid']
        #     new_task.status = TaskDictData['status']
        #     new_task.task_type = TaskDictData['task_type']
        #     new_task.args = TaskDictData['args']
        #     new_task.notes = TaskDictData['notes']
        #     session.add(new_task)
        #     session.commit()
        #     return new_task.id
        # except Exception as e:
        #     print("An error occurred while inserting task:", e)
        #     session.rollback()
        #     return None
        # finally:
        #     session.close()
    
    def modifyUserInfo(self, userInfo):
        """
        修改用户信息
        """
        session = self.Session()
        try:
            user_to_update = session.query(User).filter_by(id=userInfo['id']).first()
            if user_to_update:
                user_to_update.nickname = userInfo['nickname']
                user_to_update.signature = userInfo['signature']
                user_to_update.avatar_url = userInfo['avatar_url']
                user_to_update.background_url = userInfo['background_url']
                session.commit()
                return True
            else:
                print(f"User with ID {userInfo['id']} not found.")
                return False
        except Exception as e:
            print(f"An error occurred while modifying user info: {e}")
            session.rollback()
            return False
        finally:
            session.close()



    def returnUsers(self):
        # 创建SQLAlchemy会话
        session = self.Session()
        try:
            # 查询并返回用户列表
            users = session.query(User).filter(User.id.in_(self.users)).all()
            
            return [
                {
                    'UserID': user.id,
                    'Username': user.username,
                    'Signature': user.signature,
                    'AvatarURL': user.avatar_url,
                    'Status': 1 if user.cookies else 2  # 检查 cookies 是否存在
                }
                for user in users
            ]
        
        finally:
            session.close()
        

if __name__=="__main__":
    window = webview.create_window('批量操作窗口', url='templates/batchoperation.html', width=800, height=600,js_api=batchoperation_api())
    webview.start()