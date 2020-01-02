from flask import jsonify, json, request, current_app, url_for, make_response
from . import api
from ..models import User, Group, Task, Record
from ..resJsons import msg_json
from .. import db


@api.route('/groups/<int:id>')
def get_group(id):
    group = Group.query.get_or_404(id)
    return jsonify(group.to_json())


@api.route('/groups/<int:id>/members')
def get_members(id):
    group = Group.query.get_or_404(id)
    members = group.members
    if members is None:
        return jsonify({
            'members': [],
            'count': 0
        })

    return jsonify({
        'members': [user.to_json() for user in members],
        'count': len(members)
    })


@api.route('/groups/<int:id>/tasks')
def get_group_tasks(id):
    group = Group.query.get_or_404(id)
    tasks = group.tasks
    if tasks is None:
        return jsonify({
            'tasks': [],
            'count': 0
        })

    return jsonify({
        'tasks': [task.to_json() for task in tasks],
        'count': len(tasks)
    })


@api.route('/groups/new', methods=['POST'])
def group_new_group():
    json_data = request.get_json()
    data = json.loads(json_data)
    if json_data is None:
        return msg_json('need group data')
    name = json_data['name']
    detail = json_data['detail']
    # 确认是否有detail信息
    if detail is None or detail == '':
        detail = name
    group = Group(name=name, detail=detail)
    db.session.add(group)
    db.commit()

    return jsonify(group.to_json())


@api.route('/groups/<int:id>/newUser', methods=['POST'])
def group_add_user(id):
    group = Group.query.get_or_404(id)
    json_data = request.get_json()
    data = json.loads(json_data)
    if json_data is None:
        return msg_json('need group data')
    user = User.query.get_or_404(data['user_id'])
    group.members += [user]

    return jsonify(group.to_json())


@api.route('/groups/<int:id>/newTask', methods=['POST'])
def group_add_task(id):
    group = Group.query.get_or_404(id)
    json_data = request.get_json()
    data = json.loads(json_data)
    if json_data is None:
        return msg_json('need data')
    task = Task(name=data['name'], detail=data['detail'], group_id=group.id)
    db.session.add(task)
    db.session.commit()
    # group.tasks.append(task)
    members = group.members
    # 为每个群组内的用户添加该任务的记录
    for user in members:
        record_new = Record(uid=user.id, tid=task.id)
        db.session.add(record_new)
    db.session.commit()

    return jsonify(group.to_json())
