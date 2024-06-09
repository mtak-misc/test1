from kivy.app import App
from jnius import autoclass
from kivy.clock import Clock
from android.runnable import run_on_ui_thread
from kivy.uix.widget import Widget
import gradio as gr
from fastapi import FastAPI
import uvicorn
from threading import Thread

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.kivy.android.PythonActivity').mActivity

async def generate_text(message, history):
    temp = ""
    temp += 'Echo: ' + message
    yield temp 

def gradio_worker(app):
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")

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
        demo = gr.ChatInterface(
            fn=generate_text,
            title="Gradio Sample",
            cache_examples=False,
            retry_btn=None,
            undo_btn="Remove last",
            clear_btn="Clear all",
        )

        app = FastAPI()
        app = gr.mount_gradio_app(app, demo, path='/')

        thread = Thread(target=gradio_worker, args=(app,))
        thread.daemon = True
        thread.start()
        
        self.__functionstable__ = {}
        Clock.schedule_once(create_webview, 0)

class ServiceApp(App):
    def build(self):
        return Wv()

# https://github.com/kivy/python-for-android/issues/1908


if __name__ == '__main__':    
    ServiceApp().run()
