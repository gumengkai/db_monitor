import requests
import json
import os
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'db_monitor.settings'

def send_ding_msg(content):
# 请求的URL，WebHook地址
    webhook = settings.DING_WEBHOOK
    is_send_ding_msg = settings.IS_SEND_DING_MSG

#构建请求头部
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
}
#构建请求数据
    message ={

        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {

            "isAtAll": True
        }

    }
#对请求的数据进行json封装
    message_json = json.dumps(message)
    
    if is_send_ding_msg == 1:
#发送请求
        info = requests.post(url=webhook,data=message_json,headers=header) 
#打印返回的结果
        print('钉钉告警发送：{}'.format(info.text))


if __name__=="__main__":
    content = '告警测试'
    send_ding_msg(content)