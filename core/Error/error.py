import logging

logging.basicConfig(filename="app_errors.log",level=logging.ERROR)

class AutoErrorHandler:
    def __init__(self,max_retries=3) -> None:
        self.max_retries = max_retries

    def handle_error(self,func,*args,**kwargs):
        logging.error()
        # retries = 0
        # while retries < self.max_retries:
        #     try:
        #         pass
        #     except Exception as e:
                #TODO 需要在这里记录错误的网页截图、网页源码、程序错误行（位置）



