# -*- coding: utf-8 -*-
import traceback
import os 
import pymysql

database = pymysql.connect("localhost","root","a327327","recsys",charset="utf8")
cursor = database.cursor()
for i in range(1,441):
    src_path = "../img/"+str(i) + ".jpg"
    path = os.path.abspath(src_path)
    print(src_path)
    sql = "UPDATE `BOOK`\
    SET BOOK_IMG_SRC='%s'\
    WHERE BOOK_ID = '%d'" %(src_path,i)
    print(path)
    try:
    	cursor.execute(sql)
    	database.commit()
    except:
     	database.rollback()
     	traceback.print_exc()
    
