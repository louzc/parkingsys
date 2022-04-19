# -*- coding: utf-8 -*- 
# @Time : 2019/12/1 7:45 下午 
# @Author : Lian 
# @Site :  
# @File : parkingFee.py
import datetime
import math


# 支持函数-时间运算，获得停车时间（总小时数）
# 停车时间不足一小时，按一小时计算
def cal_parking_hours(starttime, endtime):
    try:
        # 计算入场时间starttime和出场时间endtime之间的时间差
        stime = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S")
        if endtime == '':  # 如果没有出场时间，则取当前时间，用于估算车费
            etime = datetime.datetime.now()
        else:
            etime = datetime.datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S")
        seconds = (etime - stime).seconds  # 一天之内的时差，按秒计算
        days = (etime - stime).days  # 相差的天数
        hours = math.ceil(seconds / 3600) + days * 24
        if hours < 0:
            raise Exception("结束时间早于开始时间", hours)
        return hours  # 总相差时间差
    except:
        return -1  # 如果传入的时间格式不对，则返回-1，代表错误


# 主要业务逻辑-计算停车费用
# 计算规则：
# 1. 每小时10元，不足一小时的部分按照1小时计算
# 2. 超过8小时至24小时之内按8小时计；
# 3. 连续停放超过24小时，超过部分按上述标准重新计算。
def cal_parking_fee(starttime, endtime):
    hours = cal_parking_hours(starttime, endtime)
    if hours >= 0:
        days = math.floor(hours / 24)
        left_hours = hours - days * 24
        if left_hours > 8:
            left_hours = 8
        return days * 80 + left_hours * 10
    else:
        return -1
