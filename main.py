#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-12-29 11:54:40
# @Author  : Yan Chen (cheny.gary@gmail.com)

from webopener import getHtml
import re
import urllib
import json
from functools import reduce


def fdseller(keywords,n):
    sellers = []
    # print(keywords[0])
    for item in keywords:

        seller = set()
        for page in range(0,15*n, 15):  #list start from 0, then add 15 for every page 
            postdata = {
                'q': item,
                'js': '1',
                'ie': 'utf8',
                'uniq': 'shop',
                'sort': 'price-asc',
                's': page

            }
            postdata = urllib.urlencode(postdata)
            taobao = "https://s.taobao.com/search?" + postdata
            #print(taobao)
            try:
                content1 = getHtml(taobao)
                content1 = content1.decode('utf-8', 'ignore')
                content1 = re.findall(
                    r'g_page_config = (.*?);\n', content1, re.S)
                product = json.loads(content1[0])
                productfiles = product['mods']['itemlist']['data']['sellers']
                #print(productfiles)
                for productfile in productfiles:
                    seller.add(productfile['user_id'])

            except Exception as e:
                if hasattr(e, 'code'):
                    print('页面不存在或时间太长.')
                    print('Error code:', e.code)
                #raise e
            finally:
                next
        #print(seller)
        sellers.append(seller)
    # return(sellers)
    return reduce(lambda x, y: x & y, sellers)

if __name__ == "__main__":
    pagen = raw_input("需要查几页")
    pagen = int(pagen)
    keys = []
    for keyword in iter(raw_input,''):
        keys.append(keyword)
    fdsellers = fdseller(keys,pagen)
    for fd in fdsellers:
        print('https://store.taobao.com/shop/view_shop.htm?user_number_id=%s' % fd)
