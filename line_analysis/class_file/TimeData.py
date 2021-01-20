class TimeData:
    def __init__(self):
        self.year, self.month, self.day = 0, 0, 0
        self.hour, self.minute, self.second = 0, 0, 0

    def add_time(self, hour, minute, second):
        self.second, kuriagari = (int(self.second) + second) % 60, (int(self.second) + second) // 60
        self.minute, kuriagari = (int(self.minute) + minute + kuriagari) % 60, (
                int(self.minute) + minute + kuriagari) // 60
        self.hour = int(self.hour) + hour + kuriagari

    def display_time(self):
        return f"{str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}:{str(self.second).zfill(2)}"

    def set_day(self, date_data):
        self.year, self.month, self.day = map(int, date_data.split("/"))

    def set_time(self, talk_day):
        self.hour, self.minute = map(int, talk_day.split(":"))

    def display_day(self):
        return f"{str(self.year)}/{str(self.month).zfill(2)}/{str(self.day).zfill(2)}"