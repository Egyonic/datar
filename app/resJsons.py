from flask import jsonify,json


# 简单的带message的json
def msg_json(msg):
    return jsonify({'message':msg})

