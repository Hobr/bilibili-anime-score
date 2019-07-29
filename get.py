# -*- coding:utf-8 -*-
# https://github.com/Hobr/bilibili-anime-score

import requests
import json
import sqlite3
import os

apiurl = "https://www.biliplus.com/api/bangumi?season={0}"

def bilibili_rating(bangumi_id):
    response = requests.get(apiurl.format(bangumi_id))
    data = json.loads(response.text)
    if int(data["code"]) == 10:
        pass
    else:    
        area = "\"{0}\"".format(data["result"]["area"]) # 地区
        danmaku_count = int(data["result"]["danmaku_count"]) # 弹幕
        favorites = int(data["result"]["favorites"]) # 追番
        is_finish = int(data["result"]["is_finish"]) # 完结
        count = int(data["result"]["media"]["rating"]["count"]) # 人数
        score = float(data["result"]["media"]["rating"]["score"]) # 分数
        title = "\"{0}\"".format(data["result"]["media"]["title"]) # 名称
        play_count = int(data["result"]["play_count"]) # 播放量
        season_id = int(data["result"]["season_id"]) # seasonid
        print(season_id, title, score, count,area)
        try:
            cursor.execute("insert into bangumi values ({0}, {1}, {2}, {3}, {4},{5},{6},{7},{8})"
                           .format(season_id, title, score, count, is_finish,favorites,area,danmaku_count,play_count))
            conn.commit()
        except sqlite3.IntegrityError:
            pass

if os.path.getsize("bilibili_bangumi.db") >= 2: # 数据库已创建
    conn = sqlite3.connect("bilibili_bangumi.db")
    cursor = conn.cursor()
    session = requests.session()
    cursor.execute("select MAX(season_id) from bangumi")
    lid = cursor.fetchone()
    
    try:
        lastid = int(lid[0])
    except TypeError:
        lastid = 0

    print(lastid)
    if lastid < 7000 :
        for i in range(lastid+1, 7000):
            bilibili_rating(i)
            print(i)
        for i in range(20000, 23000):
            bilibili_rating(i)
            print(i)

    elif lastid > 7000 and lastid < 23000:
        for i in range(lastid+1, 23000):
            bilibili_rating(i)
            print(i)

    print("Done well")
    cursor.close()
    conn.close()
else: # 数据库未创建
    conn = sqlite3.connect("bilibili_bangumi.db")
    cursor = conn.cursor()
    cursor.execute("create table bangumi (season_id int primary key, "
                "title varchar(255), score float, count int, is_finish int, favorites int,area varchar(40), danmaku_count int, playcount int)")
                #         名称         分数           人数        完结            追番         国家地区              弹幕                播放量
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
