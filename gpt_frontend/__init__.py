import os

from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
