# Bilibilidownload

一个简易的下载 B 站视频的 Web 程序，输入 BV 号可获取到视频列表，点击即可进行下载。

在线演示：http://kuls.one:7000/

## 页面截图

![](https://github.com/hellokuls/bilibilidownload/blob/master/static/images/1.png?raw=true)

![](https://github.com/hellokuls/bilibilidownload/blob/master/static/images/2.png?raw=true)

![](https://github.com/hellokuls/bilibilidownload/blob/master/static/images/3.png?raw=true)

## 使用方式

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirement.txt
```

```bash
python manage.py runserver 7000

```

## 技术栈

- Python3
- Django
- layui
- 前后端不分离


## docker 运行

```bash
# 拉取
git clone https://github.com/hellokuls/bilibilidownload.git

# 进入到项目中

docker build  -t bili:v1 .

docker run -d -p 7000:7000 --name bili_docker bili:v1

# 记得防火墙设置端口 7000 开放
```
