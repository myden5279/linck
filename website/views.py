from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required


UPLOAD_FOLDER = './attribute/'
ALLOWER_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg'}

route = Blueprint("route", __name__)


def checker(file):
    name = file.filename.split('.')[1]
    if name in ALLOWER_EXTENSIONS:
        return secure_filename(file.filename)


@route.route('/')
@login_required
def home():
    return render_template("home.html")


@route.route('/create_message', methods=['GET', 'POST'])
@login_required
def posts():
    if request.method == 'POST':
        head = request.form.get('heading')
        body = request.form.get('body')
        image = request.files['image']

        image_name = checker(image)

        image.save(UPLOAD_FOLDER + image_name)

    return render_template("create_message.html")
