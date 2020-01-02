from flask import jsonify, json, request, current_app, url_for, make_response, logging
from . import api
from ..models import User,Record
from .. import db
from ..resJsons import msg_json


# 修改记录的完成情况
@api.route('/records/<int:id>/finish', methods=['GET', 'POST'])
def get_record(id):
    logger = logging.create_logger(current_app)

    record = Record.query.get_or_404(id)
    data_json = request.get_json()
    if data_json is None:
        return jsonify(record.to_json())

    data = json.loads(data_json)
    finish = data['finish']
    if finish is None:
        return msg_json('need data')
    elif finish == 1:
        record.done = True
    elif finish == 0:
        record.done = False

    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_json())


# 暂时不需要此接口
# @api.route('/records/<int:id>/task/<int:tid>')
# def get_record(id, tid):
#     record = Record.query.get_or_404(id)

