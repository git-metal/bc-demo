# -*- coding:utf-8 -*-

import requests
from lxml import etree
import time
import re
from fontTools.ttLib import TTFont


session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}

words = '1234567890店中美家馆小车大市公酒行国品发电金心业商司超生装园场食有新限天面工服海华水房饰城乐汽香部利子老艺花专东肉菜学福饭人百餐茶务通味所山区门药银农龙停尚安广鑫一容动南具源兴鲜记时机烤文康信果阳理锅宝达地儿衣特产西批坊州牛佳化五米修爱北养卖建材三会鸡室红站德王光名丽油院堂烧江社合星货型村自科快便日民营和活童明器烟育宾精屋经居庄石顺林尔县手厅销用好客火雅盛体旅之鞋辣作粉包楼校鱼平彩上吧保永万物教吃设医正造丰健点汤网庆技斯洗料配汇木缘加麻联卫川泰色世方寓风幼羊烫来高厂兰阿贝皮全女拉成云维贸道术运都口博河瑞宏京际路祥青镇厨培力惠连马鸿钢训影甲助窗布富牌头四多妆吉苑沙恒隆春干饼氏里二管诚制售嘉长轩杂副清计黄讯太鸭号街交与叉附近层旁对巷栋环省桥湖段乡厦府铺内侧元购前幢滨处向座下澩凤港开关景泉塘放昌线湾政步宁解白田町溪十八古双胜本单同九迎第台玉锦底后七斜期武岭松角纪朝峰六振珠局岗洲横边济井办汉代临弄团外塔杨铁浦字年岛陵原梅进荣友虹央桂沿事津凯莲丁秀柳集紫旗张谷的是不了很还个也这我就在以可到错没去过感次要比觉看得说常真们但最喜哈么别位能较境非为欢然他挺着价那意种想出员两推做排实分间甜度起满给热完格荐喝等其再几只现朋候样直而买于般豆量选奶打每评少算又因情找些份置适什蛋师气你姐棒试总定啊足级整带虾如态且尝主话强当更板知己无酸让入啦式笑赞片酱差像提队走嫩才刚午接重串回晚微周值费性桌拍跟块调糕'


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


def load_url(url):
    # response = session.get(url, headers=headers)
    # with open('test.html', 'w', encoding='utf-8') as f:
    #     f.write(response.text)
    # return response.text
    with open('test.html', 'r', encoding='utf-8') as f:
        html = f.read()
    return html


def save_fond_css_url(url):
    with open("css_url.txt", 'a', encoding='utf-8') as f:
        f.write(url + '\n')


def download_woff(url):
    print(f"css_url:{url}")
    response = requests.get(url, headers=headers).content.decode()
    font_face_list = re.findall('@font-face\{(.*?)\}', response)
    fonts = {}
    for font_face in font_face_list:
        font_family = get_regex_data('font-family: "PingFangSC-Regular-(.*?)"', font_face)
        font_url = get_regex_data(',url\("(.*?.woff)"\);', font_face)
        print(f'font_family:{font_family} font_url:{font_url}')
        # 下载woff
        # woff = requests.get('http:' + font_url, headers=headers).content
        # with open(f'{font_family}.woff', 'wb') as f:
        #     f.write(woff)


def read_woff(file):
    real_list = {}

    # 打开本地字体文件
    font_data = TTFont(f'{file}.woff')
    # font_data.saveXML('shopNum.xml')
    # 获取全部编码，前2个非有用字符去掉
    uni_list = font_data.getGlyphOrder()[2:]
    # 请求数据中是 "" 对应 编码中为"uniF8A1",我们进行替换，以请求数据为准
    real_list[file] = ['&#x' + uni[3:] for uni in uni_list]
    return real_list

def crawl_data(url):
    html = load_url(url)

    # 获取字体样式路径
    css_url = get_regex_data('(//s3plus\.meituan\.net/.*?)"', html)
    if len(css_url) == 0:
        print("css url is empty")
        return
    save_fond_css_url(css_url)
    download_woff("http:" + str(css_url).strip())

    # 加载woff字体
    shopNum_woff = read_woff('shopNum')
    tagName_woff = read_woff('tagName')
    address_woff = read_woff('address')

    shopNum_word = []
    for x in range(len(shopNum_woff['shopNum'])):
        word_dict = {}
        word_dict['msg'] = words[x]
        word_dict['name'] = shopNum_woff['shopNum'][x]
        shopNum_word.append(word_dict)

    tagName_word = []
    for x in range(len(tagName_woff['tagName'])):
        word_dict = {}
        word_dict['msg'] = words[x]
        word_dict['name'] = tagName_woff['tagName'][x]
        tagName_word.append(word_dict)

    address_word = []
    for x in range(len(address_woff['address'])):
        word_dict = {}
        word_dict['msg'] = words[x]
        word_dict['name'] = address_woff['address'][x]
        address_word.append(word_dict)

    # 获取商铺列表
    data = get_regex_data('(<div class="content">[\d\D]*?)<div class="page"', html)
    table_list = re.findall('(<li class[\d\D]*?</li>)', data)

    # 解析商铺信息
    count = 1
    for tl in table_list:
        if count <= 2:
            count += 1
            continue
        # 店名
        title = get_regex_data('<h4>(.*?)</h4>', tl)
        print(title)
        #  打分
        star_score = get_regex_data('<div class="star_score score_45  star_score_sml">(.*?)</div>', tl)
        print(star_score)
        comment_msg = get_regex_data('<b>(.*?)</b>\s+条评价', tl)
        comments = ''  # 评论数
        comments_list = re.findall('(&#.*?);', comment_msg)
        for cl in comments_list:
            for ix in shopNum_word:
                if ix['name'] == cl:
                    comments += str(ix['msg'])
                    break
        print('评论', comments)

        per_capita_msg = get_regex_data('人均\s+<b>(.*?)</b>', tl)
        per_capita = get_regex_data('(.*?)<svgmtsi', per_capita_msg)  # 人均
        per_list = re.findall('>(.*?)<', per_capita_msg)
        for pl in per_list:
            if ';' in pl:
                for ix in shopNum_word:
                    if ix['name'] == pl[0:-1]:
                        per_capita += str(ix['msg'])
                        break
            else:
                per_capita += str(pl)
        print('人均', per_capita)

        cuisine_msg = get_regex_data('data-click-name="shop_tag_cate_click".*?>(.*?</span>)', tl)
        cuisine = get_regex_data('<span class="tag">(.*?)<svgmtsi', cuisine_msg)  # 菜系
        cuisine_list = re.findall('>(.*?)<', cuisine_msg)
        for cm in cuisine_list:
            if ';' in cm:
                for ix in tagName_word:
                    if ix['name'] == cm[0:-1]:
                        cuisine += str(ix['msg'])
                        break
            else:
                cuisine += str(cm)
        print('菜系', cuisine)

        region_msg = get_regex_data('data-click-name="shop_tag_region_click".*?>(.*?</span>)', tl)
        # 地区
        region = get_regex_data('<span class="tag">(.*?)<svgmtsi', region_msg)
        region_list = re.findall('>(.*?)<', region_msg)
        for rel in region_list:
            if ';' in rel:
                for ix in tagName_word:
                    if ix['name'] == rel[0:-1]:
                        region += str(ix['msg'])
                        break
            else:
                region += str(rel)
        print('地区', region)

        addr_msg = get_regex_data('(<span class="addr">.*?</span>)', tl)
        addr = get_regex_data('<span class="addr">(.*?)<svgmtsi', addr_msg)
        addr_list = re.findall('>(.*?)<', addr_msg)
        for al in addr_list:
            if ';' in al:
                for ix in address_word:
                    if ix['name'] == al[0:-1]:
                        addr += str(ix['msg'])
                        break
            else:
                addr += str(al)
        print('地址', addr)

        taste_msg = get_regex_data('口味(<b>.*?</b>)', tl)
        # 口味
        taste = ''
        taste_list = re.findall('>(.*?)<', taste_msg)
        for tal in taste_list:
            if ';' in tal:
                for ix in shopNum_word:
                    if ix['name'] == tal[0:-1]:
                        taste += str(ix['msg'])
                        break
            else:
                taste += str(tal)
        print('口味', taste)

        environment_msg = get_regex_data('环境(<b>.*?</b>)', tl)
        # 环境
        environment = ''
        environment_list = re.findall('>(.*?)<', environment_msg)
        for el in environment_list:
            if ';' in el:
                for ix in shopNum_word:
                    if ix['name'] == el[0:-1]:
                        environment += str(ix['msg'])
                        break
            else:
                environment += str(el)
        print('环境', taste)

        service_msg = get_regex_data('服务(<b>.*?</b>)', tl)
        # 服务
        service = ''
        service_list = re.findall('>(.*?)<', service_msg)
        for sl in service_list:
            if ';' in sl:
                for ix in shopNum_word:
                    if ix['name'] == sl[0:-1]:
                        service += str(ix['msg'])
                        break
            else:
                service += str(sl)
        print('服务', service)

    print("--------- end -----------")


if __name__ == '__main__':
    print("--------- start -----------")
    try:
        # 龙岗 岗头/雪象
        # crawl_data("http://www.dianping.com/shenzhen/ch10/r88246")
        crawl_data("http://www.dianping.com/guangzhou/ch10/r13892")
    except Exception as e:
        print(e)

