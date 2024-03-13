# 从har中找到 "_resourceType" = "media"的文件, 并下载它
import requests
import json  

with open('bbs.mihoyo.com.har', 'r', encoding='utf-8') as file:
    # 使用json库解析har文件
    har = json.load(file)

    cnt = 1
    for entry in har['log']['entries']:
        # 找到_resourceType为media的文件, 获取其url, 并下载
        if entry['_resourceType'] == 'media':
            url = entry['request']['url']
            print(url)

            f = requests.get(url)
            # filename = url.split('/')[-1]
            filename = 'download/' + str(cnt) + '.mp3'
            cnt += 1
            with open(filename, 'wb') as file:
                file.write(f.content)