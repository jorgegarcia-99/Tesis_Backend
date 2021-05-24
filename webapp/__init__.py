import os

from flask import Flask
from . import config
from flask_cors import CORS

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    
    if test_config is None:
        # app.config.from_pyfile('config.py', silent=True)
        app.config.from_object(config.DevelopmentConfig)
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register the BluePrints
    from . import posts, demo, error_handlers
    
    app.register_blueprint(posts.bp)
    app.register_blueprint(demo.bp)
    app.register_blueprint(error_handlers.bp)

    return app