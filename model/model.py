from .mysql_class import mysql_class
class ModelException(Exception):
    def __init__(self,message=''):
        self.message=message
    def __str__(self):
        return self.message
class model:
    def __init__(self,fillable,table):
        self.db = mysql_class()
        self.fillable=fillable
        self.table=table
        self.primary='id'
    def create(self,data):
        return self.db.insert(data,self.table)

    def update(self,data,condition=''):
        return self.db.update(data,condition,self.table)
        pass
    def select(self,colunm='*',condition='',order='',limit=''):
        # print(condition)
        result=[]
        if(colunm=='*'):
            colunm=[self.primary]+self.fillable
        # print(colunm)
        if(type(colunm) == list):
            l =  self.db.select(column=','.join(colunm),condition=condition,db=self.table,order=order,limit=limit)
            for value in l:
                result.append(self.tup_to_dict(colunm, value))
        elif(type(colunm) == str):
            l = self.db.select(column=colunm, condition=condition, db=self.table, order=order, limit=limit)
            for value in l:
                result.append(self.tup_to_dict([colunm], value))
        return result
        pass
    def delete(self,condition=''):
        return self.db.destroy(condition,self.table)
        pass
    def count(self,condition):
        result = self.db.select(column='count(*)',condition=condition,db=self.table)
        print(result)
        if(type(result)==tuple):
            return result[0][0]
        return 0
        pass
    def tup_to_dict(self,key,value):
        if(len(key)!=len(value)):
            raise ModelException('列表和结果长度不一致')
        result={}
        for index in range(len(key)):
            result[key[index]]=value[index]
        return result