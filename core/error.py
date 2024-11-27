import logging

logging.basicConfig(filename="app_errors.log",level=logging.ERROR)

class AutoErrorHandler:
    def __init__(self,max_retries=3) -> None:
        self.max_retries = max_retries

    def handle_error(self,func,*args,**kwargs):
        retries = 0
        while retries < self.max_retries:
            try:
                pass
            except Exception as e:
                retries += 1



