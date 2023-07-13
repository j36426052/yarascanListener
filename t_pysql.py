import mysql.connector

# 建立資料庫連線
def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin_iii",
        database="outlookScan"
    )
    return connection

# 檢查是否有重複的 ID
def check_duplicate_id(id):
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT MessageID FROM mail WHERE MessageID = %s"
    cursor.execute(query, (id,))

    result = cursor.fetchone()
    if result:
        print("ID already exists.")
        result = True
    else:
        print("ID does not exist.")
        result = False

    cursor.close()
    conn.close()
    return result

# 新增資料到資料庫
def insert_data(MessageID, Subject, Received,Sender):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO mail (MessageID, Subject, Received,Sender) VALUES (%s, %s, %s, %s)"
    values = (MessageID, Subject, Received,Sender)

    cursor.execute(query, values)
    conn.commit()

    print("Data inserted successfully.")

    cursor.close()
    conn.close()