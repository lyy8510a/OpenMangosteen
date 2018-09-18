#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created by liaoyangyang1 on 2018/9/14 上午11:12.
"""
from flask_assets import Environment, Bundle

assets_env = Environment()

main_css = Bundle(
    "css/bootstrap.css",
    "font-awesome/css/font-awesome.css",
    "css/animate.css",
    'css/style.css',
    "css/plugins/dataTables/datatables.min.css",
    filters='cssmin',
    output='assets/css/common.css')

main_js = Bundle(
    "js/jquery-2.1.1.js",
    "js/bootstrap.min.js",
    "js/plugins/jquery-ui/jquery-ui.min.js",
    "js/plugins/metisMenu/jquery.metisMenu.js",
    "js/plugins/slimscroll/jquery.slimscroll.min.js",
    "js/layer.js",
    "js/inspinia.js",
    "js/plugins/datatables/datatables.min.js",
    filters='jsmin',
    output='assets/js/common.js')
