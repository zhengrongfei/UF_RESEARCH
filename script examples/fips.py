import pymysql
import csv
# 连接 MySQL 数据库
db_config = {
    "host":'ufsummer.mysql.database.azure.com',  # 主机名
    "port":3306,         # 端口号，MySQL默认为3306
    "user":'rongfei',       # 用户名p
    "password":'Qa66394548', # 密码
    "database":'ufsummer'   # 数据库名称

}

connection = pymysql.connect(**db_config)


cursor=connection.cursor()




# 读取CSV文件并插入数据到数据库
csv_file = "Florida_ct.csv"

with open(csv_file, "r") as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header row

    for row in csv_reader:
        insert_query = "INSERT INTO FIPS (Fips) VALUES (%s)"
        values = (row[68],)
        cursor.execute(insert_query, values)

# 提交事务
connection.commit()

# 关闭游标和连接
cursor.close()
connection.close()