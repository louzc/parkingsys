# -*- coding: utf-8 -*- 
# @Time : 2019/11/29 2:48 下午 
# @Author : Lian 
# @Site :  
# @File : errors.py
from flask import render_template

from parkingsys.parkingbp import bp


@bp.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
