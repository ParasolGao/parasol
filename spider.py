import re
import urllib
import pymysql

database = pymysql.Connect("localhost","root","a327327","recsys",charset="utf8")
cursor = database.cursor()
img_list = list()
for book_id in range(1751,2250):
	sql = "SELECT BOOK_IMG_SOURCE\
	FROM `BOOK`\
	WHERE BOOK_ID='%d'" % (book_id)
	try:
		cursor.execute(sql)
		img_list.append(cursor.fetchone())
	except:
		database.rollback()
x = 0
for img_url in img_list:
	print(img_url[0])
	#urllib.urlretrieve(img_url,'%s.jpg' x)
	#x = x + 1
