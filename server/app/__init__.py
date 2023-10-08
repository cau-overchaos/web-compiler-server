from flask import Flask
from config import flask_config


def register_router(flask_app: Flask):
    # router 등록
    from router.executer.execute import execute
    # from router.judgement.judge import judge

    flask_app.register_blueprint(execute)
    # flask_app.register_blueprint(judge)

    @flask_app.before_request
    def before_request():
        print("before_request")

    @flask_app.after_request
    def after_request(result):
        print("after_request", result.status_code)
        return result


def create_app():
    # 앱 설정
    app = Flask(__name__)
    app.config.from_object(get_flask_env())
    register_router(app)
    return app


def get_flask_env():
    if flask_config.Config.ENV == 'prod':
        return 'config.flask_config.prodConfig'
    if flask_config.Config.ENV == 'dev':
        return 'config.flask_config.devConfig'
