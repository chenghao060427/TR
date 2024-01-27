from lxml import etree
from urllib.parse import urljoin
# print(urljoin('https://search.sunbiz.org/Inquiry/CorporationSearch/SearchResults?InquiryType=EntityName&inquiryDirectionType=ForwardList&searchNameOrder=VERACRUZFUTEBOLCLUB%20N110000101410&SearchTerm=VERA%20COPPORATION&entityId=N11000010141&listNameOrder=VERACRUZ806%20L230001325350','/Inquiry/CorporationSearch/SearchResultDetail?inquirytype=EntityName&directionType=ForwardList&searchNameOrder=VERACRUZGROUP%20L230003067520&aggregateId=flal-l23000306752-4a164814-2f19-4f5e-a109-83fb87d12fd9&searchTerm=VERA%20COPPORATION&listNameOrder=VERACRUZGROUP%20L230003067520'))
def get_company_list(source):
    # print(source)
    html = etree.fromstring(source,etree.HTMLParser())
    tr_list = html.xpath('//div[@id="search-results"]/table/tbody/tr')
    tr_list = [etree.tostring(tr) for tr in tr_list]
    href_list = []
    for tr in tr_list:
        tr = etree.fromstring(tr,etree.HTMLParser())
        flag = tr.xpath('//td[@class="small-width"]/text()')[0]
        # print(flag)
        # exit(1)
        if(flag=='Active'):
            href_list.append(tr.xpath('//td[@class="large-width"]/a/@href')[0])
            # print(tr.xpath('//td[@class="large-width"]/a/@href'))
    next_href = html.xpath('//a[contains(text(),"Next List")]/@href')
    return href_list,next_href[0]
# print(result)
def get_company_detail(source):
    html = etree.fromstring(source,etree.HTMLParser())
    name_html = html.xpath('//div[@class="detailSection corporationName"]/p[2]/text()')
    if(name_html):
        name_html=name_html[0]
    else:
        name_html='NONE'
    ein_html = html.xpath('//label[@for="Detail_FeiEinNumber"]/following-sibling::span[1]/text()')
    if(ein_html):
        ein_html=ein_html[0]
    else:
        ein_html='NONE'
    address = " ".join(html.xpath('//span[contains(text(),"Principal Address")]/following-sibling::span[1]/div/text()'))
    return {'name':str(name_html),'ein':str(ein_html),'address':address.replace("\n",'')}