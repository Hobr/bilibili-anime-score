# -*- coding:utf-8 -*-
# https://github.com/Hobr/bilibili-anime-score

import requests
import json
import sqlite3
import os

url = "https://bangumi.bilibili.com/jsonp/seasoninfo/{0}.ver"

def bilibili_rating(bangumi_id):
    payload = {"callback": "seasonListCallback"}
    response = requests.get(url.format(bangumi_id), params=payload)
    data = json.loads(response.text[19:-2])
    try:

        area = "\"{0}\"".format(data["result"]["area"]) #地区
        cover = "\"{0}\"".format(data["result"]["cover"]) #logo
        danmaku_count = int(data["result"]["danmaku_count"]) #弹幕
        evaluate = "\"{0}\"".format(data["result"]["evaluate"][0:60].replace('\"','')) #介绍
        favorites = int(data["result"]["favorites"]) #追番
        is_finish = int(data["result"]["is_finish"]) #完结
        count = float(data["result"]["media"]["rating"]["score"]) #人数
        score = int(data["result"]["media"]["rating"]["count"]) #分数
        title = "\"{0}\"".format(data["result"]["media"]["title"]) #名称
        play_count = int(data["result"]["play_count"]) #播放量
        season_id = int(data["result"]["season_id"]) #seasonid
        share_url = "\"{0}\"".format(data["result"]["share_url"]) #链接

        print(season_id, title, score, count,area)
        try:
            cursor.execute("insert into bangumi_20171107 values ({0}, {1}, {2}, {3}, {4},{5},{6},{7},{8},{9},{10},{11})"
                           .format(season_id, title, score, count, is_finish,favorites,area,cover,danmaku_count,evaluate,play_count,share_url))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
    except KeyError:
        return None

if os.path.getsize("bilibili_bangumi.db") >= 2: # 数据库已创建
    conn = sqlite3.connect("bilibili_bangumi.db")
    cursor = conn.cursor()
    session = requests.session()
    cursor.execute("select MAX(season_id) from bangumi_20171107")
    lastid = cursor.fetchone()
    print(lastid[0])
    if lastid[0] < 7000 :
        for i in range(lastid[0]+1, 7000):
            bilibili_rating(i)
            print(i)
        for i in range(20000, 23000):
            bilibili_rating(i)
            print(i)

    elif lastid[0] > 7000 and lastid[0] < 23000:
        for i in range(lastid[0]+1, 23000):
            bilibili_rating(i)
            print(i)

    print("Done well")
    cursor.close()
    conn.close()
else: # 数据库未创建
    conn = sqlite3.connect("bilibili_bangumi.db")
    cursor = conn.cursor()
    cursor.execute("create table bangumi_20171107 (season_id int primary key, "
                "title varchar(255), score float, count int, is_finish int, favorites int,area varchar(40), cover varchar(255), danmaku_count int, evaluate varchar(25), playcount int, url varchar(255))")
                #         名称         分数           人数        完结            追番         国家地区            LOGO               弹幕                   介绍               播放量       URL
    session = requests.session()
    for i in range(0, 7000):
        bilibili_rating(i)
        print(i)

    for i in range(20000, 23000):
        bilibili_rating(i)
        print(i)

    print("Done well")
    cursor.close()
    conn.close()
