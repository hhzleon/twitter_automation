from DrissionPage import Chromium,ChromiumOptions
import sys
sys.path.append('d:/code/twitterAuto')
import time
from core.TFA import getTwoFa
class TwitterAuto:
    user = None
    tab = None
    # def __init__(self) -> None:
    def __init__(self,user) -> None:
        self.user = user
        co = ChromiumOptions()
        co.incognito()
        co.auto_port()
        self.tab = Chromium(co).latest_tab
        # self.tab = Chromium(co).latest_tab
        # self.tab.reconnect()
        self.tab.set.cookies.clear()
    


    def ButtonListToButton(self,ButtonList,ButtonText):
        for i in ButtonList:
            if (ButtonText in i.html):
                return i
    # 定义登录函数
    # 返回cookies:str
    def login(self):
        
        url = "https://x.com/i/flow/login"

        self.tab.get(url=url)
        self.tab.ele("@autocomplete=username").input("UenM7d9eZwWOS")
        buttonList = self.tab.eles("@role=button")
        self.ButtonListToButton(buttonList,"下一步").click()
        # 输入密码
        self.tab.ele("@autocomplete=current-password").input("m88PpJdXOu")
        buttonList = self.tab.eles("@role=button")
        self.ButtonListToButton(buttonList,"登录").click()
        TwoFACode = getTwoFa("JPRNHKIUQZ6Z4HXG")
        self.tab.ele("@inputmode=numeric").input(TwoFACode)
        buttonList = self.tab.eles("@role=button")
        self.ButtonListToButton(buttonList,"下一步").click()
        
        cookies = self.tab.cookies().as_str()
        with open("cookies","w") as f:
            f.write(cookies)
            f.close()



    # 定义修改信息函数
    def modify_info(self):
        self.tab.set.cookies(
                {"auth_token": self.user.cookies,'domain': '.x.com'}
            )
        url = "https://x.com/settings/profile"
        self.tab.get(url=url)
        if self.tab.ele("@data-testid=sheetDialog"):
            self.tab.ele("@data-testid=sheetDialog").run_js("this.remove();")
        self.tab.ele("@name=displayName").input("测试名称")
        self.tab.ele("@name=description").input("测试个性签名")
        self.tab.ele('@aria-label=Add avatar photo').click.to_upload(r'D:\code\twitterAuto\img\PixPin_2024-11-23.png')
        self.tab.ele('@data-testid=applyButton').click()
        self.tab.ele('@aria-label=Add banner photo').click.to_upload(r'D:\code\twitterAuto\img\PixPin_2024-11-23.png')
        self.tab.ele('@data-testid=applyButton').click()
        self.tab.ele('@data-testid=Profile_Save_Button').click()
        
        





if __name__=="__main__":
    from core.database.User import User
    user = User() 
    user.cookies = "956abc63231363697563988eb3c09d12f732c18e"
    TwitterAuto(user=user).modify_info()
