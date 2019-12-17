from flask import jsonify, json, request, current_app, url_for, make_response
from . import api
from ..models import User,Record

@api.route('/records/<int:id>')
def get_record(id):
    record = Record.query.get_or_404(id)
    return jsonify(record.to_json())


# 暂时不需要此接口
# @api.route('/records/<int:id>/task/<int:tid>')
# def get_record(id, tid):
#     record = Record.query.get_or_404(id)

