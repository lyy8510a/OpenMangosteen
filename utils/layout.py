#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/8/24 下午5:10.
"""

import time
from flask import render_template,request,jsonify #第五课增加内容


def layout(template_name_or_list,**context): #第五课增加内容
    return render_template(template_name_or_list,
                           tag = request.url.split('/')[-2],
                           **context)

def outputJsonByMessage(RETURN_CODE,RETURN_DESC = '',RETURN_DATA = ' '): #第五课增加内容
    # RETURN_CODE：返回结果状态码，用不同的状态区分不同类型的错误。
    # RETURN_DESC：如果发生错误，包含具体的错误详细信息。
    dict = {}
    dict['RESPONSE'] = {
                        'RETURN_CODE':RETURN_CODE,
                        'RETURN_STAMP':time.time(),
                        'RETURN_DATA':RETURN_DATA
                        }
    dict['RETURN_DESC'] = RETURN_DESC
    return jsonify(dict)


