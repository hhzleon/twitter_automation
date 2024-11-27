from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    # 定义用户表
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)  # 用户ID
    username = Column(String)  # 用户名
    password = Column(String)  # 密码
    twoFa = Column(Integer)  # 双因素认证
    twoFaKey = Column(String)  # 双因素认证密钥
    cookies = Column(String)  # Cookies
    nickname = Column(String)  # 昵称
    signature = Column(String)  # 签名
    avatar_url = Column(String)  # 头像链接
    background_url = Column(String)  # 背景图片链接