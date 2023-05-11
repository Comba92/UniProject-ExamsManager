from flask import Blueprint, render_template
from flask import current_app as app

# Blueprint Configuration
welcome_bp = Blueprint(
    'welcome_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@welcome_bp.route('/', methods=['GET'])
def welcome():
    """
    Welcome/ Landing Page

    """
    return render_template(template_name_or_list='welcome.html')

