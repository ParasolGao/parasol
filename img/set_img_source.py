import pymysql
import traceback

database = pymysql.connect("localhost","root","a327327","recsys",charset="utf8")
cursor = database.cursor()
book_id = 248
for i in range(247,440):
	src = '../img/'+str(i)+'.jpg'
	print(src)
	sql = "UPDATE `BOOK`\
	SET BOOK_IMG_SRC = '%s'\
	WHERE BOOK_ID = '%d'" %(src,book_id)
	try:
		cursor.execute(sql)
		database.commit()
	except:
		database.rollback()
		traceback.print_exc()
	book_id = book_id + 1