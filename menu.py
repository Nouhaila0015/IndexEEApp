from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class MenuPopup(Popup):
    def __init__(self, interface_instance, **kwargs):
        super(MenuPopup, self).__init__(**kwargs)
        self.interface = interface_instance

        # Set the size_hint and size for the MenuPopup
        self.size_hint = (0.8, 0.8)  
        self.size = (400, 400)  

        layout = BoxLayout(orientation='vertical', spacing=5)

        title_bar = GridLayout(cols=2, size_hint=(1, None), height=40)
        title_bar.add_widget(Label(text='Menu', halign='center', valign='center', bold=True))

        close_button = Button(text='[b]X[/b]', markup=True, size_hint=(None, None), height=40, width=40)
        close_button.bind(on_release=self.dismiss)
        title_bar.add_widget(close_button)

        layout.add_widget(title_bar)

        menu_grid = GridLayout(cols=1, spacing=5, size_hint=(1, None))
        menu_grid.bind(minimum_height=menu_grid.setter('height'))


        option2_button = Button(text="Exporter data", size_hint_y=None, height=40)
        option2_button.bind(on_release=self.export)
        menu_grid.add_widget(option2_button)

        option3_button = Button(text="Importer fichier", size_hint_y=None, height=40)
        option3_button.bind(on_release=self.open_file_chooser)
        menu_grid.add_widget(option3_button)

        menu_scroll = ScrollView(size_hint=(1, 1))
        menu_scroll.add_widget(menu_grid)
        layout.add_widget(menu_scroll)

        self.title = ''  # Empty title to hide default title bar
        self.content = layout

    # def on_recherche(self, instance):
    #     self.interface.on_recherche()

    def export(self, instance):
        self.interface.export_data_to_file()
        self.dismiss()

    def open_file_chooser(self, instance):
        self.interface.open_file_chooser()
