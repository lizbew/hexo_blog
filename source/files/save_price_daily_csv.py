#!/usr/bin/env python
# coding: utf-8

import copy
import datetime
import codecs
import requests

common_headers = headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Referer': 'http://quotes.money.163.com/old/'
}

def query_quote_rank():
    url = 'http://quotes.money.163.com/hs/service/diyrank.php'
    
    headers = copy.copy(common_headers)    

    payload = {
        'host': 'http://quotes.money.163.com/hs/service/diyrank.php',
        'page': 0,
        'query': 'STYPE:EQA',
        'fields': 'SYMBOL,NAME,PRICE,PERCENT,UPDOWN,OPEN,YESTCLOSE,HIGH,LOW,VOLUME,TURNOVER,HS,LB,WB,ZF,PE,MCAP,TCAP,MFSUM,SNAME,CODE',
        'sort': 'PERCENT',
        'order': 'desc',
        'count': 24,
        'type': 'query'
    }
    
    today_date = datetime.date.today().strftime('%Y-%m-%d')
    # quote_date = None
    outfile = codecs.open('%s.csv' % today_date, 'wb', 'utf-8')
    outfile.write(payload['fields'])
    outfile.write('\n')
    
    fields = payload['fields'].split(',')
    
    page = 0
    while True:
        print 'query page', page
        payload['page'] = page
        req_session = requests.session()
        resp = req_session.get(url, headers=headers, params=payload)
        data = resp.json()
        # if quote_date is None:
        #    quote_date = data['time'].split(' ')[0] if 'time' in data else today_date

        for item in data['list']:
            line = ','.join([u'{}'.format(item.get(f)) for f in fields])
            outfile.write(line)
            outfile.write('\n')
    
        page += 1
        if page >= data['pagecount']:
            break
    outfile.close()

query_quote_rank()

