import os

from flask import Flask, send_from_directory
from werkzeug.utils import secure_filename

from samizdat.db import session


def create_app():

    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='da21ow2i1h2n',
        UPLOAD_FOLDER='/samizdat/upload/',
    )

    from . import db
    db.init_app(app)

    from .blueprints.auth import auth
    app.register_blueprint(auth.bp)

    from .blueprints.blog import blog
    app.register_blueprint(blog.bp)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

    @app.route('/uploads/<filename>')
    def send_uploaded_file(filename=''):
        return send_from_directory(os.path.join(os.path.dirname(app.instance_path) + app.config['UPLOAD_FOLDER']), filename)

    return app
