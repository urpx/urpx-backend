from flask import Blueprint

blueprint = Blueprint('common', __name__)


@blueprint.route('/api/healthy', methods=('GET',))
def healthy():
    return ''  
