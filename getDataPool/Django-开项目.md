# Django-开项目

## 文章开头

写的文档比较简单轻松，是因为每一步我都已经打磨过了，对于我们来说，我们花更多时间在业务上会更好，这只是数据基座，我们后面只需要专注于写业务和爬虫即可。

## 参考文献

上面的文章我参考链接如下：

django链接mysql:https://blog.csdn.net/shiyi1100/article/details/131156608

django项目开端：https://mp.weixin.qq.com/s?__biz=MzI3NDc4NTQ0Nw==&mid=2247537714&idx=1&sn=85819df70d42c1569ab1537429fe77de&chksm=eb0ca1fadc7b28ece9fc1aa347b00b1cceb09cee637d92793f42d756fae7edf6cc4490eae90a&scene=27

django定时器讲解：https://www.likecs.com/show-308327755.html

## 1.安装对应环境；

```powershell
pip install -r requirements
```

<img src="C:\Users\GKYN20230046\Desktop\img\image-20231017093351183.png" alt="image-20231017093351183" style="zoom:47%;" />

## 2.django启动项目

指定目录利用django开项目；

```powershell
django-admin startproject getDataPool
```

执行语句后有如下文件目录：

<img src="C:\Users\GKYN20230046\Desktop\img\image-20231017093531162.png" alt="image-20231017093531162" style="zoom:50%;" />

用Pycharm打开项目，项目结构文件含义如下：

> - **外层的loginweb目录**：是项目的容器，Django不关心它的名字，我 们可以将它重命名为任何我们喜欢的名字
> - **里面的loginweb目录**：它是一个纯python包。我们可以称呼它为项目的名称，不能随意重命名
> - **manage.py** ：它是Django的一个非常重要的工具，通过它可以调用 django shell和数据库等，如：创建app应用程序、创建数据库表、清 空数据、启动项目等操作
> - **settings.py** ：Django 项目的配置文件。包含了项目的默认设置，包 括数据库信息，调试标志以及其他一些工作的变量
> - **urls.py** ：Django 项目的URL路由声明，负责把URL模式映射到应用 程序
> - **wsgi.py**：Web服务器网关接口（Python Web Server Gateway Interface的缩写），Python应用和Web服务器之间的一种接口，可以 看成是一种协议、规范。它是基于Http协议的，不支持WebSoket
> - **asgi.py**：异步网关协议接口，能够处理多种通用的协议类型，包括 HTTP，HTTP2和WebSocket，可以看成ASGI是WSGI的扩展

## 3.django创建应用

我们创建对于django的app，我们可以理解为业务层，也就是实现接口的地方，下面我们实现一个定时任务的应用，这个应用我们专门实现定时任务。



```
 cd .\getDataPool\    #cd到manage.py的路径下

django-admin startapp web_apscheduler  #创建一个web_apscheduler的应用，名字可以自己定义
```

创建后的目录为下面

<img src="C:\Users\GKYN20230046\Desktop\img\image-20231017094233019.png" alt="image-20231017094233019" style="zoom:50%;" />

其中我们只需要知道我们写业务的地方在views.py即可，其余的文件需要涉及到python写数据库，因为兼容性和稳定性不如java，这边不做深入讲解。

## 4.注册app

我们创建了一个app，对于框架来说他是不知道的，我们需要添加到settings.py的**INSTALLED_APPS**中。

![image-20231017100643518](C:\Users\GKYN20230046\Desktop\img\image-20231017100643518.png)

关于setting.py，我们的django项目的很多配置都在里面配置，这里值得一提还有一个重要的点就是数据库驱动和链接也是在这里配置的。

![image-20231017101245339](C:\Users\GKYN20230046\Desktop\img\image-20231017101245339.png)

还能配置日志服务，这里的话因为原理开放的日志不多，他就仅仅讲解了配置的方法，我觉得我们的聚焦点可以放在业务上，没必要放在配置上，配置上我们配置一次即可。

```python
LOG_PATH = BASE_DIR / "logs"

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        # 日志格式
        "standard": {"format": "%(asctime)s [%(levelname)s] %(filename)s::%(funcName)s:%(lineno)d: %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},  # 简单格式
    },
    # 过滤
    "filters": {},
    # 定义具体处理日志的方式
    "handlers": {
        # 默认记录所有日志
        "default": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_PATH / f'system-{time.strftime("%Y-%m-%d")}.log',
            "maxBytes": 1024 * 1024 * 5,  # 文件大小
            "backupCount": 5,  # 备份数
            "formatter": "standard",  # 输出格式
            "encoding": "utf-8",  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_PATH / f'error-{time.strftime("%Y-%m-%d")}.log',
            "maxBytes": 1024 * 1024 * 5,  # 文件大小
            "backupCount": 5,  # 备份数
            "formatter": "standard",  # 输出格式
            "encoding": "utf-8",  # 设置默认编码
        },
        # 控制台输出
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    # 配置用哪几种 handlers 来处理日志
    "loggers": {
        # 类型 为 django 处理所有类型的日志， 默认调用
        "django": {
            "level": "INFO",
            "handlers": ["default", "console"],
            "propagate": False,
        },
        # log 调用时需要当作参数传入
        "log": {
            "level": "INFO",
            "handlers": ["error", "console", "default"],
            "propagate": True,
        },
    },
}
```

配置成中文

![image-20231017101619838](C:\Users\GKYN20230046\Desktop\img\image-20231017101619838.png)

## 5.数据库创建迁移

执行python manage.py migrate以后为如下信息，如果查看数据库，应该能看到定时任务的数据库表

![image-20231017101717923](C:\Users\GKYN20230046\Desktop\img\image-20231017101717923.png)

![image-20231017102055750](C:\Users\GKYN20230046\Desktop\img\image-20231017102055750.png)

## 6.业务逻辑

完成业务写入，并且暴露我们的接口给django。

业务我是直接复制之前的项目的一些我们会用到的代码，然后做了一个简单的json接口。

```python
import time
from datetime import datetime
import requests
from logging import getLogger
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponse
from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events
import json
from urllib import parse
import xml.etree.ElementTree as ET
from datetime import datetime,timedelta
import hashlib
from django_apscheduler.models import DjangoJob,DjangoJobExecutionManager,DjangoJobExecution
logger = getLogger("log")#初始化日志服务
DjangoJob.objects.all().delete()#job数据库清理
DjangoJobExecution.objects.all().delete()#jobExecution数据库清理

# ERROR = 40
# WARNING = 30
# WARN = WARNING
# INFO = 20
# DEBUG = 10
print('初始化定时任务数据库完毕，定时任务清理完毕。')
logger.log(msg='初始化定时任务数据库完毕，定时任务清理完毕。',level=20)

def job_send_record1():
    # 具体要执行的代码

    print('job_send_record 任务运行成功！{}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
# 添加任务1
# 实例化调度器
scheduler = BackgroundScheduler()
logger.info('实例化调度器。')
# 调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")
logger.info('调度器使用DjangoJobStore()。')
@register_job(scheduler,"interval", seconds=180,id='job_send_record')
def job_send_record():
    # 具体要执行的代码
    logger.info('开始执行job_send_record1.')
    logger.info('开始获取当前时间.')
    stime = datetime.now()
    ntime = stime
    logger.info('开始获取当前时间：' +stime.strftime("%Y-%m-%d %H:%M:%S"))
    #stime = stime.replace(minute=stime.minute-)
    stime = stime-timedelta(minutes=10)#时间加减法
    logger.info('传入参数时间：' + stime.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info('在时间:'+stime.strftime("%Y-%m-%d %H:%M:%S")+'---'+ntime.strftime("%Y-%m-%d %H:%M:%S")+'无QL订单数据')
    print('job_send_record1 任务运行成功！{}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
    logger.info('job_send_record1 任务运行成功！{}'.format(time.strftime("%Y-%m-%d %H:%M:%S")))
scheduler.add_job(job_send_record1,'cron', id='job_send_record1', hour=8, minute=30)
# 监控任务——注册定时任务
# 调度器开始运行
logger.info('调度器开始运行.')
scheduler.start()


def testjson(request):
    #用作app注册到django识别内容而已
    data={
    'patient_name': '张三',
    'age': '25',
    'patient_id': '19000347',
    '诊断': '上呼吸道感染',
    }
    return HttpResponse(json.dumps(data), content_type='application/json,charset=utf-8')
def send_record_web(request):
    global logger
    param = str(request.GET.get('ids'))
    result = {'data':[1,2,3]}
    if len(result['data']) > 0:
        logger.log(msg='send_record_web手动发送记录：'+str(result), level=20)
        return HttpResponse(json.dumps({"msg": "操作成功", "code": 200, "data": {}}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8',
                            headers={"Access-Control-Allow-Origin": "http://localhost:8080"})
    else:
        logger.log(msg=str(result)+'返回值主键为-1，不进行发送.',level=30)
        return HttpResponse(json.dumps({"msg": "返回值主键为-1，不进行发送", "code": 200, "data": {}}, ensure_ascii=False),
                            content_type='application/json,charset=utf-8',
                            headers={"Access-Control-Allow-Origin": "http://localhost:8080"})
```

这是业务代码，然后需要在urls.py注册上我们的接口。

```python
from django.contrib import admin
from django.urls import path
from web_apscheduler import views as apscheduler_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('test1/',apscheduler_views.testjson),
]

```



## 7.运行脚本

运行我们的脚本试试。



```powershell
python manage.py runserver 
```

![image-20231017103458531](C:\Users\GKYN20230046\Desktop\img\image-20231017103458531.png)

然后访问http://127.0.0.1:8000/test1 这个接口试试。

![image-20231017103609317](C:\Users\GKYN20230046\Desktop\img\image-20231017103609317.png)

发现成功了，我们的基础环境也就完成搭建了。

定时任务效果：

![image-20231017104258266](C:\Users\GKYN20230046\Desktop\img\image-20231017104258266.png)

