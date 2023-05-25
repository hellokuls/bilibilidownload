FROM python:3.7
WORKDIR /app
ADD . .
RUN pip  install -r requirement.txt --index-url http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
EXPOSE 8000
CMD ["python", "manage.py runserver 7000"]