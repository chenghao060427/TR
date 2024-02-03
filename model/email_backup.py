from .model import model

class email_backup(model):
    fillable=[
        'email',
        'email_pwd',
        'status'
    ]
    table = 'email_backup'

    def __init__(self):
        super().__init__(fillable=self.fillable,table=self.table)