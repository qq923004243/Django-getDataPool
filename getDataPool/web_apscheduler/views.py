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




