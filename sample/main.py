from kivy.app import App
from jnius import autoclass
from kivy.clock import Clock
from android.runnable import run_on_ui_thread
from kivy.uix.widget import Widget

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.kivy.android.PythonActivity').mActivity

@run_on_ui_thread
def create_webview(*args):
    webview = WebView(activity)
    webview.getSettings().setJavaScriptEnabled(True)
    wvc = WebViewClient();
    webview.setWebViewClient(wvc);
    activity.setContentView(webview)
    webview.loadUrl('http://127.0.0.1:8080')

class Wv(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
                self.__functionstable__ = {}
        Clock.schedule_once(create_webview, 0)

class ServiceApp(App):
    def build(self):
        return Wv()

# https://github.com/kivy/python-for-android/issues/1908


if __name__ == '__main__':    
    ServiceApp().run()
