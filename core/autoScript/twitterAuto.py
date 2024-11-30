from DrissionPage import Chromium,ChromiumOptions
from core.database.User import User
from core.database.Task import Task
from core.TFA import getTwoFa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time

import sys
sys.path.append('d:/code/twitterAuto')
import logging
logging.basicConfig(filename="app_errors.log",level=logging.ERROR,encoding="utf-8")



class TwitterAuto:
    user = None
    tab = None
    def __init__(self,user,task) -> None:
        self.user:User = user
        self.task:Task = task
        co = ChromiumOptions()
        co.incognito()
        co.auto_port()
        self.tab = Chromium(co).latest_tab
        self.tab.set.cookies.clear()
        # 创建引擎
        engine = create_engine('sqlite:///data.db')
        # 创建Session类
        self.Session = sessionmaker(bind=engine)
    
    def ButtonListToButton(self,ButtonList,ButtonText):
        # 传入Button列表，然后还有要找的Button文本，随后会查找列表内是否有文本在。
        for i in ButtonList:
            if (ButtonText in i.html):
                return i
    # 定义登录函数
    # 返回cookies:str
    def login(self):
        url = "https://x.com/i/flow/login"
        self.tab.get(url=url)
        self.tab.ele("@autocomplete=username").input(self.user.username)
        buttonList = self.tab.eles("@role=button")
        self.ButtonListToButton(buttonList,"下一步").click()
        # 输入密码
        self.tab.ele("@autocomplete=current-password").input(self.user.password)
        buttonList = self.tab.eles("@role=button")
        self.ButtonListToButton(buttonList,"登录").click()
        TwoFACode = getTwoFa(self.user.twoFaKey)
        self.tab.ele("@inputmode=numeric").input(TwoFACode)
        buttonList = self.tab.eles("@role=button")
        self.ButtonListToButton(buttonList,"下一步").click()
        cookies = self.tab.cookies().as_dict()
        auth_token = cookies['auth_token']  # 这里可能会出现异常，记录未登录完成的账户取不到auth_token
        user_id = self.user.id # 要修改的用户id
        return self.changeUserToken(user_id,auth_token)



    # 定义修改信息函数
    def modify_info(self):
        if self.user.cookies:
            self.tab.set.cookies(
                    {"auth_token": self.user.cookies,'domain': '.x.com'}
                )
        else:
            # 1. 标记任务失败
            self.changeTaskStatus(2)
            # 2. 插入新的任务
            self.insertTask_Login()
            raise Exception("无cookies可以使用")
        url = "https://x.com/settings/profile"
        self.tab.get(url=url)
        if ("登录" in self.tab.title):
            # 1. 标记任务失败
            self.changeTaskStatus(2)
            # 2. 插入新的任务
            self.insertTask_Login()
            raise Exception("cookies失效")
        
        if self.tab.ele("@data-testid=sheetDialog"):
            self.tab.ele("@data-testid=sheetDialog").run_js("this.remove();")
        self.tab.ele("@name=displayName").clear()
        self.tab.ele("@name=displayName").input(self.user.nickname)
        self.tab.ele("@name=description").clear()
        self.tab.ele("@name=description").input(self.user.signature)
        self.tab.ele('@aria-label=Add avatar photo').click.to_upload(r'%s' % (self.user.avatar_url))
        self.tab.ele('@data-testid=applyButton').click()
        # self.tab.ele('@aria-label=Add banner photo').click.to_upload(r'D:\code\twitterAuto\img\PixPin_2024-11-23.png')
        # self.tab.ele('@data-testid=applyButton').click()
        #TODO 需要在这里添加一个程序是否保存完成的检测，否则标记任务失败
        Profile_Save_Button = self.tab.ele('@data-testid=Profile_Save_Button')
        status = self.checkRequestIsTrue("api.x.com/1.1/account/update_profile.json",Profile_Save_Button)
        if (not status):  #数据发送失败
            self.changeTaskStatus(2)
            return False
        else:
        # 成功
            self.changeTaskStatus(0)
            return True
        
        
    def changeUserToken(self,id,token):
        try:
            session = self.Session()
            user_to_update = session.query(User).filter_by(id=id).first()
            user_to_update.cookies = token
            session.commit()
            return True
        except:
            session.rollback()
            return False
        finally:
            session.close()

    def changeTaskStatus(self,status):
        try:
            session = self.Session()
            task_to_update = session.query(Task).filter_by(id=self.task.id).first()
            task_to_update.status = status
            session.commit()
            return True
        except:
            session.rollback()
            return False
        finally:
            session.close()

    def insertTask_Login(self):
        session = self.Session()
        try:
            new_task = Task(
                userid=self.user.id,
                status=3,
                task_type="login",
                args=None,
                notes="账户无Cookies，修改名称失败"
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

    def checkRequestIsTrue(self,url,button):
        # raise Exception("检测封包时发生错误")
        """
        如果数据为发送成功，返回True，否则返回False
        """
        self.tab.listen.start(url) # 开启监听 # https://api.x.com/1.1/account/update_profile.json
        button.click()
        for packet in self.tab.listen.steps():
            if (packet.is_failed == False):
                self.tab.listen.stop()
                return True
            self.tab.listen.stop()
            return False
        
    

    def error_handler(self,func, *args, **kwargs):
        try:
            return func(*args, **kwargs)  # 执行传入的函数
        except Exception as e:
            Errtime = time.time()
            logging.info(f"Errtime: {Errtime} ErrUser: {self.user.id} ErrTask: {self.task.id}")
            logging.exception (f"错误发生在{func.__name__}:{e}")
            self.tab.get_screenshot(path="loggin",name=f"err{Errtime}.jpg",full_page=True)
            self.tab.save(path="loggin",name=f"errPage{Errtime}.")
            return True
        


