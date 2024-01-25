from toga import (Box, Window, Button, TextInput, ScrollContainer,
        Selection, Switch, ScrollContainer, DetailedList)
from toga.style import Pack


class CalendarWidget(Box):
    def __init__(self):
        super(CalendarWidget, self).__init__()
        '''
        scrollarea  -> box -> 15 bt
                    -> box -> 15 bt
        press bt -> load tasks
                    '''
        self.date = ''
        self.style = Pack(flex=2)
        self.main_box = Box(style=Pack(direction='column'))
        self.scr = ScrollContainer(style=Pack(flex=2))
        
        self.scr.content = self.main_box
        self.add(self.scr)
        self.add_bts()

    def add_bts(self):
        " add bts to calendar widget"
        self.box1 = Box()
        bt_titles1 = range(1, 16)
        self.box2 = Box()
        bt_titles2 = range(16, 31)
        for title in bt_titles1:
            bt = Button(text=title, style=Pack(width=40))
            bt.on_press = self.setdate
            self.box1.add(bt)
        for title in bt_titles2:
            bt = Button(text=title, style=Pack(width=40))
            bt.on_press = self.setdate
            self.box2.add(bt)
        self.main_box.add(self.box1)
        self.main_box.add(self.box2)

    def setdate(self, widget):
        "set date and new color by press date bt"
        self.reset_texts()
        self.date = widget.text
        widget.style.background_color = '#2fd100'

    def reset_texts(self):
        " change widget ssettings by press bt day"
        for bt in self.box1.children:
            if bt.style.background_color == '#2fd100':
                bt.style.background_color = '#ffffff'
        for bt in self.box2.children:
            if bt.style.background_color == '#2fd100':
                bt.style.background_color = '#ffffff'
