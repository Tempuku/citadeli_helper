from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.lang.builder import Builder

screen_helper = """
ScreenManager:
    MainScreen:

<MainScreen>:
    name: 'main'
    MDFloatingActionButton: 
        id: float_act_btn 
        icon: 'plus' 
        size_hint: None, None 
        size: dp(56), dp(56) 
        opposite_colors: True  # иконка белого/черного цветов 
        elevation_normal: 8  # длинна тени 
        pos_hint: {'center_x': .9, 'center_y': .1}  # самое нужное место на экране, которое кнопка обязательно закроет
        background_color: app.theme_cls.primary_color

"""


class MainScreen(Screen):
    """Главный экран приложения."""
    pass


sm = ScreenManager()
sm.add_widget(MainScreen(name="main"))


class CitadelsHelper(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen


if __name__ == "__main__":
    CitadelsHelper().run()
