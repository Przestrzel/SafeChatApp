from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from graphics.chat_button import ChatButton
from plyer import filechooser


class Toolbox(GridLayout):

    def __init__(self, send_message, **kwargs):
        super(Toolbox, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 50
        self.row_default_height = 10
        self.send_message = send_message

        self.add_widget(Label(text='EBC'))
        self.ebc = CheckBox(active=True)
        self.add_widget(self.ebc)
        self.ebc.bind(active=self.on_ebc_active)

        self.add_widget(Label(text='CBC'))
        self.cbc = CheckBox(active=False)
        self.add_widget(self.cbc)
        self.cbc.bind(active=self.on_cbc_active)
        self.button = ChatButton(self.file_selection, "Upload file")
        self.add_widget(self.button)

    def on_ebc_active(self, _, is_active):
        self.cbc.active = not is_active

    def on_cbc_active(self, _, is_active):
        self.ebc.active = not is_active

    def file_selection(self, _):
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        self.send_message(selection[0], is_text=False)
