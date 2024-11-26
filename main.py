import threading,time
from core.Timer import Timer
from core.window.main_window import Main_Window
import webview



# threadList = []

# def createTimer():
#     t = Timer()
#     t.run_timer()

# timer_thread = threading.Thread(target=createTimer,name="Timer")
# timer_thread.start()
# timer_thread.join()

if __name__=="__main__":
    main_windows = webview.create_window(
                                        title='推特自动化',
                                        resizable=True,
                                        url="templates\index.html",
                                        width=922,
                                        height=730,
                                        frameless=False,
                                        js_api=Main_Window()
                                        )
    webview.start(debug=True)