#用于邮件解码
#用于登录
import imapclient
import re
import time
# def GetMail(username,password):
#     #设置imap地址和 端口号
#     imapObj=imapclient.IMAPClient('outlook.office365.com',port=993)
#     #登录 hotmailoutlook指定文件夹
#     imapObj.login(username,password)
#     #打印所有文件夹
#     pprint.pprint(imapObj.list_folders())
#     #搜索邮件 read only  改为false 程序读取邮件后会变成已读
#     select_info=imapObj.select_folder('Inbox', readonly=False)
#     #打印当前收件箱邮件数
#     print('%d messages in INBOX' % select_info[b'EXISTS'])
#     #搜索未读邮件
#     UIDS = imapObj.search('UNSEEN')
#     #如果未读邮件大于1 执行以下操作
#     if len(UIDS)>=1:
#         for UID in UIDS:
#             Rawmessages = imapObj.fetch(UID, [b'BODY[]'])
#             messages = pyzmail.PyzMessage.factory(Rawmessages[UID][b'BODY[]'])
#             #获取邮件抬头
#             emailtitle = messages.get_subject()
#             #打印邮件抬头
#             print(emailtitle)
#             #获取邮件正文
#             emailmessage = messages.text_part.get_payload().decode(messages.text_part.charset)
#             #打印邮件正文
#             print(emailmessage)
#             #如果邮件内容包含 Test 则 返回HELLO
#             if 'Test' in emailmessage:
#                 print('hello')
#                 return 'hello'
#             #否则的话就返回 error
#             else:
#                 print('error')
#                 return 'erro'
def check_account_status(email='',password='',end_time=''):
    client = imapclient.IMAPClient('outlook.office365.com',port=993)
    print(email)
    print(password)
    client.login(email,password)
    folders = client.list_folders()
    # print(folders)
    # exit(11)
    for f in ['Junk','INBOX']:

        client.select_folder(folder=f)

        # messages = client.search(['FROM', 'register@account.tiktok.com'])
        # client.select_folder(folder='Inbox')

        messages = client.search(['FROM','sellersupport@shop.tiktok.com'])
        print(messages)
        messages.reverse()

        current_time = 0
        current_content=''
        for _sm in messages:
            msgdict = client.fetch(_sm, ['INTERNALDATE','ENVELOPE'])  # 获取邮件内容

            # mailbody = msgdict[_sm][b'BODY[]']
            title = str(msgdict[_sm][b'ENVELOPE'].subject)

            if(re.search(r'Your TikTok Shop Application',title)):
                if(re.search('Your TikTok Shop Application was not Successful',title)):
                    return False
                elif(re.search('Your TikTok Shop Application was Successful',title)):
                    return True


    client.logout()
    return None

def email_check(email='',password='',):
    try:
        client = imapclient.IMAPClient('outlook.office365.com',port=993)
        print(email)
        print(password)
        client.login(email,password)
        time.sleep(0.3)
        client.logout()
        return True
    except:
        return False
if __name__ == '__main__':
    print(check_account_status('q2km3zu0n@outlook.com','llas9892',end_time=int(time.time())-36000))
