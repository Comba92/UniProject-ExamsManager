from flask import Blueprint, render_template
from flask import current_app as app

# Blueprint Configuration
welcome_bp = Blueprint(
    'dashboard_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@welcome_bp.route('/', methods=['GET'])
def dashboard():
    """

    """
    return render_template(template_name_or_list='welcome.html')

