


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)  # 任务ID
    userid = Column(Integer)  # 用户ID
    status = Column(Integer)  # 状态     0成功   1进行中 2失败   3等待中
    task_type = Column(String)  # 任务类型  1登录   2修改信息   3暂无
    args = Column(String)  # 参数
    notes = Column(String)  # 备注





