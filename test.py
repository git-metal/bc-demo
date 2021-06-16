# -*- coding:utf-8 -*-

import requests
from lxml import etree
import time
import re
from fontTools.ttLib import TTFont


src = '''
<body>
  <div class="tag-addr">
    <a href = "http://www.dianping.com/shenzhen/ch10/g111" data-click-name="shop_tag_cate_click" data-shopid="k4YMr41Zmuul4QWo" ><span class="tag"><svgmtsi class="tagName">&#xe11a;</svgmtsi><svgmtsi class="tagName">&#xf730;</svgmtsi><svgmtsi class="tagName">&#xf1b5;</svgmtsi></span></a>
    <em class="sep">|</em>
    <a href = "http://www.dianping.com/shenzhen/ch10/r88246" data-click-name="shop_tag_region_click" data-shopid="k4YMr41Zmuul4QWo" ><span class="tag"><svgmtsi class="tagName">&#xf74e;</svgmtsi><svgmtsi class="tagName">&#xf3c0;</svgmtsi>/雪象</span></a>
    <span class="addr"><svgmtsi class="address">&#xe69a;</svgmtsi><svgmtsi class="address">&#xe11d;</svgmtsi><svgmtsi class="address">&#xede7;</svgmtsi><svgmtsi class="address">&#xe613;</svgmtsi><svgmtsi class="address">&#xe9f3;</svgmtsi></span>
  </div>

  <div class="recommend"></div>

  <span class="comment-list">
    <span >口味<b><svgmtsi class="shopNum">&#xe413;</svgmtsi>.<svgmtsi class="shopNum">&#xe29f;</svgmtsi><svgmtsi class="shopNum">&#xea06;</svgmtsi></b></span>
    <span >环境<b><svgmtsi class="shopNum">&#xe413;</svgmtsi>.<svgmtsi class="shopNum">&#xe29f;</svgmtsi><svgmtsi class="shopNum">&#xed58;</svgmtsi></b></span>
    <span >服务<b><svgmtsi class="shopNum">&#xe413;</svgmtsi>.<svgmtsi class="shopNum">&#xe29f;</svgmtsi><svgmtsi class="shopNum">&#xeaa1;</svgmtsi></b></span>
  </span>
<body>
'''

def get_xpath(xpath, content):
    """
    xpayh 获取具体字段 或 table
    :param xpath:  xpath语法
    :param content:  页面源代码
    :return: list
    """
    out = []
    tree = etree.HTML(content)
    # tree = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
    results = tree.xpath(xpath)
    for result in results:
        if 'ElementStringResult' in str(type(result)) or 'ElementUnicodeResult' in str(type(result)):
            out.append(result)
        else:
            # out.append(etree.tostring(result))
            # out.append(etree.tostring(result, encoding='utf-8', pretty_print=True, method='html').decode('utf-8'))
            out.append(etree.tostring(result, encoding='utf-8', pretty_print=True, method='html'))
    return out


def test():
    span = get_xpath('//span[@class="comment-list"]', src)
    print("end")
    pass


if __name__ == '__main__':
    print("--------- start -----------")
    try:
        print("xxx")
        test()
    except Exception as e:
        print(e)

