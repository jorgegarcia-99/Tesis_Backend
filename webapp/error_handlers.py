from flask import Blueprint, jsonify

bp = Blueprint('error', __name__, url_prefix='/error')

@bp.app_errorhandler(404)
def page_not_found(e):
    """ Return error 404 """
    return jsonify(error=str(e)), 404