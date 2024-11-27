from DrissionPage import Chromium,ChromiumOptions
import sys
from core.database.User import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.append('d:/code/twitterAuto')
import time
from core.TFA import getTwoFa
class TwitterAuto:
    user = None
    tab = None
    def __init__(self,user) -> None:
        self.user:User = user
        co = ChromiumOptions()
        co.incognito()
        co.auto_port()
        self.tab = Chromium(co).latest_tab
        # self.tab = Chromium(co).latest_tab
        # self.tab.reconnect()
        self.tab.set.cookies.clear()
        # 创建引擎
        engine = create_engine('sqlite:///data.db')
        # 创建Session类
        self.Session = sessionmaker(bind=engine)
    


    def ButtonListToButton(self,ButtonList,ButtonText):
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
        self.tab.set.cookies(
                {"auth_token": self.user.cookies,'domain': '.x.com'}
            )
        url = "https://x.com/settings/profile"
        self.tab.get(url=url)
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
        self.tab.ele('@data-testid=Profile_Save_Button').click()
        
        
    def changeUserToken(self,id,token):
        try:
            session = self.Session()
            user_to_update = session.query(User).filter_by(id=id).first()
            user_to_update.cookies = token
            session.commit()
            return True
        except:
            return False
        finally:
            session.close()






# if __name__=="__main__":
#     from core.database.User import User
#     user = User() 
#     user.cookies = "956abc63231363697563988eb3c09d12f732c18e"
#     TwitterAuto(user=user).modify_info()
