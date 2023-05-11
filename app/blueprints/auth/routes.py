from flask import current_app as app
from flask import Blueprint, request, render_template

auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    data = {
        'email': request.form.get('email'),
        'password': request.form.get('password'),
    }
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    data = {
        'email': request.form.get('email'),
        'password': request.form.get('password'),
    }
    print(data)
    return render_template('login.html')
