from minio import Minio
from minio.error import S3Error

# 創建一個客戶端物件，將 endpoint、access_key 和 secret_key 替換為你自己的設定
# client = Minio(
#     "127.0.0.1:9000",
#     access_key="RH6i1YFf0kknX3j7ErL4",
#     secret_key="2VDMfJJ0ju8T5E0vHY1s2vU04S96kWHYsp6ILxmd",
#     secure=False,
# )

bucket_name = "truck"
object_name = "test.txt"
file_path = "test.txt"

def uploadFIle(objectPath,name):
    try:
        client = Minio(
        "127.0.0.1:9000",
        access_key="RH6i1YFf0kknX3j7ErL4",
        secret_key="2VDMfJJ0ju8T5E0vHY1s2vU04S96kWHYsp6ILxmd",
        secure=False,
        )
        # 確保 bucket 存在
        found = client.bucket_exists(bucket_name)
        if not found:
            client.make_bucket(bucket_name)
        else:
            print(f"Bucket '{bucket_name}' already exists")

        # 上傳檔案
        client.fput_object(bucket_name, name, objectPath)
        # 第一個很好想像，第二個是名稱，第三個是本地path
        print(f"File '{name}' is uploaded successfully")
    except S3Error as exc:
        print(f"error occurred: {exc}")

    # destination_path = "destination.txt"
    # try:
    #     # 下載檔案
    #     client.fget_object(bucket_name, object_name, destination_path)
    #     print(f"File '{object_name}' is downloaded successfully")
    # except S3Error as exc:
    #     print(f"error occurred: {exc}")

    # try:
    #     # 刪除檔案
    #     client.remove_object(bucket_name, object_name)
    #     print(f"File '{object_name}' is deleted successfully")
    # except S3Error as exc:
    #     print(f"error occurred: {exc}")