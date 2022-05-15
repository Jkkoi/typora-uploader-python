import sys
import requests
from urllib.parse import urlparse


API_URL = "https://example.com/upload.php" # 上传图片的 API
IMG_URL = "https://example.com/img/" # 获取图片 API
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-us",
           "Connection": "keep-alive",
           "Accept-Charset": "GB2312,utf-8;q=0.7,*;q=0.7"}


if sys.argv.__len__() == 1:
    sys.stdout.write("error argv len is 1\n")
    sys.exit()

imageList = sys.argv[1::]
urlList = []

for i in range(imageList.__len__()):
    if(imageList[i].startswith("http")):
        urlObj = urlparse(imageList[i])
        if(urlObj.hostname in urlparse(IMG_URL).hostname):  # 判断是否为已有图片
            urlList.append(imageList[i] + "\n")
            continue
        HEADERS["Referer"] = urlObj.hostname  # 来源限制
        imgWebObj = requests.get(imageList[i], headers=HEADERS)
        files = {"file": (urlObj.path, imgWebObj.content)} # 指定文件名，以便让服务器正确返回拓展名
    else:
        files = {"file": open(imageList[i], "rb")}
    imgUrl = requests.post(API_URL, files=files).text
    if imgUrl.startswith("-1"):
        sys.stdout.write("Some Pic Upload Failed!\n")
        sys.exit()
    urlList.append(IMG_URL + imgUrl + "\n")

sys.stdout.write("Upload Success:\n")
sys.stdout.writelines(urlList)
