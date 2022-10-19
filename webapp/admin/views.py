from flask import Blueprint, render_template
from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')
@admin_required #Если пользователь не аутентифицирован, то перебрасывает на логин.
def admin_index():
    title = "Панель управления"
    first_text = "Панель управления"
    return render_template('admin/index.html', page_title=title, first=first_text)