
# 网址: https://waimai.meituan.com/customer/order/list

import requests
from lxml import etree
import json


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

def catgory(url, select_num):
    response = requests.get(url, headers=HEADERS)

    text = response.text

    html = etree.HTML(text)

    if select_num == '1':
        items = html.xpath('//*[@class="game-list-item"]//a//@report')

        all_sum = 0

        for item in items:
            item_dict = json.loads(item)
            all_sum = all_sum + spider_h(item_dict['game_id'])

        print('%.2f万人' % all_sum)
    else:
        items = html.xpath('//*[@class="layout-Classify-item"]//a/@href')

        all_sum = 0

        for item in items:
            if item:
                all_sum = all_sum + spider_d(item)

        print('%d人' % all_sum)



def spider_d(url):
    ture_url = 'https://www.douyu.com' + url
    response_new = requests.get(ture_url, headers=HEADERS)
    text_new = response_new.text
    # print(ture_url)
    html_new = etree.HTML(text_new)
    items_new = html_new.xpath('//*[@class="layout-Cover-item"]/div/a/div/div/span/text()')
    # print(items_new)
    sum = 0
    if items_new:
        for i, item_new in enumerate(items_new):
            if i % 2 != 0:
                # print(item_new)
                if '万' in item_new:
                    sum = sum + int(float(item_new[:-1])*10000)
                else:
                    sum = sum + int(item_new)

    return sum


def spider_h(url):
    ture_url = 'https://www.huya.com/g' + '/' + url
    response_new = requests.get(ture_url, headers=HEADERS)
    text_new = response_new.text
    html_new = etree.HTML(text_new)
    items_new = html_new.xpath('//*[@class="game-live-item"]/span/span[2]/i[2]/text()')
    # print(items_new)
    sum = 0
    if items_new:
        for item_new in items_new:
            if item_new[:-1]:
                sum = sum + float(item_new[:-1])

    return sum


if __name__ == '__main__':
    select_num = input('请你选择平台信息: 1.虎牙  2.斗鱼\n')
    if select_num == '1':
        url = 'https://www.huya.com/g'
        catgory(url, select_num)
    else:
        url = 'https://www.douyu.com/directory'
        catgory(url, select_num)

