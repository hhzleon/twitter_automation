import sys
sys.path.append('d:/code/twitterAuto')
import webview
from core.database.User import User
from core.database.Task import Task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.window.batchoperation_window import batchoperation_api
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
    def selectFilePath(self):
        file_types = ('Image Files (*.bmp;*.jpg;*.gif;*.png)', 'All files (*.*)')
        w = webview.create_window("Hello",width=1,height=1,frameless=True)
        w.hide()
        result = w.create_file_dialog(
            webview.OPEN_DIALOG, allow_multiple=True, file_types=file_types
        )
        w.destroy()
        return result[0]

        # webview.start(w)

    # 获取任务列表
    def getTaskList(self):
        session = self.Session()
        try:
            tasks = session.query(Task).order_by(Task.id.desc()).all()
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

    def executeBatchOperation(self, userIds):
        session = self.Session()
        try:
            if userIds:
                # 打开批量操作界面并传入用户ID
                batch_api = batchoperation_api(userIds)
                batch_api.Session = self.Session
                window = webview.create_window('批量操作窗口', url='templates/batchoperation.html', js_api=batch_api, width=800, height=700, resizable=True)
                # 传入用户数据
                webview.start(debug=True)
            else:
                print("No users selected for batch operation.")

        except Exception as e:
            print("Batch operation failed:", e)
        finally:
            session.close()

    def importUsers(self):
        #TODO 这个函数未测试,需要重写
        session = self.Session()
        try:
            # 打开用户文件并读取内容
            file_types = ('Text Files (*.txt)', 'All files (*.*)')
            w = webview.create_window("选择用户文件", width=1, height=1, frameless=True)
            w.hide()
            result = w.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
            # webview.start()
            w.destroy()
            
            if result:
                file_path = result[0]
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for line in lines:
                    # 根据文件格式假设: username, password, 2fa, ......, cookies
                    parts = line.strip().split('~~~~')
                    if len(parts) >= 7:
                        username = parts[0]
                        password = parts[1]
                        twofa = parts[2]
                        # 假设我们还需要 id, status, avatar_url 基本信息以进行处理
                        cookies = parts[6]
                        email = parts[7]

                        # 创建新的用户对象
                        new_user = User(
                            username=username,
                            password=password,
                            twoFaKey=twofa,
                            cookies=cookies,
                            email=email
                        )
                        # 添加到会话
                        session.add(new_user)
                # 提交会话
                session.commit()
                print("用户导入成功")
            else:
                print("未选择任何文件")
        except FileNotFoundError:
            print("文件未找到，请检查文件路径")
        except Exception as e:
            print("导入用户时发生错误:", e)
            session.rollback()
        finally:
            session.close()

    def deleteUserById(self, user_id):
        """
        根据用户ID删除用户
        """
        session = self.Session()
        try:
            # 查询需要删除的用户
            user_to_delete = session.query(User).filter_by(id=user_id).first()
            if user_to_delete:
                # 删除用户
                session.delete(user_to_delete)
                session.commit()
                print("删除用户成功")
                return {'success': True}
            else:
                print("未找到该用户")
                return {'success': False, 'error': 'User not found'}
        except Exception as e:
            print("删除用户时发生错误:", e)
            session.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            session.close()
