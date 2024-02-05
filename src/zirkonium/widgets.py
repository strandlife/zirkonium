import json
import os
from zirkonium.wins import AddYearWindow

from toga import (Box, Window, Button, TextInput, ScrollContainer,
        Label, NumberInput, Switch, ScrollContainer, DetailedList)
from toga.style import Pack
from toga.colors import rgb


class CalendarWidget(Box):
    def __init__(self, path, mounth):
        super(CalendarWidget, self).__init__()
        '''
        scrollarea  -> box -> 15 bt
                    -> box -> 15 bt
        press bt -> load tasks
        '''
        self.style = Pack(alignment='center')
        self.path = path
        self.date = ''
        self.mounths_list = {1:'فروردین', 2:'اردیبهشت', 3:'خرداد', 4:'تیر',
                            5:'مرداد', 6:'شهریور', 7:'مهر', 8:'آبان', 9:'آذر',
                            10:'دی', 11:'بهمن', 12:'اسفند'}
        self.week_days = {1:'شنبه', 2:'یکشنبه', 3:'دوشنبه',
                        4:'سه شنبه', 5:'چهارشنبه', 6:'پنج شنبه', 7:'جمعه'}
        self.active_mounth = mounth
        self.one_day = None
        self.style = Pack(flex=2, direction='column')
        self.main_box = Box(style=Pack(direction='column'))
        self.scr = ScrollContainer(style=Pack(flex=2, height=200))
        self.infi_label = Label('')
        # toolbar
        toolbar = Box()
        next_mounth = Button('<<')
        next_mounth.on_press = self.next_mounth
        prev_mounth = Button('>>')
        prev_mounth.on_press = self.prev_mounth
        next_year = Button('<')
        prev_year = Button('>')
        self.info_lb = Label('1390 - فروردین')
        toolbar.add(prev_year, prev_mounth, self.info_lb, next_mounth, next_year)

        self.one_day_in = NumberInput()
        
        week_lbs_box = Box()
        for title in self.week_days.keys():
            lb = Label(title, style=Pack(padding=((5,5,5,5))))
            week_lbs_box.add(lb)
        self.add(toolbar)
        self.add(week_lbs_box)
        self.scr.content = self.main_box
        self.add(self.scr)
        if os.path.isfile(self.path + 'year.json'):
            self.add_bts()
        self.set_status()

    def set_one_day(self, one_day):
        self.one_day = one_day

    def make_year(self):
        print('calender: create year data')
        year = {}
        num = self.one_day  # num = week day number
        for mounth in self.mounths_list:
            days = {}
            if mounth in range(0,7):
                for nm in range(1, 32):
                    if num < 7:
                        days[nm] = num
                        num += 1
                    elif num == 7:
                        days[nm] = num
                        num = 1
                year[mounth] = days
                print('>',days)
                num = days[list(days.keys())[-1]] + 1
            if mounth in range(7, 13):
                for nm in range(1, 31):
                    if num < 7:
                        days[nm] = num
                        num += 1
                    elif num == 7:
                        days[nm] = num
                        num = 1
                    elif num == 8:
                        num = 1
                year[mounth] = days
                print('>>',days)
                num = days[list(days.keys())[-1]] + 1
        with open(self.path + 'year.json', 'r') as file:
                json.load(file)
        file = year
        with open(self.path + 'year.json', 'w') as file:
            json.dump(year, file, indent=3)

    def next_mounth(self, widget):
        current_index = self.active_mounth - 1
        self.active_mounth = list(self.mounths_list.keys())[current_index + 1]
        self.info_lb.text = self.mounths_list[self.active_mounth] + '1390'
        self.add_bts()

    def prev_mounth(self, widget):
        current_index = self.active_mounth -1
        self.active_mounth = list(self.mounths_list.keys())[current_index - 1]
        self.info_lb.text = self.mounths_list[self.active_mounth] + '1390'
        self.add_bts()

    def add_bts(self):
        """ add bts to calendar widget"""
        print('log: wins > CalendarWidget.add_bts')
        print('active ',self.active_mounth)
        with open(self.path + 'year.json', 'r') as file:
            data = json.load(file)
        self.main_box.clear()
        bts = data[str(self.active_mounth)]
        self.box1 = Box()
        self.box2 = Box()
        self.box3 = Box()
        self.box4 = Box()
        self.box5 = Box()
        self.box6 = Box()
        
        days = list(bts.keys())
        print(bts[days[0]])
        if bts[days[0]] == 2:
            numbering = 0
            for dd in range(31, 32):
                bt = Button(text=dd, style=Pack(width=40))
                bt.enabled = False
                self.box1.add(bt)
                numbering += 1
            for dd in days:
                if numbering < 7:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box1.add(bt)
                    numbering += 1
                elif 14 > numbering >= 7:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box2.add(bt)
                    numbering += 1
                elif 21 > numbering >= 14:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box3.add(bt)
                    numbering += 1
                elif 28 > numbering >= 21:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box4.add(bt)
                    numbering += 1
                elif 33 > numbering >= 28:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box5.add(bt)
            for dd in range(1, 3):
                bt = Button(text=dd, style=Pack(width=40))
                bt.enabled = False
                self.box5.add(bt)
        
        if bts[days[0]] == 3:
            numbering = 0
            for dd in range(30, 32):
                bt = Button(text=dd, style=Pack(width=40))
                bt.enabled = False
                self.box1.add(bt)
                numbering += 1
            for dd in days:
                if numbering < 7:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box1.add(bt)
                    numbering += 1
                elif 14 > numbering >= 7:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box2.add(bt)
                    numbering += 1
                elif 21 > numbering >= 14:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box3.add(bt)
                    numbering += 1
                elif 28 > numbering >= 21:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box4.add(bt)
                    numbering += 1
                elif 32 > numbering >= 28:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box5.add(bt)
            for dd in range(1, 3):
                bt = Button(text=dd, style=Pack(width=40))
                bt.enabled = False
                self.box5.add(bt)
        
        if bts[days[0]] == 4:
            numbering = 0
            for dd in range(29, 32):
                bt = Button(text=dd, style=Pack(width=40))
                bt.enabled = False
                self.box1.add(bt)
                numbering += 1
            for dd in days:
                if numbering < 7:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box1.add(bt)
                    numbering += 1
                elif 14 > numbering >= 7:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box2.add(bt)
                    numbering += 1
                elif 21 > numbering >= 14:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box3.add(bt)
                    numbering += 1
                elif 28 > numbering >= 21:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box4.add(bt)
                    numbering += 1
                elif 35 > numbering >= 28:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box5.add(bt)
            for dd in range(1, 2):
                bt = Button(text=dd, style=Pack(width=40))
                bt.enabled = False
                self.box5.add(bt)
        
        if bts[days[0]] == 5:
            numbering = 0
            for dd in range(27, 32):
                bt = Button(text=dd, style=Pack(width=40))
                bt.enabled = False
                self.box1.add(bt)
                numbering += 1
            for dd in days:
                if numbering < 7:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box1.add(bt)
                    numbering += 1
                elif 14 > numbering >= 7:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box2.add(bt)
                    numbering += 1
                elif 21 > numbering >= 14:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box3.add(bt)
                    numbering += 1
                elif 28 > numbering >= 21:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box4.add(bt)
                    numbering += 1
                elif 35 > numbering >= 28:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box5.add(bt)
            for dd in range(1, 2):
                bt = Button(text=dd, style=Pack(width=40))
                bt.enabled = False
                self.box5.add(bt)
        
        if bts[days[0]] == 6:
            numbering = 0
            for dd in range(26, 32):
                bt = Button(text=dd, style=Pack(width=40))
                bt.enabled = False
                self.box1.add(bt)
                numbering += 1
            for dd in days:
                if numbering < 7:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box1.add(bt)
                    numbering += 1
                elif 14 > numbering >= 7:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box2.add(bt)
                    numbering += 1
                elif 21 > numbering >= 14:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box3.add(bt)
                    numbering += 1
                elif 28 > numbering >= 21:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box4.add(bt)
                    numbering += 1
                elif 35 > numbering >= 28:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box5.add(bt)
                    numbering += 1
                elif 37 > numbering >= 35:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box6.add(bt)
            for dd in range(1, 2):
                bt = Button(text=dd, style=Pack(width=40))
                bt.enabled = False
                self.box5.add(bt)
        
        if bts[days[0]] == 7:
            numbering = 0
            for dd in range(26, 32):
                bt = Button(text=dd, style=Pack(width=40))
                bt.enabled = False
                self.box1.add(bt)
                numbering += 1
            for dd in days:
                if numbering < 7:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box1.add(bt)
                    numbering += 1
                elif 14 > numbering >= 7:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box2.add(bt)
                    numbering += 1
                elif 21 > numbering >= 14:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box3.add(bt)
                    numbering += 1
                elif 28 > numbering >= 21:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box4.add(bt)
                    numbering += 1
                elif 35 > numbering >= 28:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box5.add(bt)
                    numbering += 1
                elif 37 > numbering >= 35:
                    bt = Button(text=dd, style=Pack(width=40))
                    self.box6.add(bt)
            for dd in range(1, 6):
                bt = Button(text=dd, style=Pack(width=40))
                bt.enabled = False
                self.box6.add(bt)
        
        if bts[days[0]] == 1:
            for d in bts:
                bt = Button(text=d, style=Pack(width=40))
                self.box1.add(bt)
        self.main_box.add(self.box1)
        self.main_box.add(self.box2)
        self.main_box.add(self.box3)
        self.main_box.add(self.box4)
        self.main_box.add(self.box5)
        self.main_box.add(self.box6)

    def set_status(self):
        print('log: wins > CalendarWidget.set_status')
        with open(self.path + 'bank.json', 'r') as file:
            data = json.load(file)
        duty_days = [data[day][4] for day in data]
        duty_days = list(set(duty_days))
        '''
        for bt in self.box1.children:
            if int(bt.text) in duty_days:
                bt.style.background_color = '#f178f8'  # pink
        for bt in self.box2.children:
            if int(bt.text) in duty_days:
                bt.style.background_color = '#f178f8'  # pink
        '''

    def setdate(self, widget):
        print('log: wins > CalendarWidget.setdata')
        """
        set date and new color by press date bt
        """
        self.set_status()
        self.reset_texts()
        self.date = widget.text
        widget.style.background_color = '#2fd100'  # green

    def reset_texts(self):
        print('log: wins > CalendarWidget.reset_text')
        """
        change widget settings by press bt day
        """
        for bt in self.box1.children:
            if bt.style.background_color == rgb(47, 209, 0):  # green
                bt.style.background_color = '#ffffff'   # white
        for bt in self.box2.children:
            if bt.style.background_color == rgb(47, 209, 0):  # green
                bt.style.background_color = '#ffffff'   # white
