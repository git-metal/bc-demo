# -*- coding:utf-8 -*-

import pymysql

create_table_food = '''
create table if not exists food(
    name varchar(255),
    address varchar(255),
    lat float,
    lng float,
    tag varchar(100),
    score float ,
    review_num int,
    img_url varchar(1000),
    shop_url varchar(1000),
    country varchar(100),
    province varchar(100),
    locality varchar(100),
    sub_locality varchar(100),
    street varchar (100),
    category varchar (100),
    sub_category varchar (100),
    primary key (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''


create_table_entertainment = '''
create table if not exists entertainment(
    name varchar(255),
    address varchar(255),
    lat float,
    lng float,
    tag varchar(100),
    score float ,
    review_num int,
    img_url varchar(1000),
    shop_url varchar(1000),
    country varchar(100),
    province varchar(100),
    locality varchar(100),
    sub_locality varchar(100),
    street varchar (100),
    category varchar (100),
    sub_category varchar (100),
    primary key (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

create_table_shopping = '''
create table if not exists shopping(
    name varchar(255),
    address varchar(255),
    lat float,
    lng float,
    tag varchar(100),
    score float ,
    review_num int,
    img_url varchar(1000),
    shop_url varchar(1000),
    country varchar(100),
    province varchar(100),
    locality varchar(100),
    sub_locality varchar(100),
    street varchar (100),
    category varchar (100),
    sub_category varchar (100),
    primary key (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''


create_table_sport = '''
create table if not exists sport(
    name varchar(255),
    address varchar(255),
    lat float,
    lng float,
    tag varchar(100),
    score float ,
    review_num int,
    img_url varchar(1000),
    shop_url varchar(1000),
    country varchar(100),
    province varchar(100),
    locality varchar(100),
    sub_locality varchar(100),
    street varchar (100),
    category varchar (100),
    sub_category varchar (100),
    primary key (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

create_table_car = '''
create table if not exists car(
    name varchar(255),
    address varchar(255),
    lat float,
    lng float,
    tag varchar(100),
    score float ,
    review_num int,
    img_url varchar(1000),
    shop_url varchar(1000),
    country varchar(100),
    province varchar(100),
    locality varchar(100),
    sub_locality varchar(100),
    street varchar (100),
    category varchar (100),
    sub_category varchar (100),
    primary key (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''


create_table_medical = '''
create table if not exists medical(
    name varchar(255),
    address varchar(255),
    lat float,
    lng float,
    tag varchar(100),
    score float ,
    review_num int,
    img_url varchar(1000),
    shop_url varchar(1000),
    country varchar(100),
    province varchar(100),
    locality varchar(100),
    sub_locality varchar(100),
    street varchar (100),
    category varchar (100),
    sub_category varchar (100),
    primary key (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
 

def connect():
    try:
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             database='bc',
                             cursorclass=pymysql.cursors.DictCursor)
        return db
    except Exception as e:
        print("failed to connect db:" + repr(e))
    return None


def close(db):
    if db:
        db.close()


def init_db(db):
    if not db:
        return
    try:
        with db.cursor() as cursor:
            cursor.execute(create_table_food)
            cursor.execute(create_table_entertainment)
            cursor.execute(create_table_shopping)
            cursor.execute(create_table_sport)
            cursor.execute(create_table_car)
            cursor.execute(create_table_medical)
    except Exception as e:
        print("init db failed" + repr(e))


def add_record(db, sql):
    if not db:
        return
    try:
        print(f"sql: {sql}")
        with db.cursor() as cursor:
            cursor.execute(sql)
            db.commit()
    except Exception as e:
        print("failed to insert db" + repr(e))
        db.rollback()
    pass


# connection = connect()
# init_db(connection)
# add_record(connection, a)
# close(connection)
