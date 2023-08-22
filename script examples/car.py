import json
import base64
import pymysql
import os
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tiia.v20190529 import tiia_client, models

# 初始化 Tencent Cloud SDK 客户端
cred = credential.Credential("AKIDY0smhjkkcJsGVcYJOVmz2yurZDkBSZdX", "pdLyfR3Tny8D7xa3MXXVM1b3JNE3oQq9")
httpProfile = HttpProfile()
httpProfile.endpoint = "tiia.tencentcloudapi.com"
clientProfile = ClientProfile()
clientProfile.httpProfile = httpProfile
client = tiia_client.TiiaClient(cred, "ap-beijing", clientProfile)

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_data = base64.b64encode(image_file.read())
        base64_string = base64_data.decode("utf-8")
        return base64_string

def process_images_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(root, file)
             
                base64_image = image_to_base64(image_path)
                print(f"Image: {image_path}\n")

                try:
                    req = models.RecognizeCarRequest()
                    params = {
                        "ImageBase64": base64_image
                    }
                    req.from_json_string(json.dumps(params))
                    resp = client.RecognizeCar(req)
                    cartag_info = resp.CarTags[0]

                    # MySQL database configuration
                    db_config = {
                        "host":'ufsummer.mysql.database.azure.com',
                        "port":3306,
                        "user":'rongfei',
                        "password":'Qa66394548',
                        "database":'ufsummer'
                    }

                    # Establish MySQL database connection
                    db_connection = pymysql.connect(**db_config)
                    cursor = db_connection.cursor()

                    # Prepare the data for insertion
                    serial = cartag_info.Serial
                    brand = cartag_info.Brand
                    car_type = cartag_info.Type
                    color = cartag_info.Color
                    confidence = cartag_info.Confidence
                    fips = file[:11]

                    # Create and execute the SQL query
                    sql_query = "INSERT INTO carinformation(Serial, Brand, Type, Color, Confidence, FIPS) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (serial, brand, car_type, color, confidence, fips)
                    cursor.execute(sql_query, values)

                    # Commit changes to the database
                    db_connection.commit()

                    # Close the cursor and database connection
                    cursor.close()
                    db_connection.close()

                except TencentCloudSDKException as err:
                    print("Tencent Cloud SDK Error:", err)
                except pymysql.connect.Error as db_err:
                    print("MySQL Error:", db_err)

# 替换为您的文件夹路径
folder_path = 'image'
process_images_in_folder(folder_path)