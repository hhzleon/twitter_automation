import time
import sys
sys.path.append('d:/code/twitterAuto')
from core.database.Task import Task
from core.database.User import User
from core.autoScript.twitterAuto import TwitterAuto
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import threading

class Timer:
    # 变量定义
    # 定义任务数量
    task_count = 10
    # 定义线程数量
    thread_count = 4
    # 正在进行的任务列表
    tasks_in_progress = []
    # 数据库session
    session = None

    is_running = True

    def __init__(self) -> None:
        engine = create_engine('sqlite:///data.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_current_task(self):
        # 获取任务信息
        
        task = self.session.query(Task).filter_by(status=3).first()
        if not task:
            return False
        # 获取关联用户
        user = self.session.query(User).filter_by(id=task.userid).first()
        if not user:
            return False
        
        task.status = 1
        self.session.commit()
        # 解析任务参数
        # 返回信息
        return {"task":task,"task_type":task.task_type,"task_user":user,"task_args":task.args}
    def run(self):
        task_info = self.get_current_task() # 获取任务信息
        if (task_info==False):
            return False
        if (task_info['task_type']=="login"):
            oTwitterAuto = TwitterAuto(user=task_info['task_user'],task=task_info['task'])
            oTwitterAuto.error_handler(oTwitterAuto.login())

        elif(task_info['task_type']=="modify_info"):    # 修改信息任务
            oTwitterAuto = TwitterAuto(user=task_info['task_user'],task=task_info['task'])
            oTwitterAuto.error_handler(oTwitterAuto.modify_info())
            
    # 执行下一条任务
    def execute_next_task(self):
        task = threading.Thread(target=self.run)
        task.start()
        # print("正在执行任务")
        self.tasks_in_progress.append(task)

    def clean_up_completed_tasks(self):
        self.tasks_in_progress = [task for task in self.tasks_in_progress if task.is_alive()]

    def run_timer(self):
        while self.is_running:
            self.clean_up_completed_tasks() # 删除队列中已失活的任务
            if len(self.tasks_in_progress) < self.thread_count: # 如果队列的长度小于最大线程
                self.execute_next_task() # 执行搜索执行下一条任务
            else:
                pass
            time.sleep(2)  # 约定2s执行一次定时器

    def stop(self):
        self.is_running = False


            



if __name__=="__main__":
    timer = Timer()
    timer.run_timer()