from flask import Blueprint, render_template, current_app

blueprint = Blueprint('news', __name__)

@blueprint.route("/")
def index():
    title = current_app.config['TEST_KEY']
    first_text = "Hello, project"
    return render_template('news/index.html', 
                            page_title=title, 
                            first=first_text
                        )
        