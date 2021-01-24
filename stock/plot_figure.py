#!/usr/bin/python
# -*- Coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from matplotlib import dates as mdates
from stock.DataClass import DataClass

plt.rcParams["font.family"] = "IPAexGothic"

DT_NOW = dt.datetime.now()
DEFINITION_YEAR = 1900

data_class = DataClass()
one_year_xlist = [dt.datetime(DEFINITION_YEAR, 1, 1), dt.datetime(DEFINITION_YEAR, 12, 31)]
ax = plt.subplot()

# 必要に応じてここから下にデータを追記

data_class.set_label("test", True)
# data_class.set_label("2020", True)
# data_class.set_label("2021", False)

# 縦軸の数値は消した方がいいかも
# ax.axes.yaxis.set_ticklabels([])

# 追加したいグラフがあればここに追記
def add_graph():
    add_straight(score=0, label="損益分岐点")
    # add_straight(score=10000, label="目標")
    pass


# 追記ここまで


# x軸に並行なグラフの追加
def add_straight(score, label):
    ylist = [score, score]
    ax.plot(one_year_xlist, ylist, linestyle="dashdot", label=label, alpha=0.3)


# csvデータの読み込みとプロット
def load_data(data_element):
    # データの読み込み
    data = pd.read_csv(f"./data/{data_element.name}.csv")
    data = data.dropna(subset=["通算損益[円]"])

    # 日時順に並び替え
    data["datetime"] = [dt.datetime.strptime(day[5:], "%m/%d") for day in data["譲渡日"]]
    data = data.sort_values("datetime")

    xlist = list(data["datetime"])
    ylist = [int(money.replace(",", "")) for money in data["通算損益[円]"]]

    # 並び替えたものを書き出し
    data.drop("datetime", axis=1).to_csv(f"./data/{data_element.name}.csv", index=False)

    # 1月1日のデータを挿入
    xlist = [dt.datetime(DEFINITION_YEAR, 1, 1)] + xlist
    ylist = [0] + ylist

    # 折れ線グラフにならないように当日ににその前のデータを入れる
    for i in range(len(xlist))[:0:-1]:
        xlist.insert(i, xlist[i])
        ylist.insert(i, ylist[i - 1])

    # 末尾に12月31日もしくは今日のデータを挿入
    if data_element.fin_flg:
        # 12月31日のデータを挿入
        xlist.append(one_year_xlist[1])
    else:
        xlist.append(dt.datetime(DEFINITION_YEAR, DT_NOW.month, DT_NOW.day))
    ylist.append(ylist[-1])

    # データをプロット
    ax.plot(xlist, ylist, linestyle="solid", label=f"譲渡損益({data_element.name}年)", alpha=0.7)


# 画像の出力
def plot_data():
    # 追加グラフ
    add_graph()

    # 諸々設定
    plt.title("譲渡損益の推移")
    plt.legend(loc="lower right")
    xfmt = mdates.DateFormatter("%m/%d")
    ax.xaxis.set_major_formatter(xfmt)
    ax.set_xlim(one_year_xlist[0], one_year_xlist[-1])
    plt.xlabel("日付")
    plt.ylabel("譲渡損益")

    # 画像保存
    plt.savefig(f"./figure/{DT_NOW.strftime('%Y%m%d')}.png")


def main():
    for data_element in data_class.data_list:
        # データの読み込みとプロット
        load_data(data_element)
    # プロット
    plot_data()


if __name__ == '__main__':
    main()
