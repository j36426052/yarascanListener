key = 'EwB4A8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAeRR1RrwnzHkWaYtQorXAcP/SKmtuNW0GdXCGIUHIoApGcDNNRKA3BwBPR1iN8tpJSNqkvFA/WCYvmQKW/MvB6yxjuGtPXe2gSwGJPpM8HxsvrjtB2cLHT7fh92UrRSOLFU3bDN2LumZklfuvDLu1XN/Vj6ROXOScSJmpYKiqXCez8NtuCEodFdD6IrSqxrkK/yEcJqBS7ckyAXMtuHrC91Shc6CkJF9zdnAzLwTUKHhi1KmWAY2ZvZjUSLk00sTRkyvox/6GEUi0dT+dbs6qL8ln+5K2c3hPtsTvfcSKn8Ks06yTo7g0mkUcBauk1amsM8xGEhK2t18x4u5NXZU7G4DZgAACBIeY5wz48ElSAKvMvRJnUTua6vmkxgBcIRvbQjvoZPfWUomEggP7Gt15ydBAN3Nfl1lFaB/24DXA5hlJdL7+SZmIM+WS6cvTfCtc2iD7rS64IdrtQlpeQfpE0Pcum8olsHw5AB7XOBA9ot+rFlhIdSYemqx4lRemq2s32D6Y/bcL9FCeGDFN2tyTo3MeU+GPRqnKyPYrew45MfzefocDZPL0Vtt3TbJPC7vOD8g1jEKOcSMUxtZeedRJORbWCANAYrkdPdGFWzv+gvY7SE1dd9KrEUWZK4AWcMaV2M046s7Gg9PM1W0VswBEI695FCkbogbqiP1U7rvCFOKE/GQIuoQIHzqjuVTApmUg6vCJzqRqjg/3o3pIhYZbTsHjfOsLnfcN/mXwuuJ2tuJ77gsBB6+NZakanyEbyqN/k9cARJZn5/YD9khuIj47Dn8Jxv76hmIlKU/F44X4RGXr1mY5m9ySGOcJ1CuJ1BRGpMa2cLhhIJ808kStKb+tWWyYavjHWzmlgDkr949twTwfU1MRkxKJuemmmy3vPuZxnrSphJ8tezDs8VzzXja5aKrWx7lc0hb1yArKP+Sw8odK0+RtDQsdqcSBVLmkmrnwHNW3F6aOH80iJTa03Iws93ktslZXEFg0wJi54lQDZjhANbGMDckFxG1Fk3JhcTRh7+XnsQT4WOcRJTaRAQxrdz3mgPccyjssdlMJZjGOXuCUUjLSJxL6uufxjv+UGyi2953QcSFkKrKNAe6Mf7nAxU1FyvEIg0dj7w1BMH91sXrSNbTartGT4cC'
import t_minIO
import requests
import json
import os
import base64
import t_pysql
from datetime import datetime

access_token = key

url = 'https://graph.microsoft.com/v1.0/me/mailfolders/inbox/messages'

headers = {
    'Authorization': f'Bearer {access_token}',
}

params = {
    '$top': 100,  # Limit to 100 messages
}

response = requests.get(url, headers=headers, params=params)

#print(response.json())

# 解析回應並印出每封郵件的相關資訊
for message in response.json()['value']:
    print(f"Subject: {message['subject']}")
    print(f"Received: {message['receivedDateTime']}")
    print(f"From: {message['from']['emailAddress']['address']}")
    print(f"Message ID: {message['id']}")

    MessageID = message['id']
    Subject = message['subject']
    # 将接收时间字符串转换为datetime对象
    received_datetime = datetime.strptime(message['receivedDateTime'], "%Y-%m-%dT%H:%M:%SZ")
    # 将datetime对象转换为MySQL支持的日期时间格式
    Received = received_datetime.strftime("%Y-%m-%d %H:%M:%S")
    Sender = message['from']['emailAddress']['address']

    # TODO: 把id抓下來跟資料庫比對
    if t_pysql.check_duplicate_id(MessageID):
        # 假如有在id那就跳過
        continue
    # 假如不在那就加入資料庫並且繼續掃描
    t_pysql.insert_data(MessageID, Subject, Received,Sender)

    # 獲取郵件的附件
    attachment_url = f"https://graph.microsoft.com/v1.0/me/messages/{message['id']}/attachments"
    attachment_response = requests.get(attachment_url, headers=headers)
    attachments = attachment_response.json()['value']

    for attachment in attachments:
        if attachment['@odata.type'] == '#microsoft.graph.fileAttachment':
            # 下載附件
            attachment_content = base64.b64decode(attachment['contentBytes'])
            
            # path = os.path.join('./fileSave', attachment['name'])
            # with open(path, 'wb') as f:
            #     f.write(attachment_content)
            
            # 把附件放到minIO
            t_minIO.uploadFile(attachment_content,attachment['name'])



    print("\n")
