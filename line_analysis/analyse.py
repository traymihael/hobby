import re
import datetime
from line_analysis.class_file.TimeData import TimeData
from line_analysis.class_file.TalkData import TalkData

PartnerTalkData = "なっつん.txt"

line_pay_pattern = re.compile(r"(.*?)が(.*?) 円相当のLINE Pay残高またはボーナスを送りました。$")


def calc_day_elapsed(start_day: TimeData, save_day: TimeData):
    dt_start = datetime.datetime(year=start_day.year, month=start_day.month, day=start_day.day)
    dt_save = datetime.datetime(year=save_day.year, month=save_day.month, day=save_day.day)
    return (dt_save - dt_start).days


def max_str_one_day(talk_data):
    talk_data.sort(key=lambda x: -x.strTalkerCount["all"])
    for element in talk_data[:3]:
        print(f"- 発話文字数: {element.strTalkerCount['all']}, 日時: {element.date.display_day()}")
    print()


def max_talk_count_one_day(talk_data):
    talk_data.sort(key=lambda x: -x.talkerCount["all"])
    for element in talk_data[:3]:
        print(f"- 発話回数: {element.talkerCount['all']}, 日時: {element.date.display_day()}")
    print()


def main_process():
    talk_data = TalkData(PartnerTalkData)
    print("トーク相手:", talk_data.partner)
    print("- 保存日時: ", talk_data.save_day.display_day())
    print("- トーク開始日", talk_data.start_day.display_day())
    print("- 経過日数: ", calc_day_elapsed(talk_data.start_day, talk_data.save_day))
    print("- トーク日数:", talk_data.talkSumDay)
    print("- トーク回数:", talk_data.talkerCount)
    print("- 発話文字数:", talk_data.strTalkerCount)
    print("- 写真送信回数:", talk_data.pictureTalkerCount)
    print("- スタンプ回数:", talk_data.stampTalkerCount)
    print("- 通話時間:", talk_data.call_time["all"].display_time())
    print()
    print("集計")
    max_str_one_day(talk_data.analyse_data)
    max_talk_count_one_day(talk_data.analyse_data)


def main():
    main_process()


if __name__ == '__main__':
    main()
