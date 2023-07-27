# 使用官方的 Python 基礎映像
FROM python:3.11.4

# 設定工作目錄
WORKDIR /app

# 複製當前目錄下的所有檔案到容器的 /app 目錄
COPY ./src /app

# 安裝需要的 Python 套件
RUN pip install commitizen>=3.5.2 minio>=7.1.15 requests>=2.31.0 \
    fastapi>=0.100.0 yara-python>=4.3.1 uvicorn>=0.22.0 httpx>=0.24.1 \
    nats-py>=2.3.1 mysql-connector-python>=8.0.33 msal>=1.22.0

# 在容器啟動時執行 b_yaraScanner.py
CMD ["python", "b_yaraScanner.py"]
