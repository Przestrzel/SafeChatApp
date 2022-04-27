from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox


class Toolbox(GridLayout):

    def __init__(self, **kwargs):
        super(Toolbox, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 50
        self.row_default_height = 10

        self.add_widget(Label(text='EBC'))
        self.ebc = CheckBox(active=True)
        self.add_widget(self.ebc)
        self.ebc.bind(active=self.on_ebc_active)

        self.add_widget(Label(text='CBC'))
        self.cbc = CheckBox(active=False)
        self.add_widget(self.cbc)
        self.cbc.bind(active=self.on_cbc_active)

    def on_ebc_active(self, checkboxInstance, isActive):
        self.cbc.active = not isActive

    def on_cbc_active(self, checkboxInstance, isActive):
        self.ebc.active = not isActive