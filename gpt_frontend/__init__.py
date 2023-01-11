from flask import Flask

# create and configure the app
app = Flask(__name__)

from . import summarize
app.register_blueprint(summarize.bp)
