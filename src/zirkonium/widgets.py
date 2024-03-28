import json
import os
import jdatetime

from toga import (Box, Window, Button, TextInput, ScrollContainer,
        Label, NumberInput, Switch, ScrollContainer, DetailedList)
from toga.style import Pack
from toga.style.pack import RIGHT, LEFT, CENTER
from toga.colors import rgb


class CalendarWidget(Box):
    def __init__(self, path, month):
        super(CalendarWidget, self).__init__()
        '''
        scrollarea  -> box -> 15 bt
                    -> box -> 15 bt
        press bt -> load tasks
        '''
        self.style = Pack(alignment='center')
        self.path = path
        self.date = ''
        self.months_list = {1: 'فروردین', 2: 'اردیبهشت', 3: 'خرداد', 4: 'تیر', 5: 'مرداد', 6: 'شهریور',
                            7: 'مهر', 8: 'آبان', 9: 'آذر', 10: 'دی', 11: 'بهمن', 12: 'اسفند'}
        self.week_days = {1: 'شنبه', 2: '  یک  ', 3: '  دو  ', 4: '  سه  ',
                            5: ' چهار ', 6: ' پنج ', 7: 'جمعه'}
        self.active_month = month
        self.today = jdatetime.date.today()
        self.year = self.today.year
        self.today_month = self.today.month
        self.today_date_day = self.today.day
        self.day_selected = ''
        
        self.one_day = None
        self.style = Pack(flex=2, direction='column')
        self.main_box = Box(style=Pack(height=180, direction='column'))
        self.infi_label = Label('')
        # toolbar
        toolbar = Box()
        self.next_month_bt = Button('<<')
        self.prev_month_bt = Button('>>')
        self.next_year_bt = Button('<')
        self.prev_year_bt = Button('>')
        self.info_lb = Label('فروردین', style=Pack(width=170, text_align='center'))

        toolbar.add(self.prev_year_bt, self.prev_month_bt, self.info_lb, self.next_month_bt, self.next_year_bt)
        self.one_day_in = NumberInput()
        week_lbs_box = Box()

        for ind in self.week_days.keys():
            lb = Label(self.week_days[ind], style=Pack(padding=((5, 5, 5, 5))))
            week_lbs_box.add(lb)

        self.add(toolbar)
        self.add(week_lbs_box)
        self.add(self.main_box)

        if os.path.isfile(self.path + 'year.json'):
            self.add_bts(self.today_month, self.today_date_day)
            self.set_status_daily()

    def set_one_day(self, one_day):
        print('log: calendar.set_one_day')
        self.one_day = one_day

    def make_year(self):
        print('calender: create year data')
        year = {}
        num = self.one_day  # num = week day number
        for month in self.months_list:
            days = {}
            if month in range(0, 7):
                for nm in range(1, 32):
                    if num < 7:
                        days[nm] = num
                        num += 1
                    elif num == 7:
                        days[nm] = num
                        num = 1
                year[month] = days
                num = days[list(days.keys())[-1]] + 1
            if month in range(7, 13):
                for nm in range(1, 31):
                    if num == 8:
                        num = 1
                    if num < 7:
                        days[nm] = num
                        num += 1
                    elif num == 7:
                        days[nm] = num
                        num = 1
                year[month] = days
                num = days[list(days.keys())[-1]] + 1
        with open(self.path + 'year.json', 'w') as file:
            json.dump(year, file, indent=3)

    def add_bts(self, month=None, day=None):
        """ add bts to calendar widget"""
        print('log: wins > CalendarWidget.add_bts')
        with open(self.path + 'year.json', 'r') as file:
            data = json.load(file)
        if month is not None:
            self.active_month = self.today_month
        self.info_lb.text = str(self.year) + ' - ' + self.months_list[self.active_month]
        bts = data[str(self.active_month)]
        self.box1 = Box()
        self.box2 = Box()
        self.box3 = Box()
        self.box4 = Box()
        self.box5 = Box()
        self.box6 = Box()
        for bx in list(self.main_box.children):
            self.main_box.remove(bx)
        self.main_box.add(self.box1)
        self.main_box.add(self.box2)
        self.main_box.add(self.box3)
        self.main_box.add(self.box4)
        self.main_box.add(self.box5)
        self.main_box.add(self.box6)
        days = list(bts.keys())
        x = bts[days[0]]
        if len(days) == 31:
            if x == 2:
                pre_list = [31]
                numbering = len(pre_list)
                self.box1.style.padding_left = 40 * numbering
            elif x == 3:
                pre_list = [30, 31]
                numbering = len(pre_list)
                self.box1.style.padding_left = 40 * numbering
            elif x == 4:
                pre_list = [29, 30, 31]
                numbering = len(pre_list)
                self.box1.style.padding_left = 40 * numbering
            elif x == 5:
                pre_list = [28, 29, 30, 31]
                numbering = len(pre_list)
                self.box1.style.padding_left = 40 * numbering
            elif x == 6:
                pre_list = [27, 28, 29, 30, 31]
                numbering = len(pre_list)
                self.box1.style.padding_left = 40 * numbering
            elif x == 7:
                pre_list = [26, 27, 28, 29, 30, 31]
                numbering = len(pre_list)
                self.box1.style.padding_left = 40 * numbering
        elif len(days) == 30:
            if x == 2:
                pre_list = [30]
                numbering = len(pre_list)
                self.box1.style.padding_left = 40 * numbering
            elif x == 3:
                pre_list = [29, 30]
                numbering = len(pre_list)
                self.box1.style.padding_left = 40 * numbering
            elif x == 4:
                pre_list = [28, 29, 30]
                numbering = len(pre_list)
                self.box1.style.padding_left = 40 * numbering
            elif x == 5:
                pre_list = [27, 28, 29, 30]
                numbering = len(pre_list)
                self.box1.style.padding_left = 40 * numbering
            elif x == 6:
                pre_list = [26, 27, 28, 29, 30]
                self.box1.style.padding_left = 40 * numbering
                numbering = len(pre_list)
            elif x == 7:
                pre_list = [25, 26, 27, 28, 29, 30]
                numbering = len(pre_list)
                self.box1.style.padding_left = 40 * numbering
        numbering = x
        for dd in days:
            if numbering < 8:
                bt = Button(text=dd, style=Pack(width=40))
                self.box1.add(bt)
                numbering += 1
            elif 15 > numbering >= 8:
                bt = Button(text=dd, style=Pack(width=40))
                self.box2.add(bt)
                numbering += 1
            elif 22 > numbering >= 15:
                bt = Button(text=dd, style=Pack(width=40))
                self.box3.add(bt)
                numbering += 1
            elif 29 > numbering >= 22:
                bt = Button(text=dd, style=Pack(width=40))
                self.box4.add(bt)
                numbering += 1
            elif 36 > numbering >= 29:
                bt = Button(text=dd, style=Pack(width=40))
                self.box5.add(bt)
                numbering += 1
            elif 38 > numbering >= 36:
                bt = Button(text=dd, style=Pack(width=40))
                self.box6.add(bt)
                numbering += 1
            if int(bt.text) == int(self.today_date_day) and self.today_month == self.active_month:
                bt.style.background_color = '#80b4f9'
        if self.active_month == 12:
            self.next_month_bt.enabled = False
            self.prev_month_bt.enabled = True
        elif self.active_month == 1:
            self.prev_month_bt.enabled = False
            self.next_month_bt.enabled = True
        elif 12 > self.active_month > 1:
            self.prev_month_bt.enabled = True
            self.next_month_bt.enabled = True

    def set_status_daily(self):
        print('log: wins > CalendarWidget.set_status_daily')
        # open database
        with open(self.path + 'bank.json', 'r') as file:
            data = json.load(file)
        # get days active
        duty_days = [int(data[task_name]['day']) for task_name in data if data[task_name]['month'] == self.active_month]
        duty_days = list(set(duty_days))
        for task_name in data:
            # get active month
            if int(data[task_name]['month']) == self.today_month:
                for child in list(self.main_box.children):
                    for bt in child.children:
                        # Color assignment buttons
                        if int(bt.text) in duty_days and int(bt.text) > self.today_date_day:
                            bt.style.background_color = '#2ccc00'  # green deep
                        if int(bt.text) in duty_days and int(bt.text) < self.today_date_day:
                            bt.style.background_color = '#f4942e'  # orange
                        if int(bt.text) not in duty_days:
                            bt.style.background_color = '#ffffff'  # white
                        if int(bt.text) == int(self.today_date_day) and self.today_month == self.active_month:
                            bt.style.background_color = '#00d6ff'  # blue
                        if int(bt.text) == self.day_selected:
                            bt.style.background_color = '#5bfe2e'  # green
                        if int(bt.text):
                            bt.enabled = True
            elif self.active_month > self.today_month:
                for child in list(self.main_box.children):
                    for bt in child.children:
                        if int(bt.text):
                            bt.style.background_color = '#ffffff'  # white
                        if int(bt.text) in duty_days:
                            bt.style.background_color = '#2ccc00'  # green deep
                        if int(bt.text) == self.day_selected:
                            bt.style.background_color = '#5bfe2e'  # green
                        if int(bt.text):
                            bt.enabled = True
            elif self.active_month < self.today_month:
                for child in list(self.main_box.children):
                    for bt in child.children:
                        if int(bt.text):
                            bt.style.background_color = '#ffffff'  # white
                        if int(bt.text) in duty_days:
                            bt.style.background_color = '#f4942e'  # orange
                        if int(bt.text) == self.day_selected:
                            bt.style.background_color = '#5bfe2e'  # green
                        if int(bt.text):
                            bt.enabled = True

    def set_status_gilding(self):
        print('log: wins > CalendarWidget.set_status_gilding')
        with open(self.path + 'gilding.json', 'r') as file:
            data = json.load(file)
        # get days have act
        days = [data[day][1] for day in data]
        days = list(set(days))
        if len(data) > 0:
            for itm in data:
                for child in list(self.main_box.children):
                    for bt in child.children:
                        # days_passed
                        if int(bt.text) in days and data[itm][2] == self.active_month:
                            bt.style.background_color = '#f0a702'  # orange
                        # future and passed day
                        if int(bt.text) not in days:
                            bt.style.background_color = '#ffffff'  # white
                        if int(bt.text) > self.today_date_day and data[itm][2] == self.active_month:
                            bt.enabled = False
                        if self.active_month != self.today_month:
                            bt.enabled = False
        elif len(data) == 0:
            for child in list(self.main_box.children):
                for bt in child.children:
                    # Color assignment buttons
                    if int(bt.text) in range(1, 32):
                        bt.style.background_color = '#ffffff'  # white
                    if int(bt.text) > self.today_date_day:
                        bt.enabled = False
        # today_day

    def setdate_task(self, widget):
        print('log: wins > CalendarWidget.setdata_tasks')
        """
        set date and new color by press date bt
        and selecting day
        """
        self.set_status_daily()
        self.reset_texts()
        self.day_selected = int(widget.text)
        # [month selected, day selected]
        self.date = [self.active_month, self.day_selected]
        widget.style.background_color = '#5bfe2e'  # green

    def reset_texts(self):
        print('log: wins > CalendarWidget.reset_text_tasks')
        """
        change widget settings by press bt day for selected day
        """
        colors = [rgb(91, 254, 46), rgb(240, 167, 2)]
        for bt in self.box1.children:
            if bt.style.background_color == colors[0]:  # green
                bt.style.background_color = '#ffffff'   # white
        for bt in self.box2.children:
            if bt.style.background_color == colors[0]:  # green
                bt.style.background_color = '#ffffff'   # white
        for bt in self.box3.children:
            if bt.style.background_color == colors[0]:  # green
                bt.style.background_color = '#ffffff'   # white
        for bt in self.box4.children:
            if bt.style.background_color == colors[0]:  # green
                bt.style.background_color = '#ffffff'   # white
        for bt in self.box5.children:
            if bt.style.background_color == colors[0]:  # green
                bt.style.background_color = '#ffffff'   # white
        for bt in self.box6.children:
            if bt.style.background_color == colors[0]:  # green
                bt.style.background_color = '#ffffff'   # white
    
    def setdate_gilding(self, widget):
        print('log: wins > CalendarWidget.setdata_gilding')
        """
        set date and new color by press date bt
        and selecting day
        """
        self.set_status_gilding()
        self.reset_texts_gilding()
        self.day_selected = int(widget.text)
        # [month selected, day selected]
        self.date = [self.active_month, self.day_selected]
        widget.style.background_color = '#5bfe2e'  # green

    def reset_texts_gilding(self):
        print('log: wins > CalendarWidget.reset_text_gilding')
        """
        change widget settings by press bt day for selected day
        """
        colors = [rgb(91, 254, 46), rgb(240, 167, 2)]
        for bt in self.box1.children:
            if bt.style.background_color == colors[0]:  # green
                bt.style.background_color = '#ffffff'   # white
        for bt in self.box2.children:
            if bt.style.background_color == colors[0]:  # green
                bt.style.background_color = '#ffffff'   # white
        for bt in self.box3.children:
            if bt.style.background_color == colors[0]:  # green
                bt.style.background_color = '#ffffff'   # white
        for bt in self.box4.children:
            if bt.style.background_color == colors[0]:  # green
                bt.style.background_color = '#ffffff'   # white
        for bt in self.box5.children:
            if bt.style.background_color == colors[0]:  # green
                bt.style.background_color = '#ffffff'   # white
        for bt in self.box6.children:
            if bt.style.background_color == colors[0]:  # green
                bt.style.background_color = '#ffffff'   # white