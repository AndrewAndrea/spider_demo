# -*- coding: utf-8 -*-


import requests
import json
import time
import re
from selenium import webdriver



def get_song(x):
    url = "http://songsearch.kugou.com/song_search_v2?callback=jQuery112407470964083509348_1534929985284&keyword={}&" \
          "page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filte" \
          "r=0&_=1534929985286".format(x)
    res = requests.get(url).text
    js = json.loads(res[res.index('(') + 1:-2])
    data = js['data']['lists']
    # print(data, '111111111111111111')
    for i in range(10):
        print(data[i], '-----------------')
        print(str(i + 1) + ">>>" + str(data[i]['FileName']).replace('<em>', '').replace('</em>', ''))
    number = int(input("\n请输入要下载的歌曲序号（输入-1退出程序）: "))
    if number == -1:
        exit()
    else:
        song_data = data[number - 1]
        AlbumID = song_data.get('AlbumID')
        FileHash = song_data.get('ResFileHash')
        file_name = song_data.get('FileName')
        url = f'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={FileHash}&album_id={AlbumID}&dfid=3w04aT3Gbgut0e6MAN2y6uWb&mid=c5895e913353ead095d4539da6974010&platid=4&_={int(time.time() * 1000)}'
        # 获取歌曲信息中的play_url
        hash_content = requests.get(url, verify=False).json()
        print(hash_content, '-11111111111111111111111112222222222222222222222222222222')
        data = hash_content.get('data')

        if data:
            play_url = data.get('play_url', '')
            song_name = data.get('song_name')
            print(f'文件名：{song_name}, 播放地址：{play_url}')
            with open('kugou/' + song_name + ".mp3", "wb")as fp:
                fp.write(requests.get(play_url, verify=False).content)
        # url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19107465224671418371_1555932632517&hash=%s&album_id=%s&_=1555932632518' % (
        # # hash, id)
        # hash_content = requests.get(hash_url)
        # print(hash_content.text, '---')
        # play_url = ''.join(re.findall('"play_url":"(.*?)"', hash_content.text))
        # real_download_url = play_url.replace("\\", "")
        # with open(name + ".mp3", "wb")as fp:
        #     fp.write(requests.get(real_download_url).content)
        # print("歌曲已下载完成！")


if __name__ == '__main__':
    x = input("请输入歌名：")
    get_song(x)


