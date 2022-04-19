# -*- coding: utf-8 -*- 
# @Time : 2019/12/1 7:40 下午 
# @Author : Lian 
# @Site :  
# @File : db.py

import sqlite3
import click
import random
from operator import itemgetter
from datetime import datetime
from time import sleep
from faker import Faker
from flask import current_app, g
from flask.cli import with_appcontext
from .tools import fakerProvider


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def db_get_all():
    db = get_db()
    cars = db.execute(
        'SELECT id, car_plate, checkin_time, checkout_time'
        ' FROM cars'
        ' ORDER BY checkin_time'
    ).fetchall()
    return cars


def db_get_car(id):
    car = get_db().execute(
        'SELECT id, car_plate, checkin_time, checkout_time'
        ' FROM cars'
        ' WHERE id = ?',
        (id,)
    ).fetchone()
    return car


def db_get_inlot_car_by_plate(car_plate):
    car = get_db().execute(
        'SELECT id, car_plate, checkin_time, checkout_time'
        ' FROM cars'
        ' WHERE car_plate = ? and checkout_time = ""',
        (car_plate,)
    ).fetchone()
    return car


def db_search(car_plate):
    db = get_db()
    cars = db.execute(
        'SELECT id, car_plate, checkin_time, checkout_time'
        ' FROM cars'
        ' WHERE car_plate like ? COLLATE NOCASE'
        ' ORDER BY checkin_time DESC',
        ('%' + car_plate + '%',)
    ).fetchall()
    return cars


def db_insert(car_plate, checkin_time, checkout_time):
    db = get_db()
    db.execute(
        'INSERT INTO cars (car_plate, checkin_time, checkout_time)'
        ' VALUES (?, ?, ?)',
        (car_plate, checkin_time, checkout_time)
    )
    db.commit()


def db_update(id, car_plate, checkin_time, checkout_time):
    db = get_db()
    db.execute(
        'UPDATE cars SET car_plate = ?, checkin_time = ?, checkout_time=?'
        ' WHERE id = ?',
        (car_plate, checkin_time, checkout_time, id)
    )
    db.commit()


def db_delete(id):
    db = get_db()
    db.execute('DELETE FROM cars WHERE id = ?', (id,))
    db.commit()


def init_db_empty():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_db(display=False, num=20):
    """建表，随机插入指定条数的纪录"""
    CAR_NUM = num
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    cars = []

    for i in range(CAR_NUM):
        f = Faker(locale='zh_CN')
        p = fakerProvider.InsurProvider(f)
        car_plate = p.license_plate()
        in_time = f.past_datetime(start_date="-1d", tzinfo=None)
        out_time = None
        if random.randint(1, 10) > 7:
            out_time = f.past_datetime(start_date="-1d", tzinfo=None)
            while out_time < in_time:
                out_time = f.past_datetime(start_date="-1d", tzinfo=None)

        cars.append((car_plate, in_time, out_time))

    cars.sort(key=itemgetter(1))
    if display:
        print('删除原数据库')
        print('插入' + str(CAR_NUM) + '条新纪录')
        print('---------------------------------------')
        sleep(1)
    for i in range(CAR_NUM):
        car = cars[i]
        checkin_time = str(car[1])
        checkout_time = ''
        if not (car[2] is None):
            checkout_time = str(car[2])
        if display:
            print('车牌号码：', car[0], '入库：', checkin_time, '出库:', checkout_time)
        db.execute('INSERT INTO cars (car_plate, checkin_time, checkout_time) '
                   'VALUES (?, ?, ?)', (car[0], checkin_time, checkout_time))

    db.commit()


@click.command('init-db')
@click.option('--display', default=False, help='是否显示初始化纪录信息')
@click.option('--num', default=20, help='生成纪录的条数')
@with_appcontext
def init_db_command(display, num):
    """Clear the existing data and create new tables."""
    click.echo('数据库初始化...')
    init_db(display, num)
    click.echo('数据库初始化完毕.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
