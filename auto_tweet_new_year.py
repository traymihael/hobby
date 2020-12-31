# -*- coding: utf-8 -*-

from twitter import Twitter, OAuth
from datetime import datetime
import os

access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

t = Twitter(auth=OAuth(access_token, access_token_secret, api_key, api_secret))

def main_process():
    now_time = datetime.now().strftime("%Y年%m月%d日 %H時%M分%S秒")
    tweet_text = f"【定期実行】\n" \
                 f"{now_time}です。\n" \
                 f"あけましておめでとうございます。\n" \
                 f"本年もどうぞよろしくお願いします。"
    t.statuses.update(status=tweet_text)

def main():
    main_process()

if __name__ == '__main__':
    main()

