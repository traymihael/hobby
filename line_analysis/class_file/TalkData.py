
from line_analysis.class_file.TimeData import TimeData
from line_analysis.class_file.TalkOneDay import TalkOneDay
import re
from collections import defaultdict

date_pattern = re.compile(r"[0-9]{4}/[0-9]{2}/[0-9]{2}\(.\)")

class TalkData:
    def __init__(self, partner):
        self.talk_path = f"./talk_data/{partner}"
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
        save_date = re.match(r"保存日時：(.+?)$", head_data[1]).group(1).split()
        self.save_day = TimeData()
        self.save_day.set_day(save_date[0])
        self.save_day.set_time(save_date[1])
        self.analyse_data = [TalkOneDay(talk_history_one_day) for talk_history_one_day in self.talk_data[1:]]
        self.start_day = self.analyse_data[0].date

    def _extract_talker(self):
        self.talkerSet = set()
        for day_data in self.analyse_data:
            self.talkerSet |= set(day_data.talkerCount.keys())
        self.talkerSet.discard("all")

    def _analyze_all(self):
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
        # トーク日数
        self.talkSumDay = len(self.analyse_data)

        for day_data in self.analyse_data:
            for talker in self.talkerSet:
                self.talkerCount[talker] += day_data.talkerCount[talker]
                self.strTalkerCount[talker] += day_data.strTalkerCount[talker]
                self.stampTalkerCount[talker] += day_data.stampTalkerCount[talker]
                self.pictureTalkerCount[talker] += day_data.pictureTalkerCount[talker]
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