from flask import Flask, request
from config import flask_config
from provider import util


def register_router(flask_app: Flask):
    # router 등록
    from router.executor.execute import execute
    # from router.judgement.judge import judge

    flask_app.register_blueprint(execute)
    # flask_app.register_blueprint(judge)

    @flask_app.before_request
    def before_request():
        # 백엔드 서버인지 확인
        client_ip = request.remote_addr
        print(client_ip)
        if client_ip not in flask_config.Config.TRUSTED_IPS:
            return "Unauthorized", 401  # 허용되지 않은 호스트일 경우 401 Unauthorized 응답 반환

        # 디렉토리 클리어
        util.clean_dir(flask_config.Config.RESULTS_FOLDER)
        util.clean_dir(flask_config.Config.CODE_FOLDER)

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
