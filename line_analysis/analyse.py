import re
import datetime
from line_analysis.class_file.TimeData import TimeData
from line_analysis.class_file.TalkData import TalkData
from copy import deepcopy




def calc_day_elapsed(start_day: TimeData, save_day: TimeData):
    dt_start = datetime.datetime(year=start_day.year, month=start_day.month, day=start_day.day)
    dt_save = datetime.datetime(year=save_day.year, month=save_day.month, day=save_day.day)
    return (dt_save - dt_start).days


def max_str_one_day(_talk_data):
    talk_data = deepcopy(_talk_data)
    talk_data.sort(key=lambda x: -x.strTalkerCount["all"])
    return talk_data


def max_talk_count_one_day(_talk_data):
    talk_data = deepcopy(_talk_data)
    talk_data.sort(key=lambda x: -x.talkerCount["all"])
    return talk_data


def used_data(partner):
    talk_data = TalkData(partner)
    max_str_data = max_str_one_day(talk_data.analyse_data)
    max_talk_data = max_talk_count_one_day(talk_data.analyse_data)
    context = {}
    context["talk_day_count"] = talk_data.talkSumDay
    context["sum_talk_str_count_all"] = talk_data.strTalkerCount["all"]
    context["avg_talk_str_count_all"] = round(talk_data.strTalkerCount["all"] / talk_data.talkSumDay, 1)
    context["sum_talk_count_all"] = talk_data.talkerCount["all"]
    context["avg_talk_count_all"] = round(talk_data.talkerCount["all"] / talk_data.talkSumDay, 1)
    context["sum_phone_time_all"] = talk_data.call_time["all"].display_time()
    context["passed_day"] = calc_day_elapsed(talk_data.start_day, talk_data.save_day)
    context["start_talk_day"] = talk_data.start_day.display_day()
    context["talk_partner"] = talk_data.partner
    context["save_day"] = talk_data.save_day.display_day()
    context["max_str_data_one_day"] = max_str_data[0].strTalkerCount["all"]
    context["max_str_data_one_day_date"] = max_str_data[0].date.display_day()
    context["max_talk_data_one_day"] = max_talk_data[0].talkerCount["all"]
    context["max_talk_data_one_day_date"] = max_talk_data[0].date.display_day()
    return context


def main_process():
    partner = "test_talk.txt"
    talk_data = TalkData(partner)
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

    max_str_one_day_data = max_str_one_day(talk_data.analyse_data)
    max_talk_count_one_day_data = max_talk_count_one_day(talk_data.analyse_data)

    for element in max_str_one_day_data[:3]:
        print(f"- 発話文字数: {element.strTalkerCount['all']}, 日時: {element.date.display_day()}")
    print()
    for element in max_talk_count_one_day_data[:3]:
        print(f"- 発話回数: {element.talkerCount['all']}, 日時: {element.date.display_day()}")
    print()


def main():
    main_process()


if __name__ == '__main__':
    main()
