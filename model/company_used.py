from .model import model

class company_used(model):
    fillable=[
        'name',
        'ein',
        'address'
    ]
    table = 'company_used'

    def __init__(self):
        super().__init__(fillable=self.fillable,table=self.table)