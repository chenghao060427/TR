#数据库的增删改查操作
import pymysql
import json
class mysql_class(object):
    DB_HOST = '127.0.0.1'
    DB_PORT = 3306
    DB_DATABASE = 'tiktok'
    DB_USERNAME = 'tiktok'
    DB_PASSWORD = '1235789!@#'
    db=None
    __instans = None
    def __new__(cls, *args, **kwargs):
        if(cls.__instans is None):
            cls.__instans = super().__new__(cls)
            return cls.__instans
        else:
            return cls.__instans
    def __init__(self):
        config = json.load(open('.env','r',encoding='utf-8'))
        self.db=pymysql.connect(host=config['DB_HOST'],user=config['DB_USERNAME'],password=config['DB_PASSWORD'],database=config['DB_DATABASE'])
    def __del__(self):
        self.db.close()
    #查询操作
    def select(self,condition='',column='*',db='',order='',limit=''):
        cursor = self.db.cursor()
        sql_string = 'SELECT '+column+' from '+db
        con = self.condition_to_str(condition)
        print(con)
        if(con!=''):
            sql_string += ' WHERE {}'.format(con)
        if(order!=''):
            sql_string+=' order by {}'.format(order)
        if(limit!=''):
            sql_string+=' limit {}'.format(limit)
        print(sql_string)
        # exit()
        cursor.execute(sql_string)
        result = cursor.fetchall()
        self.db.commit()
        return result
    def condition_to_str(self,condition=''):
        if(type(condition)==str):
            return condition
        elif(type(condition)==list):
            con=[]
            if(len(condition)):
                for c in condition:
                    if(type(c)==list):
                        con.append(self.list_to_str(c))
                    elif(type(c)==str):
                        con.append(self.list_to_str(condition))
                        break
            if(len(con)):
                return ' and '.join(con)
            else:
                return ''
        return ''
    def list_to_str(self,l):
        s_list=[]
        if(type(l[len(l)-1])==str):
            l[len(l)-1]='"{}"'.format(l[len(l)-1])
        for v in l:
            if(type(v)==str):
                s_list.append('{}'.format(v))
            elif(type(v)==int):
                s_list.append(str(v))
        return ' '.join(s_list)
    #添加到数据
    def insert(self,data,db):
        cursor = self.db.cursor()
        key_list = data.keys()
        key_string=''
        value_string=''
        for k in key_list:
            key_string=key_string+k+','
            if(type(data[k])== int):
                value_string = value_string + str(data[k]) + ","
            elif(type(data[k])== None):
                value_string = value_string+" NULL,"
            else:
                value_string = value_string + "'" + str(data[k]) + "',"
        sql_string = 'INSERT INTO '+db+' ('+key_string[0:-1]+') VALUES ('+value_string[0:-1]+')'
        # print(sql_string)
        # exit()
        try:
            cursor.execute(sql_string)
            self.db.commit()
            return True
        except Exception as e:
            print(e)
            self.db.rollback()
            return False

    def update(self,data,condition,db):

        cursor = self.db.cursor()
        key_list = data.keys()
        key_string=''
        for k in key_list:
            if(type(data[k])== int):
                key_string = key_string+k+'='+str(data[k]) + ","
            elif(type(data[k])== None):
                key_string = key_string + k + '= NULL ,'
            else:
                key_string=key_string+k+'='+"'"+str(data[k])+"',"

        con=self.condition_to_str(condition)
        if(con!=''):
            sql_string = 'UPDATE ' + db + ' SET ' + key_string[0:-1] + ' WHERE  ' + con
        else:
            sql_string = 'UPDATE ' + db + ' SET ' + key_string[0:-1]
        print(sql_string)
        # return
        try:
            cursor.execute(sql_string)
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False
    def destroy(self,condition,db):
        cursor = self.db.cursor()
        con=self.condition_to_str(condition)
        print(con)
        if(con!=''):
            sql = "DELETE FROM "+db+" WHERE "+con
        else:
            sql = "DELETE FROM "+db
        print(sql)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            self.db.commit()
            return True
        except:
            # 发生错误时回滚
            self.db.rollback()
            return False
    #清空表
    def clear(self,db):
        cursor = self.db.cursor()
        sql = "Truncate table "+db
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            self.db.commit()
            return True
        except:
            # 发生错误时回滚
            self.db.rollback()
            return False