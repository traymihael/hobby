#!/usr/bin/python
# -*- Coding: utf-8 -*-

# 使用するデータの要素ごとのクラス
# 1年終了している場合はfin_flgにTrueを入れる。途中の場合はFalseを入れる
class DataClassElement:
    def __init__(self, name, fin_flg):
        self.name = name
        self.fin_flg = fin_flg


# 使用するデータのリストクラス
class DataClass:
    def __init__(self):
        self.data_list = []

    def set_label(self, name, fin_flg):
        self.data_list.append(DataClassElement(name, fin_flg))
