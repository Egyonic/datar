from flask import render_template, redirect, request, url_for,json, current_app
from flask import jsonify
from json import load
from ..models import User
from .. import db

from . import data_bp


@data_bp.route('/data', methods=["GET"])
def data_view():
    # keyname = request.args.get(key="key")
    # current_app.logger.info(keyname)
    return jsonify(resMessage='get the data!',
                   resData='euniu@gmail.com',
                   )


# 接收一个Post的请求，如用户注册
@data_bp.route('/register', methods=['POST'])
def register():
    # current_app.logger.debug(request.mimetype)
    current_app.logger.debug(request.form)

    reg_form = request.form
    # TODO 客户端可以做数据验证，服务器此处也可以添加验证
    name = reg_form['userName']
    psd = reg_form['password']
    email = reg_form['email']
    user = User(username=name,
                password=psd,
                email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify(resMessage='Register success',
                   resData='other data',
                   )



@data_bp.route('/api/flick')
def get_flick_res():
    return redirect(url_for('static', filename='flickRes.json'))

