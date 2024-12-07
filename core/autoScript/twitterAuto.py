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
logging.basicConfig(filename="app_errors.log",level=logging.INFO,encoding="utf-8")



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
            # print (i.html)
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
        # 检测是否需要输入电话号码和邮件地址
        if "输入你的电话号码或邮件地址" in self.tab.ele("@role=heading").html:
            self.tab.ele("@autocomplete=on").input(self.user.email)
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
        
        # 验证是否登录成功
        # self.checkRequestIsTrue()
        
        # 开始封包监听,来截取auth_token
        auth_token = False
        cookies_List = 0
        self.tab.listen.start('x.com/home')  # 开始监听，指定获取包含该文本的数据包
        for packet in self.tab.listen.steps():
            cookies_List = packet.request.cookies
            break
        for cookie in cookies_List:
            if (cookie['name']=="auth_token"):
                auth_token = cookie['value']
                break
        
        # 更新任务状态 
        user_id = self.user.id # 要修改的用户id
        if (auth_token):
            self.changeTaskStatus(0)
            return self.changeUserToken(user_id,auth_token)
        self.changeTaskStatus(2)


    # 定义修改信息函数
    def modify_info(self):

        try:
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
            if self.tab.ele("@@role=group@@tabindex=0"):
                self.tab.ele("@@role=group@@tabindex=0").run_js("this.remove();")
            if self.tab.ele("@data-testid=mask"):
                self.tab.ele("@data-testid=mask").run_js("this.remove();")
            if self.tab.ele("@data-testid=sheetDialog"):
                self.tab.ele("@data-testid=sheetDialog").run_js("this.remove();")
            self.tab.ele("@name=displayName").clear()
            self.tab.ele("@name=displayName").input(self.user.nickname)
            self.tab.ele("@name=description").clear()
            self.tab.ele("@name=description").input(self.user.signature)
            self.tab.ele('@aria-label=Add avatar photo').click.to_upload(r'%s' % (self.user.avatar_url))
            self.tab.ele('@data-testid=applyButton').click()
            # buttonList = self.tab.eles("@role=button")
            # print(buttonList)
            # self.ButtonListToButton(buttonList,"Apply").click()
            # self.tab.ele('@aria-label=Add banner photo').click.to_upload(r'D:\code\twitterAuto\img\PixPin_2024-11-23.png')
            # self.tab.ele('@data-testid=applyButton').click()
            #程序是否保存完成的检测，否则标记任务失败
            Profile_Save_Button = self.tab.ele('@data-testid=Profile_Save_Button')
            status = self.checkRequestIsTrue("api.x.com/1.1/account/update_profile.json",Profile_Save_Button)
            if (not status):  #数据发送失败
                # raise "数据发送失败"
                return self.changeTaskStatus(2)
                
            else:
            # 成功
                return self.changeTaskStatus(0)
        except Exception as e:
            logging.error("modify_info函数问题:",e)
            # return False
            return self.changeTaskStatus(2)
        
        
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
        """
        更改当前任务状态:
        0 - 完成
        1 - 进行中
        2 - 失败
        3 - 等待中
        """        
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
            # self.changeTaskStatus(2)
            self.tab.get_screenshot(path="loggin",name=f"err{Errtime}.jpg",full_page=True)
            self.tab.save(path="loggin",name=f"errPage{Errtime}.")
            return True
        


