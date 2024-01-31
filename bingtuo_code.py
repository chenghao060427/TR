import base64,requests
import json



def verification_code_cracking(img_url,type):
    api_post_url = "http://www.bingtop.com/ocr/upload/"
    config = json.load(open('.env','r',encoding='utf-8'))
    with open(img_url,'rb') as pic_file:
        img64=base64.b64encode(pic_file.read())
    params = {
        "username": config['Bingtop_User'],
        "password": config['Bingtop_Pwd'],
        "captchaData": img64,
        "captchaType": type
    }
    response = requests.post(api_post_url, data=params)
    dictdata=json.loads(response.text)
    print(dictdata)

img_url = 'verification_code/3d_2385_457b937e9a7d8ec15f6fe3657eb914dbfc44db65_1.jpg'
verification_code_cracking(img_url=img_url,type=2301)