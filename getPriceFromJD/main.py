# encoding=utf-8

import requests
import json
import lxml
from bs4 import BeautifulSoup

# url & info
goods_info = [
    {"name": "微星 X470 GAMING PLUS", "id": "7052266"},
    {"name": "AMD 2700X 8核16线程 AM4", "id": "6902456"},
    {"name": "Surface Pro i5 8G内存 128G存储", "id": "5537833"}
]

for good_info in goods_info:
    r = requests.get("https://p.3.cn/prices/mgets?skuIds=J_" + str(good_info['id']))
    r = str(r.text)[1:-2]
    data = json.loads(r, encoding='utf-8')
    p = float(data['p'])
    plus_p = -1.0
    try:
        plus_p = float(data['tpp'])
    except:
        pass
    finally:
        final_p = 0
        if 0 <= plus_p < p:
            final_p = plus_p
        else:
            final_p = p
        print(good_info['name']+"\t"+str(final_p))
