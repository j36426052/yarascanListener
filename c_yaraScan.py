import yara
from fastapi import FastAPI, Depends, Body
from starlette.responses import JSONResponse
import uvicorn
import os
import t_minIO,t_pysql

app = FastAPI()

# TODO:fastAPI規定的，不知道要幹嘛
def validate_filename(filename: str = Body(..., embed=True)):
    #if not os.path.exists(filename):
    #    raise ValueError(f"The file {filename} does not exist.")
    return filename

@app.post("/scan")
async def scan(filename: str = Depends(validate_filename)):
    #讀取yara rule TODO:聽說數量大了會讀取很久
    rules = yara.compile(filepath='./yaraRule/rules.yar')

    # 測試的時候讀取本地的地方
    # with open('./'+filename, 'r') as file:
    #     content = file.read()

    # 讀取minIO的資料
    content = t_minIO.loadFile(filename)

    # 掃描檔案
    matches = rules.match(data=content)
    # 把minIO上面的資料刪掉
    t_minIO.deleteFile(filename)

    # 傳送掃描結果 TODO:把結果儲存到資料庫
    if matches:
        t_pysql.updateIsbad(filename,1)
        for match in matches:
            t_pysql.insert_scanResult(filename,str(match))
        return JSONResponse(content={"matches": str(matches)}, status_code=200)
    else:
        t_pysql.updateIsbad(filename,0)
        return JSONResponse(content={"matches": "No matches"}, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8121)