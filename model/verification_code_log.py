from .model import model

class verification_code_log(model):
    fillable=['code_url','type','return_msg','created_at']
    table = 'verification_code_logs'

    def __init__(self):
        super().__init__(fillable=self.fillable,table=self.table)