from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from graphics.chat_button import ChatButton
from plyer import filechooser
from Crypto.Cipher import AES
from messages.message import Message
from utils.enums import MessageType


class Toolbox(GridLayout):

    def __init__(self, send_message, add_message, **kwargs):
        super(Toolbox, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 50
        self.row_default_height = 10
        self.send_message = send_message
        self.add_message = add_message

        self.add_widget(Label(text='ECB'))
        self.ecb = CheckBox(active=True)
        self.add_widget(self.ebc)
        self.ecb.bind(active=self.on_ebc_active)

        self.add_widget(Label(text='CBC'))
        self.cbc = CheckBox(active=False)
        self.add_widget(self.cbc)
        self.cbc.bind(active=self.on_cbc_active)
        self.button = ChatButton(self.file_selection, "Upload file")
        self.button.size_hint = (.3, .3)
        self.button.pos_hint = {'x': .3, 'y': .3}
        self.add_widget(self.button)

    def on_ebc_active(self, _, is_active):
        self.cbc.active = not is_active

    def on_cbc_active(self, _, is_active):
        self.ecb.active = not is_active

    def active_mode(self):
        if self.ecb.active:
            return AES.MODE_ECB
        else:
            return AES.MODE_CBC

    def file_selection(self, _):
        filechooser.open_file(on_selection=self.selected)

    def selected(self, selection):
        if selection:
            self.send_message(selection[0], is_text=False)
        self.add_message(Message(selection[0], True, message_type=MessageType.FILE))
