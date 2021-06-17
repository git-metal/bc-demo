# -*- coding:utf-8 -*-

class ShopInfo:
    name = ''
    address = ''
    lat = None
    lng = None
    tag = ''
    score = None
    review_num = None
    img_url = ''
    shop_url = ''
    country = ''
    province = ''
    locality = ''
    sub_locality = ''
    street = ''
    category = ''
    sub_category = ''

    def get_sql(self):
        return f'insert into food values ("{self.name}", "{self.address}", {self.lat}, {self.lng}, "{self.tag}", ' \
               f'{self.score}, {self.review_num}, "{self.img_url}", "{self.shop_url}", "{self.country}",' \
               f'"{self.province}", "{self.locality}", "{self.sub_locality}", "{self.street}",' \
               f'"{self.category}", "{self.sub_category}");'
