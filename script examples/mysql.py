import pymysql

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


# 创建表的 SQL 命令
create_table_query = """
CREATE TABLE CarInformation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    Serial VARCHAR(255),
    Brand VARCHAR(255),
    Type VARCHAR(255),
    Color VARCHAR(255),
    Confidence INT,
    Year INT,
    CarLocation TEXT,
    FIPS VARCHAR(255)
);
"""

# 执行创建表的 SQL 命令
#cursor.execute(create_table_query)

# 提交事务
connection.commit()

# 关闭游标和连接
cursor.close()
connection.close()