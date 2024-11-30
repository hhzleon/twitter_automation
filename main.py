import threading
from core.Timer import Timer
from core.window.main_window import Main_Window
import webview

threadList = []

def createTimer():
    global t
    t = Timer()
    t.run_timer()

def closeWindowsEvent():
    global t
    t.stop()
    


if __name__=="__main__":
    window = Main_Window()
    main_windows = webview.create_window(
                                        title='x自动化',
                                        resizable=True,
                                        url="templates/index.html",
                                        width=922,
                                        height=730,
                                        frameless=False,
                                        js_api=window,easy_drag=True
                                        )
    timer_thread = threading.Thread(target=createTimer,name="Timer")
    timer_thread.start()
    main_windows.events.closing += closeWindowsEvent
    webview.start(debug=False)