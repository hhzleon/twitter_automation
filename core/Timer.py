import time
# from core.database.User import User
import sys
sys.path.append('d:/code/twitterAuto')
from core.database.Task import Task
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

    def __init__(self) -> None:
        engine = create_engine('sqlite:///data.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_current_task(self):
        self.task_count = self.session.query(Task).filter(Task.status == '3').count()
        self.tasks_in_progress = self.session.query(Task).filter(Task.status == '1').all()
        return  self.task_count

    def run(self):
        n = 0
        while (n < 5):
            n = n + 1
            print('thread %s >>> %s' % (threading.current_thread().name, n))
            time.sleep(10)
    # 执行下一条任务
    def execute_next_task(self):
        print ("添加前",len(self.tasks_in_progress))
        task = threading.Thread(target=self.run)
        task.start()
        self.tasks_in_progress.append(task)
        # task.join()
        print ("添加后",len(self.tasks_in_progress))

    def clean_up_completed_tasks(self):
        self.tasks_in_progress = [task for task in self.tasks_in_progress if task.is_alive()]

    def run_timer(self):
        while True:
            self.clean_up_completed_tasks()
            if len(self.tasks_in_progress) < self.thread_count:
                self.execute_next_task()
            else:
                pass
            time.sleep(2)  # 约定2s执行一次定时器

if __name__=="__main__":
    timer = Timer()
    timer.run_timer()