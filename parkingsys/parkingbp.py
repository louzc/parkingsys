# -*- coding: utf-8 -*- 
# @Time : 2019/12/1 7:42 下午 
# @Author : Lian 
# @Site :  
# @File : parkingbp.py
from datetime import datetime
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from parkingsys.parkingFee import cal_parking_fee
from parkingsys.db import (
    db_search, db_insert, db_get_all, db_get_car, db_update, db_delete,
    db_get_inlot_car_by_plate
)

bp = Blueprint('parking', __name__)

from . import errors


class Error(Exception):
    pass


class InputError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def cmp_datetime(a, b):
    a_datetime = datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
    b_datetime = datetime.strptime(b, '%Y-%m-%d %H:%M:%S')

    if a_datetime > b_datetime:
        return -1
    elif a_datetime < b_datetime:
        return 1
    else:
        return 0


def verify_datetime_str(datetime_str):

    try:
        datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def cal_cars_parkingfee(cars):
    for car in cars:
        car["parking_fee"] = ""
        if not ((car["checkout_time"] is None) or str(car["checkout_time"]) == ""):
            car["parking_fee"] = cal_parking_fee(car["checkin_time"], car["checkout_time"])


@bp.route('/')
def index():
    cars = db_get_all()
    return render_template('cars.html', cars=cars)


@bp.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == "POST":
        car_plate = request.form['car_plate']
        if not car_plate:
            flash('请输入车牌号码或车牌号码的部分字符！')
        cars = db_search(car_plate)
        return render_template('cars.html', cars=cars)
    return render_template('cars.html')


@bp.route('/create', methods=('GET', 'POST'))
def create():
    try:
        if request.method == 'POST':
            car_plate = request.form['car_plate']
            checkin_time = request.form['checkin_time']
            try:
                checkout_time = request.form['checkout_time']
            except:
                checkout_time = ''

            if not car_plate:
                raise InputError('car_plate', '请输入车牌信息！')

            if not checkin_time:
                raise InputError('checkin_time', '请输入入场时间！')
            else:
                if not verify_datetime_str(checkin_time):
                    raise InputError('checkin_time', '时间格式错误！')

            if checkout_time and not verify_datetime_str(checkout_time):
                raise InputError('checkout_time', '出场时间格式错误！')

            car = db_get_inlot_car_by_plate(car_plate)
            if car and not car['checkout_time']:
                raise InputError('car_info', '车辆已在库中！')

            db_insert(car_plate, checkin_time, checkout_time)
            return redirect(url_for('parking.index'))

    except InputError as e:
        flash(e.message)

    return render_template('create.html')


def get_car(id):
    car = db_get_car(id)
    if car is None:
        abort(404, "对应编号{0}的车辆未找到。".format(id))

    return car


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    car = get_car(id)

    try:
        if request.method == 'POST':
            car_plate = request.form['car_plate']
            checkin_time = request.form['checkin_time']
            checkout_time = request.form['checkout_time']

            if not car_plate:
                raise InputError('car_plate', '请输入车牌信息！')

            if not checkin_time:
                raise InputError('checkin_time', '请输入入场时间！')
            else:
                if not verify_datetime_str(checkin_time):
                    raise InputError('checkin_time', '入场时间格式错误！')

            if checkout_time and not verify_datetime_str(checkout_time):
                raise InputError('checkout_time', '出场时间格式错误！')

            # if not checkout_time:
            #    raise InputError('checkout_time', '请输入出场时间！')

            if checkout_time and cmp_datetime(checkin_time, checkout_time) < 0:
                raise InputError('time difference error', '出场时间需晚于入场时间！')

            db_update(id, car_plate, checkin_time, checkout_time)
            return redirect(url_for('parking.index'))

    except InputError as e:
        flash(e.message)

    return render_template('update.html', car=car)


@bp.route('/<int:id>/delete', methods=('POST', 'GET'))
def delete(id):
    db_delete(id)
    return redirect(url_for('parking.index'))


@bp.route('/parkingfee')
def parkingfee():
    a = request.args.get('starttime', '')
    b = request.args.get('endtime', '')
    return jsonify(result=cal_parking_fee(a, b))

