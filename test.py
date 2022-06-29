from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import pymysql
app = Flask(__name__)
# 协议：mysql+pymysql
# 用户名：root
# 密码：xuweijian
# IP地址：localhost
# 端口：3306
# 数据库名：aphasia
'''app.config['SECRET_KEY'] = 'xuweijian'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:xuweijian@localhost:3306/aphasia'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
db=SQLAlchemy(app)'''

db=pymysql.connect(host='localhost',user='root',password='xuweijian',database='aphasia')
cursor=db.cursor()
sql="SELECT * FROM USER "
try:
    sursor.execute(sql)
    results=cursor.fetchall()
    for row in results:
        fname=row[0]
        lname=row[1]
        apassword=row[2]
    print(fname,lname,apassword)
except:
    print("Error")
