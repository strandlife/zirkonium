from toga import (Box, Window, Button, TextInput, NumberInput,
        Selection, Switch, ScrollContainer, DetailedList)
from toga.style import Pack


class AddTaskWindow(Window):
    def __init__(self, date):
        """
        a window for get new task data from user
        """
        super(AddTaskWindow, self).__init__()
        self.on_close = self.close_handler
        self.title = "افزودن وظیفه جدید"
        self.size = (250, 170)
        self.box = Box(style=Pack(padding=(10, 10, 10, 10), direction='column'))
        self.task_name_te = TextInput(style=Pack())
        self.importancs_sw = Switch('اهمیت', style=Pack())
        self.urgency_sw = Switch('فوریت', style=Pack())
        self.date_sp = NumberInput()
        self.date_sp.value = date
        self.ok_bt = Button('افزودن', style=Pack(padding_top=40))

        self.box.add(self.task_name_te)
        self.box.add(self.urgency_sw)
        self.box.add(self.importancs_sw)
        self.box.add(self.date_sp)
        self.box.add(self.ok_bt)
        self.content = self.box

    def get(self):
        print('log: wins > AddTaskWindow.get')
        """
        return intered user data for add task"""
        if self.urgency_sw.value == 1:
            ur = 2
        else:
            ur = 0
        return [self.task_name_te.value, ur, self.importancs_sw.value, self.date_sp.value]

    def close_handler(self, window, **kwargs):
        """
        close window
        """
        return True


class OkTaskWindow(Window):
    def __init__(self):
        super(OkTaskWindow, self).__init__()
        """
        A window to specify the result of a task
        """
        self.on_close = self.close_handler
        self.title = "Ok Task Window"
        self.size = (250, 180)
        self.box = Box(style=Pack(padding=(10, 10, 10, 10), direction='column'))
        self.cancel_bt = Button('لغو', style=Pack(padding=(10, 10, 10, 10)))
        self.oked_bt = Button('انجام شده', style=Pack(padding=(10, 10, 10, 10)))
        self.delete_bt = Button('حذف', style=Pack(padding=(10, 10, 10, 10)))
        self.close_bt = Button('بستن پنجره', style=Pack(padding=(10, 10, 10, 10)))
        self.box.add(self.oked_bt)
        self.box.add(self.cancel_bt)
        self.box.add(self.delete_bt)
        self.box.add(self.close_bt)
        self.content = self.box

    def close_handler(self, window, **kwargs):
        return True
