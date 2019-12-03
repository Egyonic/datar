from flask import render_template, redirect, request, url_for
from . import data


@data.route('/data')
def data_view():
    return 'this is the resquest'

