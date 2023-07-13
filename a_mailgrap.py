# 目前使用暫時產生的key TODO:生出永久的key
key = 'EwB4A8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAUCK7cvI3U7+Nl4Gy2VtYiQB1w5QvODJDXb8ORQAUXphTtMB+1TOa/h1x/FZABSgIvqZOaXZAUZLLqYkgWYWtpPc+5LKXFTdu2LfzeDyAG+CZcMRm1rIJFs6YVe1rE/c2PmDfheVbRSKFATzg20kPRlffhFrok7ftdBNSGfGjutk8kSmOTXCB8uIBz+WF2zZfbvmyEefbdKwtw1gZ47xFLl0UHwXuCg6sZhJmt2opz3NK2uHKQj1ym7+BmWM3HMUazKFZB+9PObftooz1msiW33oQZm/Rkqaudx+zeGEJVJzE663UhG5xvfOC4zSHgl8f87biRr2pnnQdRkVOr7bghsDZgAACFpDUJriIF/kSAJzifr1qIktidETGMOh9XRrQX6pzsU54aaLRqqrr+1EQSQ2EIV49MjQ/Vsyefe3jUI4jE18pNJutMVBbhdvjrV/UtvkhFKJKCbX7vnO+u4g2BmTX3NuSMsBQnwIbRSJabUAosXf9GGiuyxPWmMOYZoynQ9CrJ5QaGNmtpkD4wPFX49rU8dP8qYqWGSNCeHST648h82UR+MRtftoMitdX3NXRHVUOi3SXDS83f4ELnxGjX6Y8cKAqx9mxDh8gcQqeDBG6V6kIeoQgP2qEz8eew3wWuzC163JyiuF9KU+xlUSIvoiVDN2rBgeVlUqSx/skm3ZeZ9FzcH1pQ8J/wLGPitplMBOPraxqRLAv48ch+0UszBDa8AKxxa0mgoep2wHW6WNy4NE88n+bD0n1SwHPPC42PujcUQz4tLvLsG7Sz3D9GWryQ80IDApOUzG5SXdE+Z+Qq+7UQlJn6WopUY2s/iD57UN5EMk2noiFbOeCcayaFpGQzyGuqi7h0bz5YGeQYFX2UjEUZDU2ywmxz7dfktZe7DHK7QVhbjCw3COYUIMWeFWZa1yk7ZTzQPkG+3zUVqxOM4B7gTioXewGSzzVzj8bONXcI8mDOPuugkhch5i0scBDTzsQ0dhuSyf1tgTz8arbxiepmeNiC/prJOmbJBmcZ2EuAplof5/epU8GBnejJXHg0KqmRy5MVeHOTxpUCz2x+tHjNAyI7SIN9mIQQ18HKhdpMXbtG8f4qiZkjHJf107fQqdld1vGhJqKL+JHuBtrZZ3EkbvUIcC'

import t_minIO
import requests
import json
import os
import base64
import t_pysql
from datetime import datetime

# 用graph api把信件發過來
access_token = key
url = 'https://graph.microsoft.com/v1.0/me/mailfolders/inbox/messages'
# access設定認證
headers = {
    'Authorization': f'Bearer {access_token}',
}
# 設定抓取信件的rule
params = {
    '$top': 100,  # Limit to 100 messages
}
# 得到response
response = requests.get(url, headers=headers, params=params)
#print(response.json())

# 解析回應並印出每封郵件的相關資訊
for message in response.json()['value']:
    print(f"Subject: {message['subject']}")
    print(f"Received: {message['receivedDateTime']}")
    print(f"From: {message['from']['emailAddress']['address']}")
    print(f"Message ID: {message['id']}")
    #把信件的值取出
    MessageID = message['id']
    Subject = message['subject']
    # 把時間轉換為datatime
    received_datetime = datetime.strptime(message['receivedDateTime'], "%Y-%m-%dT%H:%M:%SZ")
    # 把datatime換成mysql喜歡的格式
    Received = received_datetime.strftime("%Y-%m-%d %H:%M:%S")
    Sender = message['from']['emailAddress']['address']

    #把id抓下來跟資料庫比對
    if t_pysql.check_duplicate_id(MessageID):
        # 假如有在id那就跳過
        continue
    # 假如不在那就加入資料庫並且繼續掃描
    t_pysql.insert_maildata(MessageID, Subject, Received,Sender)

    # 獲取郵件的附件，一樣使用url去抓，主要用message id 去搞
    attachment_url = f"https://graph.microsoft.com/v1.0/me/messages/{message['id']}/attachments"
    attachment_response = requests.get(attachment_url, headers=headers)
    # 得到attachment的value們，要再進一步拆解
    attachments = attachment_response.json()['value']

    for attachment in attachments:
        if attachment['@odata.type'] == '#microsoft.graph.fileAttachment':
            # 下載附件
            attachment_content = base64.b64decode(attachment['contentBytes'])
            
            #儲存到本地
            # path = os.path.join('./fileSave', attachment['name'])
            # with open(path, 'wb') as f:
            #     f.write(attachment_content)
            
            # 把附件放到minIO
            t_minIO.uploadFile(attachment_content,MessageID+attachment['name'])
            # TODO: 把附件訊息放到sql
            t_pysql.insert_attData(MessageID,attachment['name'],MessageID+attachment['name'])

    print("\n")
