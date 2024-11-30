import sys
# sys.path.append(twitterAuto')
import webview
from core.database.User import User
from core.database.Task import Task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class batchoperation_api:
    Session = None 
    def __init__(self) -> None:
        engine = create_engine('sqlite:///data.db')
        self.Session = sessionmaker(bind=engine)

    def selectNicknames(self): # 选择昵称文件 一行一个
        file_types = ('Image Files (*.bmp;*.jpg;*.gif;*.png)', 'All files (*.*)')
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
        return text

    def selectSignatures(self): # 选择签名文件 一行一个
        file_types = ('Image Files (*.bmp;*.jpg;*.gif;*.png)', 'All files (*.*)')
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
        return text

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

    def insertTask(self, TaskDictData): # 插入任务的函数 
            #TODO 可以把任务改成由传入的的参数总结成任务列表，然后再一一插入
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
        

    if __name__=="__main__":
        print (1)
        
        