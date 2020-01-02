from flask import render_template, redirect, request, url_for,json, current_app, make_response
from flask import jsonify, logging, g
from ..models import User
from .. import db
from . import auth_bp


# 简单的带message的json
def msg_json(msg):
    return jsonify({'message':msg})


@auth_bp.route('/data', methods=["GET"])
def data_view():
    # keyname = request.args.get(key="key")
    return jsonify(resMessage='get the data!',
                   resData='euniu@gmail.com',
                   )


# 用户注册
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    register_data = json.loads(data)
    # logger = logging.create_logger(current_app)
    # print(type(register_data))

    if register_data is None:
        return msg_json('need register data')
    psd = register_data['password']
    email = register_data['email']
    # 检查是否提供了username
    name = register_data['name']
    if name is None:
        name = email
    user = User(name=name,
                password=psd,
                email=email)
    db.session.add(user)
    db.session.commit()
    # 返回用户的信息
    return jsonify(user.to_json())


@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    info_json = request.get_json()
    info = json.loads(info_json)
    if info is None \
            or info['email'] is None \
            or info['password'] is None:
        return msg_json('need login json data')

    user = User.query.filter_by(email=info['email']).first()
    if user is None:
        return msg_json('No such user')

    if user.verify_password(info['password']):
        # 设置当前用户
        g.current_user = user
        g.token_used = False
        return jsonify(user.to_json())
    else:
        return jsonify({
            'message': 'password error'
        })

