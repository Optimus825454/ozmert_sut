from flask import Blueprint

blueprint = Blueprint('auth', __name__)

@blueprint.route('/login')
def login():
    return "Login sayfası"

@blueprint.route('/register')   
def register():
    return "Register sayfası"

@blueprint.route('/logout')
def logout():
    return "Logout sayfası"

@blueprint.route('/forgot-password')
def forgot_password():
    return "Forgot password sayfası"

@blueprint.route('/reset-password')
def reset_password():
    return "Reset password sayfası"

@blueprint.route('/change-password')
def change_password():
    return "Change password sayfası"

@blueprint.route('/profile')
def profile():
    return "Profile sayfası"

@blueprint.route('/profile/edit')
def profile_edit():
    return "Profile edit sayfası"

@blueprint.route('/profile/delete')
def profile_delete():
    return "Profile delete sayfası"
