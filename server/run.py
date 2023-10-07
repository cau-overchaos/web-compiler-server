from app import create_app
from config import flask_config

app = create_app()

if __name__ == "__main__":
    app.run(host=flask_config.Config.HOST,
            port=flask_config.Config.PORT, use_debugger=True)
