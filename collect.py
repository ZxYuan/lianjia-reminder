#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2018 zxyuan.me | All Rights Reserved
# 
########################################################################
 
"""
File: collect.py
Author: ZxYuan(lvp0526@gmail.com)
Date: 2018/01/30 00:10:59
"""

import sys
import json

import requests
from bs4 import BeautifulSoup

import conf

to_int = lambda x: int(x) if x.isdigit() else 0

def get_page_count(url):
    r = requests.get(url)
    html_doc = BeautifulSoup(r.text, 'lxml')
    num = to_int(html_doc.find(class_='result-count strong-num').string.strip())
    return ((num - 1) / conf.NUM_ITEMS_PER_PAGE) + 1


def crawl(id):
    data = {}
    url = conf.URL_TPL.format(page=1, id=id)
    for page in xrange(get_page_count(url) + 1):
        url = conf.URL_TPL.format(page=page, id=id)
        r = requests.get(url)
        html_doc = BeautifulSoup(r.text, 'lxml')
        for li in html_doc.find(class_='js_fang_list').find_all('li'):
            href = li.a['href']
            info = ' '.join(li.find(class_='info').get_text().split())
            data[href] = info.encode('utf8')
    return data


def load(id):
    try:
        with open('%s.json' % id, 'r') as fin:
            data = json.load(fin)
    except:
        data = {}
    return data

def dump(id, data):
    with open('%s.json' % id, 'w') as fout:
        json.dump(data, fout, ensure_ascii=False)


def diff(new, old):
    new_keys = set(new.keys())
    old_keys = set(old.keys())
    online_keys = new_keys - old_keys
    offline_keys = old_keys - new_keys
    data_by_keys = lambda keys, data: {k: data[k] for k in keys}
    return data_by_keys(online_keys, new), data_by_keys(offline_keys, old)


if __name__ == '__main__':
    id = sys.argv[1]
    new = crawl(id)
    old = load(id)
    online, offline = diff(new, old)
    dump(id, new)




