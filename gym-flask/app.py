from flask import Flask, session, g, jsonify
from flask_cors import CORS
import config
from exts import db, mail
from pydantic import ValidationError
from blueprint.auth import bp as auth_bp
from blueprint.user import bp as user_bp
from blueprint.feedback import bp as feedback_bp
from blueprint.equipment import bp as equipment_bp
from blueprint.venues import bp as venues_bp
# from models import UserModel

app = Flask(__name__)
# 跨域
CORS(app, supports_credentials=True)
# 配置
app.config.from_object(config)

db.init_app(app)
mail.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(feedback_bp)
app.register_blueprint(equipment_bp)
app.register_blueprint(venues_bp)


# class APIError(Exception):
#     """自定义 API 异常"""
#     def __init__(self, message, status_code=400):
#         super().__init__()
#         self.message = message
#         self.status_code = status_code

# 注册全局异常处理器
# 验证错误处理器
@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({
        "error": "Validation Error",
        "details": e.errors()  # Pydantic 的标准错误格式
    }), 400

# @app.errorhandler(APIError)
# def handle_api_error(e):
#     return jsonify({
#         "error": e.message
#     }), e.status_code



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
