from utils import *
import pandas as pd


class Task:
    def __init__(self,
        #          name:str,
        #          start_day:Date,
        #          end_day:Date,
        #          start_time:Time,
        #          end_time:Time,
        #          priority:float,
        #          tags:list=[]):
        # self.name = name
        # self.tags = tags
        # self.start_day = start_day
        # self.start_time = start_time
        # self.end_day = end_day
        # self.end_time = end_time
        # self.priority = priority
                application):
        self.app = application
        
class TaskApplication:
    def __init__(self):
        self.name = "Dummy"
        self.tags = []
        self.priority = 0.5
        
        self.allow_time_specification = False
        self.use_start_time = True
        self.use_end_time = True
        
        self.start_date = Date()
        self.start_time = Time()
        self.end_date = Date()
        self.end_time = Time()
        
        self.allow_repeat = False
        self.infinite = False
        
        self.repeat_value = 0
        self.repeat_unit = None
        self.repeat_end_date = Date()
        self.repeat_end_time = Time()
        
    def check(self) -> bool:
        start_end_seq = True
        start_repeat_seq = True
        if self.allow_time_specification and self.use_start_time and self.use_end_time:
            start_end_seq = compare_datetime(self.start_date, self.start_time, self.end_date, self.end_time)
        if self.allow_time_specification and self.use_start_time and self.allow_repeat and not self.infinite:
            start_repeat_seq = compare_datetime(self.start_date, self.start_time, self.repeat_end_date, self.repeat_end_time)
        return start_end_seq and start_repeat_seq

class TaskManager:
    def __init__(self,
                 data_path:str=None):
        self.data_path = data_path
        self.data = None
        self.task_list = []
        self.alarm_list = []
        self.dataframe = pd.DataFrame()
        
    def load_data(self, data_path:str=None):
        if data_path:
            self.data_path = data_path
        if not self.data_path:
            return "error"
        self.data = load(self.data_path)
        if type(self.data) == dict:
            self.data = [self.data]
            
    def enroll(self, application):
        # 시간 모순 체크
        if not application.check():
            return False
        self.task_list.append(Task(application))
        self.update_dataframe()
    
    def update_dataframe(self):
        self.dataframe = pd.DataFrame()
        for task in self.task_list:
            ap = task.app
            tmp_dict = {
                'name' : ap.name,
                'tags' : str(ap.tags),
                'start_date' : str(ap.start_date),
                'start_time' : str(ap.start_time),
            }
            self.dataframe = pd.concat([self.dataframe, pd.DataFrame([tmp_dict])], ignore_index=True)