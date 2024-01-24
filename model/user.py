from .model import model

class user(model):
    fillable=['email',
              'email_pwd',
              'backup_email',
              'backup_email_url',
              'realname',
              'pwd',
              'birth',
              'address',
              'ssn',
              'phone',
              'sms_url',
              'comany_name',
              'ein',
              'comnay_addr',
              'browser_account',
              'status',
              'created_at',
              'updated_at'
              ]
    table = 'users'

    def __init__(self):
        super().__init__(fillable=self.fillable,table=self.table)
if __name__ == "__main__":
    m = user()
    print(m.delete(conditon=''))