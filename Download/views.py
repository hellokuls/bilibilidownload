from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse,JsonResponse
from urllib.parse import quote
import requests, hashlib, urllib.request, re
# 公众号：Python进击者
# Create your views here.


def index(request):

    return render(request, "index.html")


def index2(request):
    return JsonResponse([1,2,3],safe=False)

def getVideoList(request):
    start = request.GET.get("bv")
    start_url = "https://api.bilibili.com/x/player/pagelist?bvid=%s" % start

    # 视频质量
    quality = request.GET.get("quality")
    # 获取视频的cid,title
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    html = requests.get(start_url, headers=headers, timeout=60).json()
    print(html)
    data = html['data']
    # print(data)
    videoList = []
    for item in data:
        cid = str(item['cid'])
        title = item['part']
        title = re.sub(r'[\/\\:*?"<>|]', '', title)  # 替换为空的
        page = item['page']
        start_url1 = "%s/?p=%s" %(start_url, page)

        video_list = get_play_list(request, start_url, cid, quality)

        onevideo = {'title': title, 'video_list': video_list[0], 'page': page, 'start_url': start_url1}
        videoList.append(onevideo)

    return render(request, "videolist.html", {'videoList': videoList})


# 访问API地址
def get_play_list(request, start_url, cid, quality):
    entropy = 'rbMCKn@KuamXWlPMoJGsKcbiJKUfkPF_8dABscJntvqhRSETg'
    appkey, sec = ''.join([chr(ord(i) + 2) for i in entropy[::-1]]).split(':')
    params = 'appkey=%s&cid=%s&otype=json&qn=%s&quality=%s&type=' % (appkey, cid, quality, quality)
    chksum = hashlib.md5(bytes(params + sec, 'utf8')).hexdigest()
    url_api = 'https://interface.bilibili.com/v2/playurl?%s&sign=%s' % (params, chksum)
    headers = {
        'Referer': start_url,  # 注意加上referer
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }
    # print(url_api)
    html = requests.get(url_api, headers=headers, timeout=120).json()
    # print(json.dumps(html))
    video_list = []
    for i in html['durl']:
        video_list.append(i['url'])
    # print(video_list)
    return video_list


#  下载视频
def down_video(request):
    video_download_url = request.POST.get("video_download_url")
    title = request.POST.get("title")
    start_url = request.POST.get("start_url")

    opener = urllib.request.build_opener()
    # 请求头
    opener.addheaders = [
        ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
        ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
        ('Accept', '*/*'),
        ('Accept-Language', 'en-US,en;q=0.5'),
        ('Accept-Encoding', 'gzip, deflate, br'),
        ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
        ('Referer', start_url),  # 注意修改referer,必须要加的!
        ('Origin', 'https://www.bilibili.com'),
        ('Connection', 'keep-alive'),
    ]
    urllib.request.install_opener(opener)
    # 开始下载
    try:
        r = urllib.request.urlopen(url=video_download_url)

        response = StreamingHttpResponse(file_itrator(r), content_type="application/octet-stream",)
        response["Content-Disposition"] = 'attachment; filename={0}; filename*=utf-8''{0}'.format(
            quote(title) + '.flv')
        return response
    except Exception as e:
        print("这里有个错误：", e)
        return HttpResponse("error,请返回重新搜索")


# 每次传输视频流的大小
def file_itrator(f):
    chunk_size = 200000  # 每次读取的片大小
    while True:
        c = f.read(chunk_size)
        if c:
            yield c
        else:
            break
