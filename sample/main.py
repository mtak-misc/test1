from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.webview import WebView

class WebViewApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        webview = WebView(url='https://www.google.com/')
        layout.add_widget(webview)
        return layout

if __name__ == '__main__':
    WebViewApp().run()
