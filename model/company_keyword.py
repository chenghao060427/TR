from .model import model

class company_keyword(model):
    fillable=['value','times']
    table = 'company_keywords'

    def __init__(self):
        super().__init__(fillable=self.fillable,table=self.table)

if __name__ == "__main__":
    comany_keyword = company_keyword()
    print(comany_keyword.count(['value','=','aaa']))
