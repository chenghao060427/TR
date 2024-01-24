from lxml import etree
html = etree.parse('./company.html',etree.HTMLParser())
result =  html.xpath('//input[@placeholder="Enter the business name"]/@class')
print(result)
'XX'
'XXXXXXX' 'Street address'