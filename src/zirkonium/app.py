"""
My first application
"""
import json
import os

from toga import (App, Box, MainWindow, Table, Button, Label, OptionContainer, DetailedList, ScrollContainer)
from toga.style import Pack
from zirkonium.widgets import CalendarWidget
from zirkonium.wins import AddTaskWindow, OkTaskWindow, AddYearWindow, Add_Act_Window


class Zirkonium(App):

    def startup(self):
        """
        create a new database by json format
        """
        self.path = os.path.realpath(__file__)[:-6]
        self.date_active = None
        self.mounth_active = 1
        self.tabs = OptionContainer(on_select=self.select_tab)
        # daily
        self.add_Task_bt = Button('افزودن', style=Pack(padding=(0, 5, 0, 5)), on_press=self.open_add_task_window)
        self.add_Task_bt.enabled = False
        self.show_all_tasks = Button('نمایش همه', on_press=self.upload)
        self.menubar = Box(style=Pack(padding=(0, 0, 0, 0)))
        arranger_task_bt = Button('رده بندی', on_press=self.arranger)
        self.menubar.add(self.add_Task_bt)
        # self.menubar.add(arranger_task_bt)
        self.menubar.add(self.show_all_tasks)
        self.tasks_list = Table(headings=['عنوان', 'ارزش', 'وضعیت', "فرصت"],
                                style=Pack(direction="column"),
                                multiple_select=False,
                                missing_value='')
        self.tasks_list._on_activate = self.open_oked_window
        # gilding
        self.gilding_list = DetailedList(on_select=self.select_act)
        self.add_forbidden_act_bt = Button('حرام', on_press=self.add_forbidden_act_window)
        self.add_abominable_act_bt = Button('مکروه', on_press=self.add_abominable_act_window)
        self.del_act_bt = Button('حذف', on_press=self.delete_act)
        self.gilding_menubat = Box()
        self.gilding_menubat.add(self.add_forbidden_act_bt)
        self.gilding_menubat.add(self.add_abominable_act_bt)
        self.gilding_menubat.add(self.del_act_bt)
        # calendar
        self.calendar = CalendarWidget(self.path, self.mounth_active)
        self.calendar.next_mounth_bt.on_press = self.next_mounth
        self.calendar.prev_mounth_bt.on_press = self.prev_mounth
        try:
            with open(self.path + 'year.json', 'r') as file:
                json.load(file)
            self.set_func_for_cal_bts()
            self.show()
        except FileNotFoundError:
            self.create_and_upload_calendar()

    def create_and_upload_calendar(self):
        print('log: app  > upload calendar')
        self.one_day_win = AddYearWindow()
        self.one_day_win.ok_bt.on_press = self.make_year
        self.windows.add(self.one_day_win)
        self.one_day_win.show()

    def set_func_for_cal_bts(self):
        print('log: app  > set func for calendar bts')
        for bt in self.calendar.box1.children:
            bt.on_press = self.load_day
        for bt in self.calendar.box2.children:
            bt.on_press = self.load_day
        for bt in self.calendar.box3.children:
            bt.on_press = self.load_day
        for bt in self.calendar.box4.children:
            bt.on_press = self.load_day
        for bt in self.calendar.box5.children:
            bt.on_press = self.load_day
        for bt in self.calendar.box6.children:
            bt.on_press = self.load_day
        # clear task table
        for itm in list(self.tasks_list.data):
            self.tasks_list.data.remove(itm)

    def make_year(self, widget):
        print('log: app  > make_year')
        with open(self.path + 'year.json', 'w') as file:
            json.dump({}, file, indent=3)
        # Determine the first day of the week for the current year
        self.calendar.set_one_day(self.one_day_win.set_one_day())
        # Building the current year database
        self.calendar.make_year()
        # Add calendar days buttons for a year
        self.calendar.add_bts()
        # Creating a task database
        if self.calendar.one_day != None:
            try:
                with open(self.path + 'bank.json', 'r') as file:
                    json.load(file)
            except FileNotFoundError:
                with open(self.path + 'bank.json', 'w') as file:
                    json.dump({}, file, indent=3)
                with open(self.path + 'gilding.json', 'w') as file:
                    json.dump({}, file, indent=3)
            self.one_day_win.close()
            # Assign tasks to calendar buttons
            self.set_func_for_cal_bts()
            # Display the main window of the program
            self.show()

    def next_mounth(self, widget):
        print('log: app  > calendar.next_mounth')
        current_index = self.calendar.active_mounth - 1
        self.calendar.active_mounth = list(self.calendar.mounths_list.keys())[current_index + 1]
        self.calendar.info_lb.text = self.calendar.mounths_list[self.calendar.active_mounth] + '1390'
        self.calendar.add_bts()
        self.set_func_for_cal_bts()
        self.calendar.day_selected = None
        self.calendar.set_status_daily()

    def prev_mounth(self, widget):
        print('log: app  > calendar.prev_mounth')
        current_index = self.calendar.active_mounth - 1
        self.calendar.active_mounth = list(self.calendar.mounths_list.keys())[current_index - 1]
        self.calendar.info_lb.text = self.calendar.mounths_list[self.calendar.active_mounth] + '1390'
        self.calendar.add_bts()
        self.set_func_for_cal_bts()
        self.calendar.day_selected = None
        self.calendar.set_status_daily()

    def show(self):
        print('log: app  > show main_window')
        scr = ScrollContainer(style=Pack(height=500, padding=(5, 5, 5, 5)))
        scr.content = self.tasks_list
        main_box = Box(style=Pack(direction='column', alignment='center', padding=(5, 5, 5, 5)))
        main_box.add(self.calendar)
        daily_box = Box(style=Pack(direction='column'))
        daily_box.add(self.menubar)
        daily_box.add(scr)
        # daily_box.add(Label(os.path.realpath(__file__)[:-6]))
        gilding_box = Box(style=Pack(direction='column'))
        gilding_scr = ScrollContainer(style=Pack(height=500, padding=(5, 5, 5, 5)))
        gilding_scr.content = self.gilding_list
        gilding_box.add(self.gilding_menubat)
        gilding_box.add(gilding_scr)
        self.tabs.content.insert(0, 'روزانه', daily_box)
        self.tabs.content.insert(1, 'تذهیب', gilding_box)
        main_box.add(self.tabs)
        self.main_window = MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def load_day(self, widget):
        print('log: app  > load day tasks by press bt:', widget.text)
        self.add_Task_bt.enabled = True
        if self.tabs.current_tab.index == 0:
            self.calendar.setdate_task(widget)
        elif self.tabs.current_tab.index == 1:
            self.calendar.setdate_gilding(widget)
        self.date_active = int(widget.text)
        if self.tabs.current_tab.index == 0:
            self.upload_day_tasks(self.date_active)
        elif self.tabs.current_tab.index == 1:
            self.upload_day_acts(self.date_active)

    def arranger(self, widget):
        print('log: app > arranger')
        with open(self.path + 'bank.json', 'r') as f:
            bank = json.load(f)

    def add_task(self, widget):
        print('log: app  > add task')
        data = self.win.get()
        self.win.close()
        value = data[1] + data[2]
        # item = [icon, task name, value, statuse]
        item = {'taskname': data[0], 'sub': value, 'mounth': data[3], 'statuse': 'انتظار'}
        self.tasks_list.data.append(item)
        # add task to database
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        # add day number to item
        item['day'] = data[4]
        # add item to database
        newbank[data[0]] = item
        # save database
        with open(self.path + 'bank.json', 'w') as f:
            json.dump(newbank, f, indent=2)
        self.upload_day_tasks(self.date_active)
        self.calendar.set_status_daily()

    def upload(self, widget):
        print('log: app  > upload all tasks')
        self.tasks_list.data.clear()
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        for itm in newbank:
            cd = newbank[itm]
            deedline = self.calendar.today_date_day - int(cd['day'])
            if deedline > 0:
                deedline = 'منقضی'
            elif deedline == 0:
                deedline = 'امروز'
            self.tasks_list.data.append((cd['taskname'], cd['sub'], cd['statuse'], deedline))

    def upload_day_tasks(self, date):
        print('log: app  > upload day tasks', date)
        for itm in list(self.tasks_list.data):
            self.tasks_list.data.remove(itm)
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        for itm in newbank:
            selected_itm = newbank[itm]
            if int(selected_itm['day']) == date and  int(selected_itm['mounth']) == self.calendar.active_mounth:
                deedline = self.calendar.today_date_day - int(selected_itm['day'])
                self.mounth_active = self.calendar.today_month
                if deedline > 0:
                    deedline = 'منقضی'
                elif deedline == 0:
                    deedline = 'امروز'
                self.tasks_list.data.append((selected_itm['taskname'], selected_itm['sub'], selected_itm['statuse'], deedline))
        self.calendar.set_status_daily()

    def upload_day_acts(self, date):
        print('log: app  > load day acts')
        '''upload gilding.json to gilding_list'''
        for act in list(self.gilding_list.data):
            self.gilding_list.data.remove(act)
        with open(self.path + 'gilding.json', 'r') as f:
            data = json.load(f)
        for itm in data:
            if data[itm][1] == date and data[itm][2] == self.calendar.active_mounth:
                self.gilding_list.data.append(itm)

    def oked_task(self, widget):
        # change task to oked
        print('log: app  > oked_task')
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        newbank[self.task_name]['statuse'] = 'انجام شده'
        with open(self.path + 'bank.json', 'w') as f:
            json.dump(newbank, f, indent=2)
        self.ok_win.close()
        self.upload_day(self.date_active)

    def delete_task(self, widget):
        # change task to oked
        print('log: app  > delete_task')
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        newbank.pop(self.task_name)
        with open(self.path + 'bank.json', 'w') as f:
            json.dump(newbank, f, indent=2)
        self.ok_win.close()
        self.upload_day_tasks(self.date_active)
        self.calendar.set_status_daily()


    def cancel_task(self, widget):
        # change task to oked
        print('log: app > cancel_task')
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        newbank[self.task_name]['statuse'] = 'لغو شده'
        with open(self.path + 'bank.json', 'w') as f:
            json.dump(newbank, f, indent=2)
        self.ok_win.close()
        self.upload_day(self.date_active)

    def transfer_task(self, widget):
        with open(self.path + 'bank.json', 'r') as f:
            newbank = json.load(f)
        todey_day_name = ''
        for day_name in newbank:
            print('day=',day_name)
            if newbank[day_name]['day'] == self.ok_win.get()[0]:
                todey_day_name = day_name
                todey_day = newbank[day_name]
        newbank.pop(todey_day_name)
        new_day = self.ok_win.get()
        print(new_day)
        newbank[todey_day['taskname']] = {'taskname':todey_day['taskname'], 'sub':todey_day['sub'],
                                    'mounth':new_day[2], 'day':new_day[1], 'statuse':'انتظار'}
        # save to database
        with open(self.path + 'bank.json', 'w') as f:
            json.dump(newbank, f, indent=2)
        self.ok_win.close()
        # update calendar and tasks table 
        self.upload_day(self.date_active)

    def close_task(self, widget):
        self.ok_win.close()

    def open_add_task_window(self, widget):
        print('log: app  > open_add_task_window')
        self.date = self.calendar.date
        self.win = AddTaskWindow(self.date)
        self.win.position = (self.main_window.size[0]/2, self.main_window.size[1]/2)
        self.win.ok_bt.on_press = self.add_task
        self.windows.add(self.win)
        self.win.show()

    def open_oked_window(self, row):
        print('log: app > open_oked_window')
        self.ok_win = OkTaskWindow(self.date_active, self.mounth_active)
        self.task_name = row.__dict__['عنوان']
        self.active_row = row
        self.ok_win.position = (self.main_window.size[0]/2, self.main_window.size[1]/2)
        self.ok_win.oked_bt.on_press = self.oked_task
        self.ok_win.delete_bt.on_press = self.delete_task
        self.ok_win.cancel_bt.on_press = self.cancel_task
        self.ok_win.transfer_bt.on_press = self.transfer_task
        self.ok_win.close_bt.on_press = self.close_task
        self.windows.add(self.ok_win)
        self.ok_win.show()

    def add_forbidden_act_window(self, widget):
        print('log: app  > add_forbidden_act_window')
        self.win_act = Add_Act_Window('forbidden act')
        self.win_act.position = (self.main_window.size[0]/2, self.main_window.size[1]/2)
        self.win_act.ok_bt.on_press = self.add_act
        self.windows.add(self.win_act)
        self.win_act.show()

    def add_abominable_act_window(self, widget):
        print('log: app  > add_abominable_act_window')
        self.win_act = Add_Act_Window('abominable act')
        self.win_act.position = (self.main_window.size[0]/2, self.main_window.size[1]/2)
        self.win_act.ok_bt.on_press = self.add_act
        self.windows.add(self.win_act)
        self.win_act.show()

    def add_act(self, widget):
        print('log: app  > add_forbidden_act')
        self.win_act.close()
        with open(self.path + 'gilding.json', 'r') as f:
            newdata = json.load(f)
        newdata[self.win_act.get()[0]] = [self.win_act.get()[1],int(self.calendar.day_selected), self.calendar.active_mounth]
        self.gilding_list.data.append(self.win_act.get()[0])
        #self.gilding_list.data[0].style.color = '#c00d0d'
        with open(self.path + 'gilding.json', 'w') as f:
            json.dump(newdata, f, indent=2)

    def select_act(self, widget):
        print('select act')
        self.selcted_act = self.gilding_list.selection.title

    def delete_act(self, widget):
        print('log: app  > delete_act')
        with open(self.path + 'gilding.json', 'r') as f:
            data = json.load(f)
        for itm in data:
            if itm == self.selcted_act:
                for row in self.gilding_list.data:
                    if row.title == self.selcted_act:
                        # remove of table
                        self.gilding_list.data.remove(row)
                # remove of database
                data.pop(itm)
                print(data)
        with open(self.path + 'gilding.json', 'w') as f:
            json.dump(data, f, indent=2)

    def select_tab(self, widget):
        print('log: app  > select tab', widget.current_tab.index)
        tab_name = widget.current_tab.index
        if len(widget._content._options) == 2:
            if tab_name == 1:
                self.calendar.set_status_daily()
            elif tab_name == 0:
                self.calendar.set_status_gilding()


def main():
    return Zirkonium()
