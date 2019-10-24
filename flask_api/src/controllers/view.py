from flask import Blueprint, jsonify

api_blueprint = Blueprint(
    'api',
    __name__,
    url_prefix='/view/api'
)


@api_blueprint.route('/test/')
def test():
    data = {'name': 'jack'}
    return jsonify(data)
