import glob, re
from pprint import pprint
import datetime
from collections import defaultdict

PartnerTalkData = "test_talk.txt"


class Phone:
    def __init__(self):
        self.missed_call_count = 0
        self.call_time = datetime.time(0)

    def phone_analyse(self, phone_history):
        phone_history = phone_history.split()
        if len(phone_history) == 3:
            if phone_history[2].count(":") == 2:
                self.call_time = datetime.datetime.strptime(phone_history[2], "%H:%M:%S")
            else:
                self.call_time = datetime.datetime.strptime(phone_history[2], "%M:%S")
        else:
            self.missed_call_count += 1


class TalkOneDay:
    def __init__(self, talk_history_one_day):
        date_str, talk_history_one_day = talk_history_one_day.split("\n", 1)
        self.date = datetime.datetime.strptime(date_str[:-3], "%Y/%m/%d")
        self._talk_analyse(talk_history_one_day)

    def _talk_analyse(self, talk_history_one_day):
        # 発話者が何回発話したか(電話含む)
        self.talkerCount = defaultdict(int)
        # 発話者が発した文字数累計
        self.strTalkerCount = defaultdict(int)
        # 発話者が使ったスタンプの累計回数
        self.stampTalkerCount = defaultdict(int)
        # 発話者が電話をかけた回数
        self.stampTalkerCount = defaultdict(int)
        # 発話者がLINE PAYを送った回数
        self.linepayTalkerCount = defaultdict(int)
        # 発話者の通話データ
        self.phoneData = defaultdict(Phone)

        conversation_flg = False
        talker = None
        for talk in talk_history_one_day.split("\n"):
            if conversation_flg:
                if talk[-1] == '\"':
                    conversation_flg = False
                self.strTalkerCount[talker] += len(talk) - 1
            elif talk.count("\t") == 0:
                if "LINE Pay" in talk:
                    linePay_data = re.match(r"(.*?)が(.*?) 円相当のLINE Pay残高またはボーナスを送りました。$", talk)
                    talker, money = linePay_data.group(1), linePay_data.group(2)
                    self.linepayTalkerCount[talker] += 1
            else:
                talk_day, talker, talk_contents = talk.split("\t", 2)
                self.talkerCount[talker] += 1
                if talk_contents[0] == '\"':
                    conversation_flg = True
                    talk_contents = talk_contents[1:]
                if "☎" in talk_contents:
                    self.phoneData[talker].phone_analyse(talk_contents)
                elif talk_contents == "[スタンプ]":
                    self.stampTalkerCount[talker] += 1
                else:
                    self.strTalkerCount[talker] += len(talk_contents)


class TalkData:
    def __init__(self):
        self.talk_path = f"./talk_data/{PartnerTalkData}"
        self._get_talk_data()
        self._extract_talk_data()

    def _get_talk_data(self):
        with open(self.talk_path, "r") as f:
            self.talk_data = f.read().strip().split("\n\n")

    def _extract_talk_data(self):
        head_data = self.talk_data[0].split("\n")
        self.partner = re.match(r"\[LINE\] (.+?)とのトーク履歴$", head_data[0]).group(1)
        save_date = re.match(r"保存日時：(.+?)$", head_data[1]).group(1)
        self.save_data = datetime.datetime.strptime(save_date, '%Y/%m/%d %H:%M')

        self.analyse_data = [TalkOneDay(talk_history_one_day) for talk_history_one_day in self.talk_data[1:]]


def main_process():
    talk_data = TalkData()
    # pprint(talk_data.talk_data)
    print("トーク相手: ", talk_data.partner)
    for day_data in talk_data.analyse_data:
        print(day_data.date.strftime("%Y/%m/%d"))
        print("- トーク回数: ", day_data.talkerCount)
        print("- 発話文字数: ", day_data.strTalkerCount)
        print("- スタンプ回数: ", day_data.stampTalkerCount)


def main():
    main_process()


if __name__ == '__main__':
    main()
