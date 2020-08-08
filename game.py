from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivymd.theming import ThemeManager, ThemableBehavior
from kivymd.uix.navigationdrawer import NavigationLayout
from kivymd.uix.list import OneLineListItem, MDList
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.label import MDLabel
from kivymd.icon_definitions import md_icons
from kivymd.uix.card import MDCardSwipe
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from citadels_helper import *

# Window.size = (900, 1600)

screen_helper = """
<PlayerInsert>
    id: player_dialog
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None

    MDTextField:
        id: player_name
        hint_text: "Name"


<SwipeToDeleteItem>:
    size_hint_y: None
    height: content.height

    MDCardSwipeLayerBox:
        padding: "8dp"
        
        MDIconButton:
            icon: "trash-can"
            pos_hint: {"center_y": .5}
            on_release: app.screen.ids.base.remove_item(root)

    MDCardSwipeFrontBox:

        OneLineListItem:
            id: content
            text: root.text
            _no_ripple_effect: True

<ItemDrawer>:
    theme_text_color: "Custom"
    on_release: self.parent.set_color_item(self)

    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color

<NavDrawer>:
    id: "content_drawer"
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "56dp", "56dp"
            source: "kivymd.png"

    MDLabel:
        text: "KivyMD library"
        font_style: "Button"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: "kivydevelopment@gmail.com"
        font_style: "Caption"
        size_hint_y: None
        height: self.texture_size[1]

    ScrollView:

        DrawerList:
            id: nav_list
            
            OneLineListItem:
                text: "Screen 1"
                on_press:
                    root.nav_drawer.set_state("close")
                    
<BaseScreen>:
    name: 'base'
    
    ScrollView:

        MDList:
            id: player_list

    MDFloatingActionButton: 
        id: float_act_btn 
        icon: 'plus' 
        size_hint: None, None 
        size: dp(56), dp(56) 
        opposite_colors: True  # иконка белого/черного цветов 
        elevation_normal: 8  # длинна тени 
        pos_hint: {'center_x': .9, 'center_y': .1}
        background_color: app.theme_cls.primary_color
        on_release: root.show_confirmation_dialog()

<StartScreen>:
    name: 'main'
    
    MDToolbar:
        id: action_bar
        background_color: app.theme_cls.primary_color
        title: app.title
        left_action_items: [['menu', lambda x: nav_drawer.toggle_nav_drawer()]]
        elevation: 10
        md_bg_color: app.theme_cls.primary_color
        pos_hint: {"top": 1}

    ScreenManager:
        id: manager
        size_hint_y: None
        height: root.height - action_bar.height
        
        BaseScreen:
            id: base
    
    MDNavigationDrawer:
        id: nav_drawer
    
        NavDrawer:
            nav_drawer: nav_drawer
"""

"""MDFloatingActionButton: 
        id: float_act_btn 
        icon: 'plus' 
        size_hint: None, None 
        size: dp(56), dp(56) 
        opposite_colors: True  # иконка белого/черного цветов 
        elevation_normal: 8  # длинна тени 
        pos_hint: {'center_x': .9, 'center_y': .1}
        background_color: app.theme_cls.primary_color
        on_release: root.navigation_draw"""


game = Citadels()


class StartScreen(NavigationLayout):
    """Главный экран приложения."""
    pass

    def navigation_draw(self):
        print("Navigation")


class NavDrawer(BoxLayout):
    nav_drawer = ObjectProperty()


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class ItemDrawer(OneLineListItem):
    icon = StringProperty()


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()


class PlayerInsert(BoxLayout):
    pass


class BaseScreen(Screen):
    dialog = None
    game = Citadels()

    # start_label = None
    #
    # def on_enter(self):
    #     self.start_label = MDLabel(text="Добавь персонажа", halign="center")
    #     self.add_widget(self.start_label)

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Player:",
                type="custom",
                id="dialog",
                auto_dismiss=False,
                content_cls=PlayerInsert(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=MDApp().theme_cls.primary_color,
                        on_release=lambda x: self.dialog_close()
                    ),
                    MDFlatButton(
                        text="OK", text_color=MDApp().theme_cls.primary_color,
                        on_release=lambda x: self.add_player()
                    ),
                ],
            )
        self.dialog.open()

    def dialog_close(self, *args):
        self.dialog.dismiss(force=True)

    def add_player(self):
        name = self.dialog.content_cls.ids.player_name.text
        self.dialog.content_cls.ids.player_name.text = ""
        game.add_player(name)
        self.ids.player_list.add_widget(
            SwipeToDeleteItem(text=name)
        )
        self.dialog_close()

    def remove_item(self, instance):
        self.ids.player_list.remove_widget(instance)


class CitadelsHelper(MDApp):
    title = "Citadels"

    def build(self):
        theme_cls = ThemeManager()
        theme_cls.primary_palette = 'BlueGray'
        Builder.load_string(screen_helper)
        self.screen = StartScreen()
        self.manager = self.screen.ids.manager
        return self.screen


if __name__ == "__main__":
    app = CitadelsHelper()
    app.run()
