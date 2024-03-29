from toga import (Box, Window, Button, TextInput, MultilineTextInput, NumberInput, Divider,
        Selection, Switch, Label, DetailedList)
from toga.style import Pack


class AddTaskWindow(Window):
    def __init__(self, date):
        """
        a window for get new task data from user
        """
        super(AddTaskWindow, self).__init__()
        print('date:',date)
        self.date = date
        self.on_close = self.close_handler
        self.title = "افزودن وظیفه جدید"
        self.size = (250, 170)
        self.box = Box(style=Pack(padding=(10, 10, 10, 10), direction='column'))
        self.task_name_te = TextInput(placeholder='عنوان وظیفه را وارد کنید', style=Pack())
        self.importancs_sw = Switch('اهمیت', style=Pack())
        self.urgency_sw = Switch('فوریت', style=Pack())
        self.date_sp = NumberInput()
        self.date_sp.value = date[1]
        self.ok_bt = Button('افزودن', style=Pack(padding_top=40))

        self.box.add(self.task_name_te)
        self.box.add(self.urgency_sw)
        self.box.add(self.importancs_sw)
        self.box.add(Box(children=[self.date_sp, Label("تاریخ", style=Pack(width=100))]))
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
        # return task name, ur = subvalues, important value, mounth name, number day
        return [self.task_name_te.value, ur, self.importancs_sw.value, self.date[0], self.date[1]]

    def close_handler(self, window, **kwargs):
        """
        close window
        """
        return True


class OkTaskWindow(Window):
    def __init__(self, day_number, active_month):
        super(OkTaskWindow, self).__init__()
        """
        A window to specify the result of a task
        """
        self.on_close = self.close_handler
        self.title = "تایین وضعیت"
        self.active_month = active_month
        self.size = (250, 180)
        self.box = Box(style=Pack(padding=(10, 10, 10, 10), direction='column'))
        self.title_label = Label('روز ' + str(day_number), style=Pack(text_align='center'))
        self.cancel_bt = Button('لغو', style=Pack(width=70, padding=(10, 10, 10, 10)))
        self.oked_bt = Button('انجام شده', style=Pack(width=70, padding=(10, 10, 10, 10)))
        self.delete_bt = Button('حذف', style=Pack(width=70, padding=(10, 10, 10, 10)))
        self.transfer_bt = Button('انتقال به روز:', style=Pack(padding=(10, 10, 10, 2)))
        self.month_select = NumberInput(min=1, max=12, style=Pack(padding=(10, 10, 10, 10)))
        self.day_select = NumberInput(value=1, style=Pack(padding=(10, 10, 10, 10)))
        self.day_select.min_value = 1
        if active_month < 7 and day_number == 30:
            day_number = 1
            self.day_select.max = 30
            self.day_select.value = 1
        elif active_month > 6 and day_number == 31:
            day_number = 1
            self.day_select.max = 31
            self.day_select.value = 1
        self.todey_day = day_number
        self.day_select.value = day_number + 1

        self.close_bt = Button('بستن پنجره', style=Pack(background_color='#fbc855', padding=(10, 10, 10, 10)))
        self.box.add(self.title_label)
        self.box.add(Box(children=[self.oked_bt, self.cancel_bt, self.delete_bt]))
        self.box.add(Divider())
        self.box.add(Box(children=[Label('روز:'), self.day_select]))
        self.box.add(Box(children=[Label('ماه:'), self.month_select]))
        self.box.add(self.transfer_bt)
        self.box.add(self.close_bt)
        self.content = self.box
    
    def get(self):
        return [self.todey_day, int(self.day_select.value), int(self.month_select.value)]

    def close_handler(self, window, **kwargs):
        print('close OkTaskWindow')
        return True


class Add_Act_Window(Window):
    def __init__(self, act_type):
        super(Add_Act_Window, self).__init__()
        """
        A window to specify the result of a task
        """
        self.on_close = self.close_handler
        self.title = "add year Window"
        self.size = (250, 180)
        self.box = Box(style=Pack(padding=(10, 10, 10, 10), direction='column'))
        self.title_in = TextInput(placeholder='عنوان فعالیت را وارد کنید')
        self.subtitle_in = MultilineTextInput(placeholder='توضیحات فعالیت را وارد کنید', style=Pack(padding_top=5))
        self.act_type = act_type
        self.ok_bt = Button('تایید', style=Pack(padding=(10, 10, 10, 10)))
        self.box.add(self.title_in)
        self.box.add(self.subtitle_in)
        self.box.add(self.ok_bt)
        self.content = self.box

    def get(self):
        return [self.title_in.value, self.subtitle_in.value, self.act_type]

    def close_handler(self, window, **kwargs):
        print('close OkTaskWindow')
        return True