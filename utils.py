import os

class Date:
    def __init__(self,
                 year:int=None,
                 month:int=None,
                 week:int=None,
                 day:int=None,
                 day_of_the_week:str=None):
        self.year=year
        self.month=month
        self.week=week
        self.day=day
        self.day_of_the_week=day_of_the_week
        self.unit = -1
        
    def is_leap_year(self) -> bool:
        return self.year % 4 == 0 and (self.year % 100 != 0 or self.year % 400 == 0)
    
    def __eq__(self, other) -> bool:
        assert type(self) == type(other)
        return (self.year == other.year) and (self.month == other.month) and (self.day == other.day)
    
    def __gt__(self, other) -> bool:
        assert type(self) == type(other)
        return (self.year > other.year) or \
            ((self.year == other.year) and (self.month > other.month)) or \
            ((self.year == other.year) and (self.month == other.month and self.day > other.day))
            
    def __str__(self) -> str:
        return f"{self.year}년 {self.month}월 {self.day}일"

class Time:
    def __init__(self,
                 hour:int=None,
                 minute:int=None,
                 second:int=0):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.unit = -1
        
    def update_unit(self):
        self.unit = self.hour * 3600 + self.minute * 60 + self.second
        
    def __eq__(self, other) -> bool:
        assert type(self) == type(other)
        self.update_unit()
        other.update_unit()
        return self.unit == other.unit
    
    def __gt__(self, other) -> bool:
        assert type(self) == type(other)
        self.update_unit()
        other.update_unit()
        return self.unit > other.unit
    
    def __str__(self) -> str:
        return f"{self.hour:02d}:{self.minute:02d}"

def load(path:str):
    ext = path.split('.')[-1]
    if not os.path.exists(path):
        return "error"
    
    if ext =='json':
        import json
        with open(path, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
    elif ext == 'pkl':
        import pickle
        with open(path, 'rb') as f:
            data = pickle.load(f, encoding='utf-8-sig')
    else:
        return "error"
    return data


def compare_datetime(date1:Date, time1:Time, date2:Date, time2:Time):
    if date1 == date2:
        return time1 < time2
    return date1 < date2


def make_date(date_str):
    splitters = ['년', '월', '일']
    for splitter in splitters:
        date_str = date_str.replace(splitter, '|')
    date_int =  list(map(int, date_str.split('|')[:-1]))
    new_date = Date(year=date_int[0], month=date_int[1], day=date_int[2])
    return new_date


def make_time(time_str):
    time_int = list(map(int, time_str.split(':')))
    new_time = Time(time_int[0], time_int[1])
    return new_time