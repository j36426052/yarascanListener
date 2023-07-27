import httpx
import asyncio
from nats.aio.client import Client as NATS
import json
import yara
import t_minIO,t_pysql

# 網路上的pypl名稱是舊的
# pip install nats-py

async def run():
    # 連線到Nats
    nc = NATS()
    await nc.connect("nats:4222",name="python-connection")
    #print('connect down, waiting for message')

    #接收到資料之後要做什麼
    async def message_handler(msg):
        #把資料取出來
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received a message on '{subject}': {data}")
        # 取出filename
        #print(type(data))
        data_dict = json.loads(data)
        #print(data_dict['Key'][6:])
        filename = data_dict['Key'][6:]

        # 把filename 傳到下面的掃描參數
        #response = httpx.post('http://localhost:8121/scan', json={'filename': filename})
        scan(filename)
        #print(f"Response from FastAPI service: {response.json()}")

    # 訂閱我們要聽的頻道，這一步要人命
    await nc.subscribe("bucketevents", cb=message_handler)
    print('subscribe')

def scan(filename: str):
    #讀取yara rule
    rules = yara.compile(filepath='./rules/index.yar')

    # 讀取minIO的資料
    content = t_minIO.loadFile(filename)

    # 掃描檔案
    matches = rules.match(data=content)
    # 把minIO上面的資料刪掉
    t_minIO.deleteFile(filename)

    # 傳送掃描結果 把結果儲存到資料庫
    if matches:
        t_pysql.updateIsbad(filename,1)
        for match in matches:
            t_pysql.insert_scanResult(filename,str(match))
    else:
        t_pysql.updateIsbad(filename,0)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.run_forever()
    loop.close()