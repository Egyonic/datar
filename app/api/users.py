from flask import jsonify, json, request, current_app, url_for, make_response
from . import api
from ..models import User,Group
from ..resJsons import msg_json

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/groups')
def get_user_groups(id):
    user = User.query.get_or_404(id)
    groups = user.groups
    return jsonify({
        'groups': [ group.to_json() for group in groups],
        'count': len(groups)
    })


@api.route('/users/<int:id>/tasks')
def get_user_tasks(id):
    user = User.query.get_or_404(id)
    groups = user.groups
    if (groups is None) or (len(groups) == 0):
        return jsonify({
            'tasks': [],
            'count': 0
        })
    tasks = []
    for group in groups:
        tasks += group.tasks

    # tasks.sort(key='group_id')
    return jsonify({
        'tasks': [task.to_json() for task in tasks],
        'count': len(tasks)
    })


@api.route('/users/<int:id>/records')
def get_user_records(id):
    user = User.query.get_or_404(id)
    records = user.records
    if records is None or len(records) == 0:
        return jsonify({
            'records': [],
            'count': 0
        })
    return jsonify({
        'records': [record.to_json() for record in records],
        'count': len(records)
    })



