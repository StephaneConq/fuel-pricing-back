from flask import Blueprint, request

user_bp = Blueprint('user_bp', __name__, )


@user_bp.route('/current')
def get_user_info():
    print(request.headers.get('Authorization'))
    return {
        "token": request.headers.get('Authorization').replace('Bearer ', ''),
        "email": request.headers.get('X-Goog-Authenticated-User-Email').replace('accounts.google.com: ', '')
    }
