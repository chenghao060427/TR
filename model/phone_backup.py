from .model import model

class phone_backup(model):
    fillable=[
        'phone',
        'sms_url',
        'status'
    ]
    table = 'phone_backup'

    def __init__(self):
        super().__init__(fillable=self.fillable,table=self.table)