import glob, re, sys
from pprint import pprint
import datetime
from collections import defaultdict

PartnerTalkData = "test_talk.txt"



class TimeData:
    def __init__(self):
        self.hour = 0
        self.minute = 0
        self.second = 0

    def add_time(self, hour, minute, second):
        self.second, kuriagari = (int(self.second) + second) % 60, (int(self.second) + second) // 60
        self.minute, kuriagari = (int(self.minute) + minute + kuriagari) % 60, (int(self.minute) + minute + kuriagari) // 60
        self.hour = int(self.hour) + hour + kuriagari

    def display_time(self):
        return f"{str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}:{str(self.second).zfill(2)}"

class Conversation:
    def __init__(self, date, talker):
        self.talker = talker
        self.date = date
        self.talk = None
        self.talk_contents = None
        self.talk_contents_count = 0
        self.stamp_flg = False
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
        else:
            self.talk = contents
            self.talk_contents_count = len(contents)

time_pattern = re.compile(r"[0-9]{2}:[0-9]{2}")
line_pay_pattern = re.compile(r"(.*?)が(.*?) 円相当のLINE Pay残高またはボーナスを送りました。$")
date_pattern = re.compile(r"[0-9]{4}/[0-9]{2}/[0-9]{2}\(.\)")


class TalkOneDay:
    def __init__(self, talk_history_one_day):
        date_str, talk_history_one_day = talk_history_one_day.split("\n", 1)
        self.date = datetime.datetime.strptime(date_str[:-3], "%Y/%m/%d")
        self._talk_analyse(talk_history_one_day)
        self._analyze_one_day()

    def _talk_analyse(self, talk_history_one_day):

        conversation_flg = False
        self.conversation_data = []
        sentence = ""
        talker = None

        talk_history_one_day = talk_history_one_day.split("\n")
        for i, talk in enumerate(talk_history_one_day):
            if conversation_flg:
                if len(talk) == 0:
                    sentence += "\n"
                    continue
                sentence += talk
                if talk[-1] == '\"':
                    if i == len(talk_history_one_day) - 1 \
                            or (time_pattern.match(talk_history_one_day[i + 1][:5])):
                        conversation_flg = False
                        sentence = sentence[:-1]
            elif talk.count("\t") == 0:
                if "LINE Pay" in talk:
                    linePay_data = line_pay_pattern.match(talk)
                    talker, money = linePay_data.group(1), linePay_data.group(2)
                    money = int(money.replace(",", ""))
                    conversation = Conversation(self.date, talker)
                    conversation.apply_line_pay(money)
                    self.conversation_data.append(conversation)
                    continue
            elif talk.count("\t")  == 1:
                if talk.split("\t")[1] == "メッセージの送信を取り消しました":
                    continue
                else:
                    print(talk)
            else:
                talk_day, talker, talk_contents = talk.split("\t", 2)
                if talk_contents[0] == '\"':
                    conversation_flg = True
                    sentence += talk_contents[1:]
                    continue
                else:
                    sentence += talk_contents

            conversation = Conversation(self.date, talker)
            conversation.apply_contents(sentence)
            self.conversation_data.append(conversation)
            sentence = ""

    def _analyze_one_day(self):
        # 発話者が何回発話したか(電話含む)
        self.talkerCount = defaultdict(int)
        # 発話者が発した文字数累計
        self.strTalkerCount = defaultdict(int)
        # 発話者が使ったスタンプの累計回数
        self.stampTalkerCount = defaultdict(int)
        # 発話者が電話をかけた回数
        self.callTalkerCount = defaultdict(int)
        # 発話者が電話をかけて不在着信になった回数
        self.missed_call_count = defaultdict(int)
        # 発話者が電話をかけて話した総時間
        self.call_time = defaultdict(lambda: TimeData())
        # 発話者がLINE PAYを送った回数
        self.linepayTalkerCount = defaultdict(int)
        # 発話者がLINE PAYを送った金額
        self.linepayTalkerMoney = defaultdict(int)

        for content in self.conversation_data:
            talker = content.talker
            self.talkerCount[talker] += 1
            self.strTalkerCount[talker] += content.talk_contents_count
            if content.stamp_flg:
                self.stampTalkerCount[talker] += 1
            if content.call_flg:
                self.callTalkerCount[talker] += 1
                if content.call_time.hour == content.call_time.minute == content.call_time.second == 0:
                    self.missed_call_count[talker] += 1
                else:
                    hour, minute, second = content.call_time.hour, content.call_time.minute, content.call_time.second
                    self.call_time[talker].add_time(hour, minute, second)

            if content.line_pay_flg:
                self.linepayTalkerCount[talker] += 1
                self.linepayTalkerMoney[talker] += content.line_pay_money


class TalkData:
    def __init__(self):
        self.talk_path = f"./talk_data/{PartnerTalkData}"
        self._get_talk_data()
        self._extract_talk_data()
        self._extract_talker()
        self._analyze_all()

    def _get_talk_data(self):
        with open(self.talk_path, "r", encoding="utf-8-sig") as f:
            talk_data = f.read().strip().split("\n\n")
        self.talk_data = ["" for _ in range(len(talk_data))]
        self.talk_data[0] = talk_data[0]

        now_idx = 0
        for i in range(1, len(talk_data)):
            first_data = talk_data[i][:13]
            if date_pattern.match(first_data):
                now_idx += 1
            else:
                self.talk_data[now_idx] += "\n\n"

            self.talk_data[now_idx] += talk_data[i]

        self.talk_data = self.talk_data[:now_idx + 1]

    def _extract_talk_data(self):
        head_data = self.talk_data[0].split("\n")
        self.partner = re.match(r"\[LINE\] (.+?)とのトーク履歴$", head_data[0]).group(1)
        save_date = re.match(r"保存日時：(.+?)$", head_data[1]).group(1)
        self.save_data = datetime.datetime.strptime(save_date, '%Y/%m/%d %H:%M')
        self.analyse_data = [TalkOneDay(talk_history_one_day) for talk_history_one_day in self.talk_data[1:]]

    def _extract_talker(self):
        self.talkerSet = set()
        for day_data in self.analyse_data:
            self.talkerSet |= set(day_data.talkerCount.keys())

    def _analyze_all(self):
        # 発話者が何回発話したか(電話含む)
        self.talkerCount = defaultdict(int)
        # 発話者が発した文字数累計
        self.strTalkerCount = defaultdict(int)
        # 発話者が使ったスタンプの累計回数
        self.stampTalkerCount = defaultdict(int)
        # 発話者が電話をかけた回数
        self.callTalkerCount = defaultdict(int)
        # 発話者が電話をかけて不在着信になった回数
        self.missed_call_count = defaultdict(int)
        # 発話者が電話をかけて話した総時間
        self.call_time = defaultdict(lambda: TimeData())
        # 発話者がLINE PAYを送った回数
        self.linepayTalkerCount = defaultdict(int)
        # 発話者がLINE PAYを送った金額
        self.linepayTalkerMoney = defaultdict(int)

        for day_data in self.analyse_data:
            for talker in self.talkerSet:
                self.talkerCount[talker] += day_data.talkerCount[talker]
                self.strTalkerCount[talker] += day_data.strTalkerCount[talker]
                self.stampTalkerCount[talker] += day_data.stampTalkerCount[talker]
                self.callTalkerCount[talker] += day_data.callTalkerCount[talker]
                self.missed_call_count[talker] += day_data.missed_call_count[talker]
                hour, minute, second \
                    = day_data.call_time[talker].hour, \
                      day_data.call_time[talker].minute, \
                      day_data.call_time[talker].second
                self.call_time[talker].add_time(hour, minute, second)
                self.linepayTalkerCount[talker] += day_data.linepayTalkerCount[talker]
                self.linepayTalkerMoney[talker] += day_data.linepayTalkerMoney[talker]

        for talker in self.talkerSet:
            self.talkerCount["all"] += self.talkerCount[talker]
            self.strTalkerCount["all"] += self.strTalkerCount[talker]
            self.stampTalkerCount["all"] += self.stampTalkerCount[talker]
            self.callTalkerCount["all"] += self.callTalkerCount[talker]
            self.missed_call_count["all"] += self.missed_call_count[talker]
            hour, minute, second \
                = self.call_time[talker].hour, \
                  self.call_time[talker].minute, \
                  self.call_time[talker].second
            self.call_time["all"].add_time(hour, minute, second)
            self.linepayTalkerCount["all"] += self.linepayTalkerCount[talker]
            self.linepayTalkerMoney["all"] += self.linepayTalkerMoney[talker]


def main_process():
    talk_data = TalkData()
    # pprint(talk_data.talk_data)
    print("トーク相手: ", talk_data.partner)
    print("- トーク回数: ", talk_data.talkerCount)
    print("- 発話文字数: ", talk_data.strTalkerCount)
    print("- スタンプ回数: ", talk_data.stampTalkerCount)
    print("- 通話時間: ", talk_data.call_time["all"].display_time())


def main():
    main_process()


if __name__ == '__main__':
    main()
