from flask import jsonify, json, request, current_app, url_for, make_response
from . import api
from ..models import User,Group


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

