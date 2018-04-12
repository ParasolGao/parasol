# -*- coding:utf8 -*-
import traceback
import pymysql
#import database
import random
from flask_table import Table, Col
import win_unicode_console
win_unicode_console.enable()
class User(object):
    def __init__(self,userid,pwd):
        self.user_id  = userid
        self.username = []
        self.pwd      = pwd
        self.sex      = []
    def login(self):
        database = pymysql.Connect("localhost","root","a327327","recsys")
        cursor = database.cursor()
        sql = "SELECT PWD\
               FROM USER\
               WHERE USER_ID = '%s'" %self.user_id
        try:
            cursor.execute(sql)
            result = cursor.fetchall()

            if(int(result[0][0]) == int(self.pwd)):
                return True
            else:
                return False

        except:
            traceback.print_exc()
            database.rollback()
    
    def create_account(self,user_id,username,pwd,sex):
        temp = user_id
        temp_user = User(user_id,pwd)
        database = pymysql.Connect("localhost","root","a327327","recsys",charset="utf8")
        cursor = database.cursor()
        sql = "SELECT USER_ID\
               FROM USER\
               WHERE USER_ID = '%s'" % temp
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            
            if(len(result) == 0):
                sql_1 = "INSERT INTO USER(USER_ID,USER_NAME,PWD,SEX)\
                         VALUES('%s','%s','%s','%s')" %(temp_user.user_id,temp_user.username,temp_user.pwd,temp_user.sex)
                try:
                    cursor.execute(sql_1)
                    database.commit()
                except:
                    database.rollback()
                    traceback.print_exc()
                return temp_user    
            else:
                print("The user_id has existed!")
                return False
        except:
            database.rollback()
            traceback.print_exc()

    def buy_book(self,bookname):
        database = pymysql.Connect("localhost","root","a327327","recsys",charset="utf8")
        cursor = database.cursor()
        sql = "SELECT BOOK_ID\
               FROM BOOK\
               WHERE BOOK_NAME = '%s'" % (bookname)
        print("self.id %s" % self.user_id)
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except:
            database.rollback()
            traceback.print_exc()

        else:
            if(len(result) == 0):
                print (result)
                return False
            else:
                print("result:%s" %result[0][0])
                sql = "INSERT INTO `ORDER`(USER_ID,BOOK_ID)\
                   VALUES('%d','%d')" % (int(self.user_id),int(result[0][0]))
                try:
                    cursor.execute(sql)
                    database.commit()
                    print("执行完毕")
                except:
                    database.rollback()
                    traceback.print_exc()

    def select_user(self,book_id):
        database = pymysql.Connect("localhost","root","a327327","recsys",charset="utf8")
        cursor = database.cursor()
        print("book_id: %d" % (book_id))
        temp = book_id[0]
        print("temp : %d" %temp)
        sql = "SELECT USER_ID\
        FROM `ORDER`\
        WHERE BOOK_ID = '%s' AND USER_ID != '%d'" %(temp,int(self.user_id))
        try:
            cursor.execute(sql)
            res = cursor.fetchone()
            print("res:%s" %res)
            return res
        except:
            database.rollback()
            traceback.print_exc()

    def print_book(self,user_id,book_id):     
        database = pymysql.Connect("localhost","root","a327327","recsys",charset="utf8")
        cursor = database.cursor()
        sql = "SELECT `BOOK`.BOOK_ID,`BOOK`.BOOK_NAME,`BOOK`.BOOK_SCORE,\
        `BOOK`.BOOK_EVALUATE_PEOPLE,`BOOK`.BOOK_PUBLISHER,`BOOK`.BOOK_IMG_SRC\
        FROM `ORDER`,`BOOK`\
        WHERE `ORDER`.USER_ID = '%d' AND\
        `ORDER`.BOOK_ID != '%d'\
        AND `ORDER`.BOOK_ID = BOOK.BOOK_ID" %(int(user_id[0]),int(book_id[0]))
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            return result
            #for item in result_1:
            #    print(item)
        except:
            database.rollback()
            traceback.print_exc()

    def recommend_based_on_score(self):
        database = pymysql.Connect("localhost","root","a327327","recsys",charset="utf8")
        cursor = database.cursor()
        result = []
        sql = "SELECT BOOK_ID\
        FROM `ORDER`\
        WHERE USER_ID = '%d'\
        ORDER BY BOOK_POINT" % int(self.user_id)
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
            result_1 = self.select_user(result)
            print("user_id: %s" %result_1)
            print("book_id: %s" %result)
            self.print_book(result_1,result)
            return self.print_book(result_1,result)

        except:
            database.rollback()
            traceback.print_exc()




    global user_id_index
    
    def get_user_book(self):
        global user_id_index
        user_id_index = list()
        database = pymysql.Connect("localhost","root","a327327","recsys",charset="utf8")
        cursor = database.cursor()
        result = []
        try:

            for i in range(0,300):
                
                user_id = random.randint(1751,2250)
                user_id_index.append(user_id)
                sql = "SELECT BOOK_ID\
                FROM `ORDER`\
                WHERE USER_ID = '%d'" % user_id
                cursor.execute(sql)
                result.append(cursor.fetchall())
            #print(result)
            return result
        except:
            database.rollback()
            traceback.print_exc()
            
    def select_book_user_buy(self,user_id):
        database = pymysql.Connect("localhost","root","a327327","recsys",charset="utf8")
        cursor = database.cursor()
        sql = "SELECT `BOOK`.BOOK_ID,`BOOK`.BOOK_NAME,`BOOK`.BOOK_SCORE,\
        `BOOK`.BOOK_EVALUATE_PEOPLE,`BOOK`.BOOK_PUBLISHER,`BOOK`.BOOK_IMG_SRC\
        FROM `ORDER`,`BOOK`\
        WHERE `ORDER`.USER_ID = '%d' and `BOOK`.BOOK_ID = `ORDER`.BOOK_ID" %(int(user_id))
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
        except:
            database.rollback()
            traceback.print_exc()  

    def recommend_based_on_simularity(self):
        global user_id_index
        user_id_index = list()
        database = pymysql.Connect("localhost","root","a327327","recsys",charset="utf8")
        cursor = database.cursor()
        result = []
        sql = "SELECT BOOK_ID\
               FROM `ORDER`\
               WHERE USER_ID = '%d'" % int(self.user_id)
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            user_result = self.get_user_book()
            simularity = []
            
            set_1 = set()
            set_2 = set()
            simularity = list()

            for i in range(0,len(user_result)):
                for idx in range(0,len(result)):
                    for j in range(0,len(result[idx])):
                        set_2.add(result[idx][j])

                for j in range(0,len(user_result[i])):
                    for k in range(0,len(user_result[i][j])):
                        #print(user_result[i][j][k])
                        set_1.add(user_result[i][j][k])
                set_result = set_2-set_1
 
                
                simularity.append(1-1.0*len(set_result)/len(set_2))
                set_1.clear()
            max_simularity = simularity[0]
            max_user_id = 0
            for x in range(0,len(simularity)):
                if simularity[x] > max_simularity:
                    max_simularity = simularity[x]
                    max_user_id = user_id_index[x]
            res = self.select_book_user_buy(max_user_id)
            return res
            


            #simularity.sort(reverse=True)
            #print(simularity)
            #simularity.sort(reverse=True)
            #print(len(user_result))
            # for i in range(0,len(user_result)):
            #     for j in range(0,len(user_result[i])):
            #         for k in range(0,len(user_result[i][j])):
            #             #print(user_result[i][j][k])
            #             set_1.add(user_result[i][j][k])

            # for i in range(0,len(result)):
            #     for j in range(0,len(result[i])):
            #         set


            #for i in range(0,len(user_result)):


            # for i in range(0,len(user_result)):
            #     set_1 = set()
            #     set_2 = set()
            #     user_result_tuple = ()
            #     result_tuple = ()
            #     set_result = set()
            #     user_result_tuple = tuple(user_result)
            #     result_tuple = tuple(result)
            #     #for i in range(0,len(user_result_tuple)):
            #        # set_1.add(user_result_tuple[i][0][0])
            #     set_1.add(user_result_tuple)
            #     print(set_1)
            #     #x = len(user_result_tuple)-1
            #     #for k in range(0,len(user_result_tuple[i])):
            #     #    set_1.add(user_result_tuple[i][k][0])
            #     #for i in range(0,len(result_tuple)):
            #     #    set_2.add(result_tuple[i][0])
            #     print('set_1')
            #     print(set_1)
            #     print('set_2')
            #     print(set_2)

            #     set_result = set_1 - set_2
            #     print('set_result')
            #     print(set_result)
            #    # a = len(x) for x in set_result
            #    # b = len(y) for x in set_1
            #     a = len(list(set_result)[0])
            #     b = len(list(set_1)[0])
            #     print('a')
            #     print(a)
            #     print('b')
            #     print(b)
            #     simularity.append(a/b)
            #     i = i+1
            #for i in range(0,len(simularity)):
            #   print(simularity[i])
        except:
            database.rollback()
            traceback.print_exc()
    
    def add_user(self,username,sex):
        database = pymysql.Connect("localhost","root","a327327","recsys",charset="utf8")
        cursor = database.cursor()
        new_user = User(self.user_id,self.pwd)
        new_user_sex = sex
        sql = "INSERT INTO `USER`(USERNAME,PWD,SEX)\
        VALUES('%s','%s','%s')" %(new_user.username,new_user.pwd,new_user_sex)
        try:
            cursor.execute(sql)
            database.commit()
        except:
            database.rollback()
            traceback.print_exc()
    
    def add_book(self,_book_name,_book_img_src,_book_publish_year,_book_publisher,_book_isbn):
        database = pymysql.Connect("localhost","root","a327327","recsys",charset="utf8")
        cursor = database.cursor()
        sql = "INSERT INTO `BOOK`(BOOK_NAME,BOOK_IMG_SRC,BOOK_PUBLISH_YEAR,BOOK_PUBLISHER,BOOK_ISBN)\
        VALUES('%s','%s','%s','%s','%s')" %(_book_name,_book_img_src,_book_publish_year,_book_publisher,_book_isbn)
        try:
            cursor.execute(sql)
            database.commit()
        except:
            database.rollback()
            traceback.print_exc()


        




   