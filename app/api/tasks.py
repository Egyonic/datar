from flask import jsonify, json, request, current_app, url_for, make_response
from . import api
from ..models import User,Record, Task

@api.route('/tasks/<int:id>')
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_json())


@api.route('/tasks/<int:id>/records')
def get_task_records(id):
    task = Task.query.get_or_404(id)
    records = task.records
    if records is None:
        return jsonify({
            'records': [],
            'ccount': 0
        })

    return jsonify({
        'records': [record.to_json() for record in records],
        'count': 0
    })

