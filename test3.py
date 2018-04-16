import base64
import random

import requests

from mySpider.settings import IPPOOL

url = "http://mmbiz.qpic.cn/mmbiz_png/AMsr7u8sNEGP0cSbuAzaYnxwb0Uls5rB2kaXaI1SGpkUOgibxOPey2V5Xl61nW7dfdMoHj1HquyDyRceZtg8YcA/0?wx_fmt=png"

proxy = random.choice(IPPOOL)
# proxies = {'http': 'http://' + proxy['ip']}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3386.1 Safari/537.36',
    "Proxy-Authorization": "Basic %s" % base64.b64encode(proxy['proxy_user_pass'].encode("utf-8")),
}

data = requests.get(url).content

with open("4.jpg",'wb') as f:
    f.write(data)