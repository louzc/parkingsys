# -*- coding: utf-8 -*- 
# @Time : 2019/12/1 8:01 下午 
# @Author : Lian 
# @Site :  
# @File : fakerProvider.py
from __future__ import unicode_literals

from faker import Faker
from faker.providers import BaseProvider

localized = True


class InsurProvider(BaseProvider):
    license_plate_provinces = (
        "沪", "沪", "沪", "沪", "沪", "沪", "沪", "沪",
        "沪", "沪", "沪", "沪", "沪", "沪", "沪", "沪",
        "沪", "沪", "沪", "沪", "沪", "沪", "沪", "沪",
        "沪", "沪", "沪", "沪", "沪", "沪", "沪", "沪",
        "沪", "沪", "沪", "沪", "沪", "沪", "沪", "沪",
        "沪", "沪", "沪", "沪", "沪", "沪", "沪", "沪",
        "沪", "沪", "沪", "沪", "沪", "沪", "沪", "沪",
        "沪", "沪", "沪", "沪", "沪", "沪", "沪", "沪",
        "沪", "沪", "沪", "沪", "沪", "沪", "沪", "沪",
        "沪", "沪", "沪", "沪", "沪", "沪", "沪", "沪",
        "沪", "沪", "沪", "沪", "沪", "沪", "沪", "沪",
        "京", "沪", "浙", "苏", "粤", "鲁", "晋", "冀",
        "豫", "川", "渝", "辽", "吉", "黑", "皖", "鄂",
        "津", "贵", "云", "桂", "琼", "青", "新", "藏",
        "蒙", "宁", "甘", "陕", "闽", "赣", "湘"
    )

    license_plate_num = (
        "A", "B", "C", "D", "E", "F", "G", "H",
        "J", "K", "L", "M", "N", "P", "Q", "R",
        "S", "T", "U", "V", "W", "X", "Y", "Z",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"
    )

    def license_plate(self):
        plate = "{0}{1}{2}".format(
            self.random_element(self.license_plate_provinces),
            self.random_uppercase_letter(),
            "".join(self.random_choices(elements=self.license_plate_num, length=5))
        )
        return plate
