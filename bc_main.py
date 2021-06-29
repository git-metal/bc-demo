# -*- coding:utf-8 -*-

from lxml import etree
import time
import re
from fontTools.ttLib import TTFont
import html
from pathlib import Path
import random
import request_utils
import db_util
from bc_bean import ShopInfo


# 初始位置信息，只收集制定区域的
# base_url = 'http://www.dianping.com/shenzhen/ch20/r88246'
# base_country = '中国'
# base_province = '广东'
# base_locality = '深圳'
# base_sub_locality = '龙岗'
# base_street = '岗头/雪象'
# base_category = '购物'
# base_sub_category = ''
# base_table = ''

base_url = 'http://www.dianping.com/nanjing/ch20/r91120'
base_country = '中国'
base_province = '江苏'
base_locality = '南京'
base_sub_locality = '雨花台区'
base_street = '铁心桥/楚翘城'
base_category = '购物'
base_sub_category = ''
base_table = ''

words = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下澩凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'

# 保存的的woff字体
address_woff = {}
shopNum_woff = {}
tagName_woff = {}

# woff url
s3plus_url = ''

# db
db_connection = None


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
    results = tree.xpath(xpath)
    for result in results:
        if 'ElementStringResult' in str(type(result)) or 'ElementUnicodeResult' in str(type(result)):
            out.append(result)
        else:
            out.append(etree.tostring(result))
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


def download_woff_font(url):
    fonts = {}
    response = request_utils.get(url)
    if response.status_code == 200:
        content = response.content.decode()
        font_list = re.findall('@font-face\{(.*?)\}', content)

        # 获取woff下载url
        for font in font_list:
            font_name = get_regex_data('font-family: "PingFangSC-Regular-(.*?)"', font)
            font_path = get_regex_data(',url\("(.*?.woff)"\)', font)
            fonts[font_name] = f'http:{font_path}'
            print(f"font name:{font_name} path:{font_path}")

    # 下载woff文件
    for name, url in fonts.items():
        response = request_utils.get(url)
        if response.status_code == 200:
            with open(f'{name}.woff', 'wb') as f:
                f.write(response.content)
            print(f'download {name}.woff success')


def get_img(name, url):
    img_path = Path('img')
    if not img_path.exists():
        img_path.mkdir()

    file_name = f"img\\{name}.png"
    content = request_utils.download_img(url)
    if content:
        with open(file_name, 'wb') as f:
            f.write(content)


def get_sub_category_urls(save):
    src = ''
    file_name = 'category.html'
    if save:
        src = request_utils.get_html(base_url)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(src)
    else:
        with open(file_name, 'r', encoding='utf-8') as f:
            src = f.read()

    # 获取woff字体的地址
    s3plus_url = get_regex_data('(//s3plus\.meituan\.net/.*?)"', src)
    if save and len(s3plus_url) != 0:
        # 下载woff字体
        download_woff_font(f'http:{s3plus_url}')

    # 解析出分类的url
    url_list = get_xpath('//div[@class="nav-category J_filter_category"]/div/div/div/a', src)
    urls = {}
    for item in url_list:
        name = get_xpath('//text()', item)[0]
        url = str(get_xpath('//a/@href', item)[0])
        urls[name] = url
        print(f'name:{name} url:{url}')
    return urls


def get_shop_list(url, save):
    src = ''
    file_name = 'shop_list.html'
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

    # 如果商铺比较少，可能不会有分页，要单独再处理一次
    if len(li_list) == 0:
        content = get_regex_data('(<div class="content">[\d\D]*?)<div class="sear-result no-result"', src)
        li_list = re.findall('(<li class[\d\D]*?</li>)', content)

    print("---- 商铺信息 ----")
    if len(li_list) <= 2:
        print("没找到商铺信息")
        return

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
    if star_score == '':
        star_score = 0

    # 评论数
    review_html = get_regex_data('<b>(.*?)</b>\s+条评价', src)
    review_str = re.findall('>(.*?)<', review_html)
    review_num = get_woff_string(review_str, woff=shopNum_woff)
    if review_num == '':
        review_num = 0

    # 获取商铺图标
    img_url = get_xpath('//div[@class="pic"]/a/img/@src', src)[0]
    # get_img(shop_name, img_url)

    # 商铺链接
    shop_url = get_xpath('//div[2]/div[1]/a/@href', src)[0]

    print(f'店名:{shop_name} 地址:{address} 纬度:{latlng.get("lat")} 经度:{latlng.get("lng")} tag:{tag} 评分:{star_score} 评论数:{review_num} 图标地址:{img_url} 商铺地址:{shop_url}')

    # 保存到数据库
    shop_info = ShopInfo()
    shop_info.name = shop_name
    shop_info.address = address
    shop_info.lat = latlng.get('lat')
    shop_info.lng = latlng.get('lng')
    shop_info.tag = tag
    shop_info.score = star_score
    shop_info.review_num = review_num
    shop_info.img_url = img_url
    shop_info.shop_url = shop_url
    shop_info.country = base_country
    shop_info.province = base_province
    shop_info.locality = base_locality
    shop_info.sub_locality = base_sub_locality
    shop_info.street = base_street
    shop_info.category = base_category
    shop_info.sub_category = base_sub_category
    db_util.add_record(db_connection, shop_info.get_sql(base_table))


def set_base_info(info):
    global base_url
    global base_country
    global base_province
    global base_locality
    global base_sub_locality
    global base_street
    global base_category
    global base_sub_category
    global base_table
    base_url = info[0]
    base_country = info[1]
    base_province = info[2]
    base_locality = info[3]
    base_sub_locality = info[4]
    base_street = info[5]
    base_category = info[6]
    base_sub_category = info[7]
    base_table = info[8]


def get_data():
    # 获取某一个类目下的所有url
    urls = get_sub_category_urls(True)

    # 加载woff字体，woff文件可能会有更新
    get_woff()

    # 获取数据库连接
    global db_connection
    db_connection = db_util.connect()
    if not db_connection:
        return
    db_util.init_db(db_connection)

    # 测试加载第一个，根据好评排序
    time.sleep(5)
    for name, url in urls.items():
        print(f'获取列表： name:{name} url:{url}o3')
        global base_sub_category
        base_sub_category = name
        get_shop_list(url + 'o3', True)
        # break
        time.sleep(30 + random.randint(10, 30))

    db_util.close(db_connection)


if __name__ == '__main__':
    try:
        # base_info = ['http://www.dianping.com/shenzhen/ch45/r88246', '中国', '广东', '深圳', '龙岗', '岗头/雪象', '运动健身', '', 'sport']
        # base_info = ['http://www.dianping.com/nanjing/ch45/r91120', '中国', '江苏', '南京', '雨花台区', '铁心桥/楚翘城', '运动健身', '', 'sport']

        # base_info = ['http://www.dianping.com/shenzhen/ch65', '中国', '广东', '深圳', '龙岗', '岗头/雪象', '爱车', '', 'car']
        # base_info = ['http://www.dianping.com/nanjing/ch65', '中国', '江苏', '南京', '雨花台区', '铁心桥/楚翘城', '爱车', '', 'car']

        bases = [
            ['http://www.dianping.com/shenzhen/ch85', '中国', '广东', '深圳', '龙岗', '岗头/雪象', '爱车', '', 'medical'],
            ['http://www.dianping.com/nanjing/ch85', '中国', '江苏', '南京', '雨花台区', '铁心桥/楚翘城', '爱车', '', 'medical']
        ]

        for info in bases:
            set_base_info(info)
            get_data()
            time.sleep(10)

        # 测试
        # get_woff()
        # get_shop_list('http://www.dianping.com/nanjing/ch10/g250r91120o3', True)
        # download_woff_font("http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/07cfbc597da8b932f4f1a3361255f809.css")
    except Exception as e:
        print(e)
        pass
