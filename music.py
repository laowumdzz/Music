import json
import os
from io import BytesIO
from urllib.parse import urlparse

import requests as rq

downloads_path = input("请输入下载路径，默认为./music：")
downloads_path = "./music/" if downloads_path == "" else downloads_path
while True:
    print("1.下载歌曲 2.关闭")
    chooise = int(input("请输入数字："))
    if chooise == 2:
        exit()
    print('-----------------------')
    music_name = input("请输入歌曲名称：")
    url = "https://xiaoapi.cn/API/yy_sq.php?msg={}&type=json"
    try:
        result = rq.get(url.format(music_name))
        if result.status_code == 200:
            data = json.loads(result.content)["list"]
            for f in range(len(data)):
                p: dict = data[f]
                for i, j in p.items():
                    if i == 'name':
                        print(f'{f + 1}.名字：', j)
                    else:
                        print('歌手：', j)
                        print('--------')
            download_music = int(input("请输入要下载的歌曲数字："))
            print('-----------------------')
            result = rq.get(
                "https://xiaoapi.cn/API/yy_sq.php?msg={0}&type=json&n={1}".format(music_name, download_music))
            if result.status_code == 200:
                result = json.loads(result.content)
                print(
                    "正在下载:\n名字：{0}\n歌手：{1}\n音质：{2}".format(result["name"], result["singer"],
                                                                     result["quality"]))

                url = result['url']

                file_name = os.path.basename(urlparse(url).path)
                _, ext = os.path.splitext(file_name)
                save_path = f"{downloads_path}{result['name']}{ext}"

                yy_xz = rq.get(url)
                if yy_xz.status_code == 200:
                    with open(save_path, "wb") as file:
                        file.write(yy_xz.content)

                if ext == '.mp3':
                    print('下载成功，路径：{}\n-----------------------'.format(save_path))
                    continue
                from PIL import Image
                from mutagen.flac import FLAC, Picture

                fm_url = result["cover"]
                fm_xz = rq.get(fm_url)
                cover_image = Image.open(BytesIO(fm_xz.content))

                cover_image.save("cover.jpg", "JPEG")

                audio = FLAC(save_path)

                image = open('cover.jpg', 'rb').read()

                cover = Picture()
                cover.type = 3
                cover.mime = 'image/jpeg'
                cover.desc = 'Cover'
                cover.data = image

                audio.clear_pictures()
                audio.add_picture(cover)

                audio.save()
                os.remove('./cover.jpg')
                print('下载成功，路径：{}\n-----------------------'.format(save_path))
    except BaseException as e:
        print("下载错误", str(e))
        print('-----------------------')
