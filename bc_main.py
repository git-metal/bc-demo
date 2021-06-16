# -*- coding:utf-8 -*-

import requests
from lxml import etree
import time
import re
from fontTools.ttLib import TTFont
import html
from pathlib import Path
import request_utils

# 美食 深圳 龙岗 岗头/雪象
base_url = 'http://www.dianping.com/shenzhen/ch10/r88246'

words = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下澩凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'

# 保存的的woff字体
address_woff = {}
shopNum_woff = {}
tagName_woff = {}


def get_regex_data(regex, buf):
    """
    正则表达式
    :param regex: 正则语法
    :param buf: html源代码
    :return:
    """
    group = re.search(regex, buf)
    if group:
        return group.groups()[0]
    else:
        return ''


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
            out.append(etree.tostring(result))
            # out.append(etree.tostring(result, encoding='utf-8', pretty_print=True, method='html').decode('utf-8'))
            # out.append(etree.tostring(result, encoding='utf-8', pretty_print=True, method='html'))
    return out


# 解析大众点评地图坐标参数(POI)
# 鲲鹏数据 http://www.site-digger.com
def to_base36(value):
    """将10进制整数转换为36进制字符串
    """
    if not isinstance(value, int):
        raise TypeError("expected int, got %s: %r" % (value.__class__.__name__, value))

    if value == 0:
        return "0"

    if value < 0:
        sign = "-"
        value = -value
    else:
        sign = ""

    result = []

    while value:
        value, mod = divmod(value, 36)
        result.append("0123456789abcdefghijklmnopqrstuvwxyz"[mod])

    return sign + "".join(reversed(result))


def decode_latlng(C):
    """解析大众点评POI参数
    """
    digi = 16
    add = 10
    plus = 7
    cha = 36
    I = -1
    H = 0
    B = ''
    J = len(C)
    G = ord(C[-1])
    C = C[:-1]
    J -= 1

    for E in range(J):
        D = int(C[E], cha) - add
        if D >= add:
            D = D - plus
        B += to_base36(D)
        if D > H:
            I = E
            H = D

    A = int(B[:I], digi)
    F = int(B[I + 1:], digi)
    L = (A + F - int(G)) / 2
    K = float(F - L) / 100000
    L = float(L) / 100000
    return {'lat': K, 'lng': L}


def parse_woff(file_name):
    font_data = TTFont(file_name)
    uni_list = font_data.getGlyphOrder()[2:]
    return ['&#x' + uni[3:] for uni in uni_list]


def get_woff():
    address = parse_woff('address.woff')
    shopNum = parse_woff('shopNum.woff')
    tagName = parse_woff('tagName.woff')

    for x in range(len(address)):
        address_woff[address[x]] = words[x]

    for x in range(len(shopNum)):
        shopNum_woff[shopNum[x]] = words[x]

    for x in range(len(tagName)):
        tagName_woff[tagName[x]] = words[x]


def get_woff_string(src, woff):
    ret = ''
    ret.split()
    for item in src:
        if ';' in item:
            codes = item.split(';')
            for code in codes:
                if woff.get(code):
                    ret += woff.get(code)
                else:
                    ret += code
        else:
            ret += item
    return ret


def get_img(name, url):
    img_path = Path('img')
    if not img_path.exists():
        img_path.mkdir()

    file_name = f"img\\{name}.png"
    content = request_utils.download_img(url)
    if content:
        with open(file_name, 'wb') as f:
            f.write(content)


def get_food_urls(save):
    src = ''
    file_name = 'food_home.html'
    if save:
        src = request_utils.get_html(base_url)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(src)
    else:
        with open(file_name, 'r', encoding='utf-8') as f:
            src = f.read()

    # 解析出美食的url
    url_list = get_xpath('//div[@class="nav-category J_filter_category"]/div/div/div/a', src)
    urls = {}
    for item in url_list:
        name = get_xpath('//text()', item)[0]
        url = str(get_xpath('//a/@href', item)[0])
        urls[name] = url
        print(f'name:{name} url:{url}')
    return urls


def get_food_shop_list(url, save):
    src = ''
    file_name = 'food_shop_list.html'
    if save:
        src = request_utils.get_html(url)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(src)
    else:
        with open(file_name, 'r', encoding='utf-8') as f:
            src = f.read()

    # 解析商铺列表
    content = get_regex_data('(<div class="content">[\d\D]*?)<div class="page"', src)
    li_list = re.findall('(<li class[\d\D]*?</li>)', content)

    print("---- 商铺信息 ----")
    for item in li_list[2:]:
        get_shop_info(item)


def get_shop_info(src):
    # 店名
    shop_name = html.unescape(get_regex_data('<h4>(.*?)</h4>', src))

    # 地址
    address = get_xpath('//div[@class="operate J_operate Hide"]/a[2]/@data-address', src)[0]

    # 经纬度
    poi = get_xpath('//div[@class="operate J_operate Hide"]/a[2]/@data-poi', src)[0]
    latlng = decode_latlng(poi)

    # tag
    tag_addr = get_regex_data('(<div class="tag-addr">[\d\D]*?</div>)', src)
    tag_span = re.findall('<span[\d\D]*?</span>', tag_addr)[0]
    tag_str = re.findall('>(.*?)<', tag_span)
    tag = get_woff_string(tag_str, woff=tagName_woff)

    # 评分
    star_score = get_regex_data('star_score_sml">(.*?)</div>', src)

    # 评论数
    review_html = get_regex_data('<b>(.*?)</b>\s+条评价', src)
    review_str = re.findall('>(.*?)<', review_html)
    review_num = get_woff_string(review_str, woff=shopNum_woff)

    # 获取商铺图标
    img_url = get_xpath('//div[@class="pic"]/a/img/@src', src)[0]
    # get_img(shop_name, img_url)

    # 商铺链接
    shop_url = get_xpath('//div[2]/div[1]/a/@href', src)

    print(f'店名:{shop_name} 地址:{address} 纬度:{latlng.get("lat")} 经度:{latlng.get("lng")} tag:{tag} 评分:{star_score} 评论数:{review_num} 图标地址:{img_url} 商铺地址:{shop_url}')
    pass


if __name__ == '__main__':
    try:
        # 加载woff字体，woff文件可能会有更新
        get_woff()

        # 获取某一个类目下的所有url
        urls = get_food_urls(False)

        # 测试加载第一个，根据好评排序
        for name, url in urls.items():
            get_food_shop_list(url + 'o3', False)
            break
    except Exception as e:
        print(e)
        pass

