from .model import model

class comany_keyword(model):
    fillable=['value']
    table = 'comany_keywords'

    def __init__(self):
        super().__init__(fillable=self.fillable,table=self.table)

if __name__ == "__main__":
    comany_keyword = comany_keyword()
    print(comany_keyword.count(['value','=','aaa']))
