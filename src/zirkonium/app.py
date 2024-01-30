"""
My first application
"""
import json
import os

from toga import (App, Box, MainWindow, Table, Button, Label, ScrollContainer)
from toga.style import Pack
from zirkonium.widgets import CalendarWidget
from zirkonium.wins import AddTaskWindow, OkTaskWindow


class Zirkonium(App):

    def startup(self):
        """
        create a new database by json format
        """
        self.path = os.path.realpath(__file__)[:-6]
        self.date_active = None
        try:
            with open(self.path + 'bank.json', 'r') as file:
                json.load(file)
        except FileNotFoundError:
            with open(self.path + 'bank.json', 'w') as file:
                json.dump({}, file, indent=3)
        add_Task_bt = Button('افزودن', style=Pack(padding=(0, 5, 0, 5)), on_press=self.open_add_task_window)
        menubar = Box(style=Pack(padding=(0, 0, 0, 0)))

        arranger_task_bt = Button('رده بندی', on_press=self.arranger)
        menubar.add(add_Task_bt)
        menubar.add(arranger_task_bt)
        self.tasks_list = Table(headings=['علامت', 'عنوان', 'ارزش', 'وضعیت'], 
                                style=Pack(direction="column"),
                                multiple_select=True,
                                missing_value='',
                                on_select=self.open_oked_window)
        self.calendar = CalendarWidget(self.path)
        for bt in self.calendar.box1.children:
            bt.on_press = self.load_day_tasks
        for bt in self.calendar.box2.children:
            bt.on_press = self.load_day_tasks
        scr = ScrollContainer(style=Pack(height=500, padding=(5, 5, 5, 5)))

        scr.content = self.tasks_list

        main_box = Box(style=Pack(direction='column', alignment='center', padding=(5, 5, 5, 5)))
        main_box.add(self.calendar)
        main_box.add(menubar)
        main_box.add(scr)
        main_box.add(Label(os.path.realpath(__file__)[:-6]))

        self.main_window = MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()
        self.upload()

    def load_day_tasks(self, widget):
        self.calendar.setdate(widget)
        self.date_active = int(widget.text)
        self.upload_day(self.date_active)

    def arranger(self, widget):
        print('log: app > arranger')
        with open(self.path + 'bank.json', 'r') as f:
            bank = json.load(f)
        for it in bank:
            print(it)

    def add_task(self, widget):
        print('log: app > add bt')
        data = self.win.get()
        self.win.close()
        value = data[1] + data[2]
        item = [None, data[0], value, 'انتظار']
        self.tasks_list.data.append(item)
        # add task to database
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        item.append(int(data[3]))
        newbank[data[0]] = item
        with open(self.path + 'bank.json', 'w') as f:
            json.dump(newbank, f, indent=2)
        self.upload_day(self.date_active)
        self.calendar.set_status()

    def upload(self):
        print('log: app > upload')
        self.tasks_list.data.clear()
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        for itm in newbank:
            cd = newbank[itm]
            self.tasks_list.data.append(cd[0], cd[1], cd[2], cd[3])

    def upload_day(self, number):
        print('log: app > upload day')
        self.tasks_list.data.clear()
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        for itm in newbank:
            selected_itm = newbank[itm]
            if selected_itm[4] == number:
                self.tasks_list.data.append(selected_itm[0], selected_itm[1], selected_itm[2], selected_itm[3])

    def oked_task(self, widget):
        # change task to oked
        print('log: app > oked_task')
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        newbank[self.task_name][3] = 'انجام شده'
        with open(self.path + 'bank.json', 'w') as f:
            json.dump(newbank, f, indent=2)
        self.ok_win.close()
        self.upload_day(self.date_active)

    def delete_task(self, widget):
        # change task to oked
        print('log: app > delete_task')
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        newbank.pop(self.task_name)
        with open(self.path + 'bank.json', 'w') as f:
            json.dump(newbank, f, indent=2)
        self.ok_win.close()
        self.upload_day(self.date_active)
        self.calendar.set_status()

    def cancel_task(self, widget):
        # change task to oked
        print('log: app > cancel_task')
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        newbank[self.task_name][3] = 'لغو شده'
        with open(self.path + 'bank.json', 'w') as f:
            json.dump(newbank, f, indent=2)
        self.ok_win.close()
        self.upload_day(self.date_active)

    def close_task(self, widget):
        self.ok_win.close()

    def open_add_task_window(self, widget):
        print('log: app > open_add_task_window')
        self.date = int(self.calendar.date)
        self.win = AddTaskWindow(self.date)
        self.win.position = (self.main_window.size[0]/2, self.main_window.size[1]/2)
        self.win.ok_bt.on_press = self.add_task
        self.windows.add(self.win)
        self.win.show()

    def open_oked_window(self, widget, row):
        print('log: app > open_oked_window')
        self.ok_win = OkTaskWindow()
        self.task_name = row.__dict__['عنوان']
        self.active_row = row
        self.ok_win.position = (self.main_window.size[0]/2, self.main_window.size[1]/2)
        self.ok_win.oked_bt.on_press = self.oked_task
        self.ok_win.delete_bt.on_press = self.delete_task
        self.ok_win.cancel_bt.on_press = self.cancel_task
        self.ok_win.close_bt.on_press = self.close_task
        self.windows.add(self.ok_win)
        self.ok_win.show()


def main():
    return Zirkonium()
