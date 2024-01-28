#用于邮件解码
# import pyzmail
#用于登录
import imapclient

# def GetMail(username,password):
#     #设置imap地址和 端口号
#     imapObj=imapclient.IMAPClient('outlook.office365.com',port=993)
#     #登录 hotmail
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

client = imapclient.IMAPClient('outlook.office365.com',port=993)
client.login('mbgfwocbbo@hotmail.com','uOdVxL889')
client.select_folder('INBOX', readonly=True)
messages = client.search(['FROM','sellersupport@shop.tiktok.com'])
for _sm in messages:
    msgdict = client.fetch(_sm, ['INTERNALDATE','BODY[TEXT]'])  # 获取邮件内容
    # mailbody = msgdict[_sm][b'BODY[]']
    print(msgdict)
    exit(1)
