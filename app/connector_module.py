import mysql.connector
import datetime as dt
import netifaces as ni
import os

os_name = os.name
ni_interface = ni.interfaces()
print(ni_interface)
if os_name == 'posix':
    host = ni.ifaddresses('eth0')[2][0]['addr']
elif os_name == 'nt':
    host = ni.ifaddresses(ni_interface[6])[2][0]['addr']


connect_data = {
    'host': 'localhost', # host #192.168.10.68 (this will change whenever you log into different connection)
    'user': 'newuser',
    'passwd': 'password',
    'database': 'dahshboard_demo'
}
cnx = None

def get_connection():
    global cnx  # 將連線物件存放在全域變數
    if not cnx:
        cnx = mysql.connector.connect(**connect_data)
        return cnx
    else:
        return cnx

def get_cursor():
    cursor = get_connection().cursor(dictionary=True)  # 讀出資料使用 dict，預設為 tuple
    return (cursor, get_connection())  # 同時回傳 cursor 和 connection



def update_example_table(data):
    connection = mysql.connector.connect(**connect_data)
    cursor = connection.cursor()
    
    for _, row in data.iterrows(): 
        try:
            sql = f"UPDATE `example` SET `col_0`= {row['col_0']},`col_1`={row['col_1']},`col_2`={row['col_2']} WHERE `event_date`='{row['event_date']}'"
            cursor.execute(sql)
            connection.commit()
        except Exception as e:
            print(e)
            raise Exception


def create_and_delete_example_table(data):
    connection = mysql.connector.connect(**connect_data)
    cursor = connection.cursor()
    sql = "INSERT INTO `example` (`event_date`, `col_0`, `col_1`, `col_2`) VALUES (%s, %s, %s, %s)"

    for i in range(len(data)):
        sql_delete = "DELETE FROM `example` WHERE event_date = '{}'".format(str(data.iloc[i].values[0]))
        cursor.execute(sql_delete)
        connection.commit()
        cursor.execute(sql, tuple(data.iloc[i].values))
        connection.commit()

    
def delete_selected_row(data):
    connection = mysql.connector.connect(**connect_data)
    cursor = connection.cursor()
    sql_delete = "DELETE FROM `example` WHERE event_date = '{}'".format(str(data))
    cursor.execute(sql_delete)
    connection.commit()
    
    # close connection
    if connection.is_connected():
        connection.close()