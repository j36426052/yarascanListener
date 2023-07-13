import yara
from fastapi import FastAPI, Depends, Body
from starlette.responses import JSONResponse
import uvicorn
import os
import t_minIO

app = FastAPI()

def validate_filename(filename: str = Body(..., embed=True)):
    #if not os.path.exists(filename):
    #    raise ValueError(f"The file {filename} does not exist.")
    return filename

@app.post("/scan")
async def scan(filename: str = Depends(validate_filename)):
    #ontent = await file.read()
    
    # Load your yara rules
    rules = yara.compile(filepath='./yaraRule/rules.yar')

    # 測試的時候讀取本地的地方
    # with open('./'+filename, 'r') as file:
    #     content = file.read()
    # 讀取minIO的資料
    content = t_minIO.loadFile(filename)
    # Scan the file
    matches = rules.match(data=content)

    # Clean up the temporary file
    #os.remove(file.filename)
    t_minIO.deleteFile(filename)
    if matches:
        return JSONResponse(content={"matches": str(matches)}, status_code=200)
    else:
        return JSONResponse(content={"matches": "No matches"}, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8121)