key = 'EwB4A8l6BAAUAOyDv0l6PcCVu89kmzvqZmkWABkAAWQXMrvFuyw7IceJYhGg4mMVGIvvHQYtAmjy1lf+UJJlNc+58i9CpWIfap3+biQ507mDtntgXOVCoeU+1WO37VbGcEbd6wKogw3lmlISe6tCXd5gIBo6UC7ulYi7stjBesiw2fNbpkfrpQgZ3n5zdefx1PfmiUGoFOJxC6ihtsKKk3Qk9Uzy/0+1j81qjjV2rEQoNbBumtkf7fcvgXsrjrFC5hluq4ETSoGNGVXXqNldp2hSGY/B6H+CWUZg2of+RJ2Ji8W56BAOp1SmtpfNkl6e/PJHxJozenM7jpzxKAYe+7ZXhim/7Ds2BH04GovinC1xklKBk8WFKrifWK1aY4ADZgAACOrqk+ghzPKzSAJYtYF8BbWAFH/B4hldOhKH2uiPK9nPYFxl8nD9aQ3bETpsHYfFHQ0/29DCJp4VJDChFRo/HQThgnTy6DdsPuZjZXWqX4TLL8rKYxnnwHCCwk6qL92mYqYbpK0EEgyGR0cb0EOxQEZ86eLwjuYUdlewCuDE+ju/n03G+y6kH+w22lBFD2BQxZh2e6E/2HdxzH/y1GX9FskdDHTddvZOZiUmY9WLBLNdLfTswDaUkmMQjEPUMhdK9ynGBNjdEDTyguOudInOO90OOjnhkZ3qPb99N9UkRzKmEB8JPogM+/3J6Nh9aaXPH7y/46FW/wkLxCOfKo7zuFHIQmNB5fSRkZqLQvsWg9yyrG2gOCreJsxU2nJTJBZpLgAopFsxP0cUNiSkq3/84P857K5gCNw1ETvY/bqeTn7JDwR+FSwWC4YCfTtStD9R8BHsCU9CWx1siMeN4v0k+JGEYrJOxhn6CoJyhp19dfkv/2iHwif5jGhLiuLgdM+bMgAdXWmOZylurxg27aNB9no2765dh3NTGDupPxHhZIRz9Ekp510MhI6vnCN0gPdFnndvTOTSGN8sDKAYMXbXnRjnJp5zoLHKZfJ7EiZ0xukAKC1+rljZ+6knFnYhZrsliPNONHi6iqbrjKkdoLYwbWL/7kGePPBtssbDUYz9KpZLV7L5CqZS+TELpOc0nN1ik9Gub+8ruH5+iOZbxxA5mrpA1mMwxQgmO7VbaZMDWmFAMGcRFpzNaFdmdhzhBxUTQD3QafnfvTWn9JZ3yuvHZt/vPocC'
import minIO
import requests
import json
import os
import base64

access_token = key

url = 'https://graph.microsoft.com/v1.0/me/mailfolders/inbox/messages'

headers = {
    'Authorization': f'Bearer {access_token}',
}

params = {
    '$top': 100,  # Limit to 100 messages
}

response = requests.get(url, headers=headers, params=params)

# 解析回應並印出每封郵件的相關資訊
for message in response.json()['value']:
    print(f"Subject: {message['subject']}")
    print(f"Received: {message['receivedDateTime']}")
    print(f"From: {message['from']['emailAddress']['address']}")
    print(f"Message ID: {message['id']}")

    # 獲取郵件的附件
    attachment_url = f"https://graph.microsoft.com/v1.0/me/messages/{message['id']}/attachments"
    attachment_response = requests.get(attachment_url, headers=headers)
    attachments = attachment_response.json()['value']

    for attachment in attachments:
        if attachment['@odata.type'] == '#microsoft.graph.fileAttachment':
            # 下載附件
            attachment_content = base64.b64decode(attachment['contentBytes'])
            path = os.path.join('./fileSave', attachment['name'])
            with open(path, 'wb') as f:
               f.write(attachment_content)
            # 把附件放到minIO
            minIO.uploadFIle(path,attachment['name'])



    print("\n")
