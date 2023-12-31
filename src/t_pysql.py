import mysql.connector
from yamlReader import getyamlkey

# 建立資料庫連線
def create_connection():
    connection = mysql.connector.connect(
        host="db",
        user=getyamlkey('dbuser'),
        password=getyamlkey('dbpassword'),
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
def insert_maildata(MessageID, Subject, Received,Sender):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO mail (MessageID, Subject, Received,Sender) VALUES (%s, %s, %s, %s)"
    values = (MessageID, Subject, Received,Sender)

    cursor.execute(query, values)
    conn.commit()

    print("Data inserted successfully.")

    cursor.close()
    conn.close()

def insert_attData(MessageID,AttatchmentName,ID):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO attatchment (MessageID,AttatchmentName,ID) VALUES (%s, %s,%s)"
    values = (MessageID,AttatchmentName,ID)

    cursor.execute(query, values)
    conn.commit()

    print("Data inserted successfully.")

    cursor.close()
    conn.close()


# 檢查是否有重複的 ID
def check_duplicate_Attid(id,yara):
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT ID,yara FROM yara_result WHERE ID = %s AND yara = %s"
    cursor.execute(query, (id,yara))

    result = cursor.fetchone()
    if result:
        print("ID already exists.")
        result = True
    else:
        print("ID does not exist.")
        result = False
    # SELECT ID,yara FROM yara_result WHERE ID = %s, yara = %s
    cursor.close()
    conn.close()
    return result

def updateIsbad(id,value):
    conn = create_connection()
    cursor = conn.cursor()

    # 更新isbad
    #update_query = "UPDATE attatchment SET isBad = %s WHERE ID = %s"
    update_query = "UPDATE attatchmentTask SET isBad = %s WHERE ID = %s"
    values = (value, id)
    cursor.execute(update_query, values)
    conn.commit()

    print("Data inserted successfully.")

    cursor.close()
    conn.close()

def insert_scanResult(filename,match):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO yara_result (ID,yara) VALUES (%s, %s)"
    values = (filename,match)

    cursor.execute(query, values)
    conn.commit()

    print("Data inserted successfully.")

    cursor.close()
    conn.close()

def updateTaskStatus(taskID,status):
    conn = create_connection()
    cursor = conn.cursor()

    # 更新isbad
    update_query = "UPDATE task SET status = %s WHERE ID = %s"
    values = (status, taskID)
    cursor.execute(update_query, values)
    conn.commit()

    print("update task"+taskID+" to " + status)

    cursor.close()
    conn.close()

def insert_taskError(taskID,error):
    conn = create_connection()
    cursor = conn.cursor()

    query = "INSERT INTO taskError (taskID,Error) VALUES (%s, %s)"
    values = (taskID,error)

    cursor.execute(query, values)
    conn.commit()

    print("Error log")

    cursor.close()
    conn.close()
