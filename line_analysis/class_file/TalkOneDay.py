from line_analysis.class_file.TimeData import TimeData
from line_analysis.class_file.Conversation import Conversation

import re
from collections import defaultdict

time_pattern = re.compile(r"[0-9]{2}:[0-9]{2}")
class TalkOneDay:
    def __init__(self, talk_history_one_day):
        date_str, talk_history_one_day = talk_history_one_day.split("\n", 1)
        self.date = TimeData()
        self.date.set_day(date_str[:-3])
        self._talk_analyse(talk_history_one_day)
        self._analyze_one_day()
        self._sum_data()

    def _talk_analyse(self, talk_history_one_day):

        conversation_flg = False
        self.conversation_data = []
        sentence = ""
        talker = None
        talk_day = None

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
            elif talk.count("\t") == 1:
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

            conversation = Conversation(self.date.set_time(talk_day), talker)
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
        # 発話者が送った写真の累計回数
        self.pictureTalkerCount = defaultdict(int)
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
        # 発話者
        self.talkerSet = set()

        for content in self.conversation_data:
            talker = content.talker
            self.talkerSet.add(talker)
            self.talkerCount[talker] += 1
            self.strTalkerCount[talker] += content.talk_contents_count
            if content.stamp_flg:
                self.stampTalkerCount[talker] += 1
            if content.picture_flg:
                self.pictureTalkerCount[talker] += 1
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

    def _sum_data(self):
        for talker in self.talkerSet:
            self.talkerCount["all"] += self.talkerCount[talker]
            self.strTalkerCount["all"] += self.strTalkerCount[talker]
            self.stampTalkerCount["all"] += self.stampTalkerCount[talker]
            self.pictureTalkerCount["all"] += self.pictureTalkerCount[talker]
            self.callTalkerCount["all"] += self.callTalkerCount[talker]
            self.missed_call_count["all"] += self.missed_call_count[talker]
            hour, minute, second \
                = self.call_time[talker].hour, \
                  self.call_time[talker].minute, \
                  self.call_time[talker].second
            self.call_time["all"].add_time(hour, minute, second)
            self.linepayTalkerCount["all"] += self.linepayTalkerCount[talker]
            self.linepayTalkerMoney["all"] += self.linepayTalkerMoney[talker]