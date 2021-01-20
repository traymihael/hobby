from line_analysis.class_file.TimeData import TimeData

class Conversation:
    def __init__(self, date, talker):
        self.talker = talker
        self.date = date
        self.talk = None
        self.talk_contents = None
        self.talk_contents_count = 0
        self.stamp_flg = False
        self.picture_flg = False
        self.call_flg = False
        self.call_time = TimeData()
        self.line_pay_flg = False
        self.line_pay_money = 0

    def apply_line_pay(self, money):
        self.line_pay_flg = True
        self.line_pay_money = money

    def apply_contents(self, contents):

        if "☎" in contents:
            phone_history = contents.split()
            self.call_flg = True
            if len(phone_history) != 3:
                return
            if phone_history[2].count(":") == 2:
                hour, minute, second = map(int, phone_history[2].split(":"))
            else:
                hour = 0
                minute, second = map(int, phone_history[2].split(":"))
            self.call_time.add_time(hour, minute, second)
        elif contents == "[スタンプ]":
            self.stamp_flg = True
        elif contents == "[写真]":
            self.picture_flg = True
        else:
            self.talk = contents
            self.talk_contents_count = len(contents)
