# 登录和注册
from flask import Blueprint, jsonify
from exts import mail, db
from flask_mail import Message
from flask import request


from formss.authForm import LoginForm,EmailForm,RegisterForm
from models.auth import EmailCaptchaModel,WebCaptchaModel,UserModel
# from werkzeug.security import generate_password_hash, check_password_hash
from tool.generateCaptchaImg import generate_captcha_image_base64

import string
import random
from datetime import datetime

# 创建蓝图对象
bp = Blueprint("auth", __name__, url_prefix="/auth")



# 登录
@bp.route("/login", methods=['POST'])
def login():
    if(request.method != 'POST'):
        return "请求方式错误"
    else:
        print(request.form, 789)
        if(request.form.get('captcha') == None):
            return "请输入验证码"
        print(request.form,789)
        # 验证表单
        form = LoginForm(**request.form,client_id=request.headers.get("X-Client-ID"))
        user = UserModel.query.filter_by(username=form.username).first()
        print(user,890)
        # 验证验证码是否正确
        # form.web_captcha_valid()
        # 验证用户名和密码
        # if form.validate_credentials == form:
        return jsonify({"code": 200, "msg": "登陆成功", "data": {
            'id':user.id,
            'username': user.username,
            'permission_level': user.permission_level,
            'avatar':user.avatar,
        }})
        # else:
        #     return jsonify({"code": 401, "msg": "用户名或密码错误", "data": None})

# 注册
@bp.route("/register", methods=['POST'])
def register():
    if(request.method != 'POST'):
        return "请求方式错误"
    else:
        form = RegisterForm(**request.form)

        db.session.add(UserModel(
            email=form.email,
            password=form.password,
            username=form.username,
            avatar="data:image/webp;base64,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"
        ))
        db.session.commit()
        return jsonify({"code": 200, "msg": "注册成功", "data": "请登录"})
# 忘记密码

# 登录验证码
@bp.route("/login/captcha", methods=['GET'])
def login_captcha():
    if(request.method != 'GET'):
        return "请求方式错误"
    else:
        # 获取客户端ID
        client_id = request.headers.get("X-Client-ID")
        print(client_id)
        captcha_text, captcha_base64 = generate_captcha_image_base64()
        record = WebCaptchaModel.query.filter_by(
            client_id=client_id,
        ).first()
        # 覆盖旧的验证码
        if record:
            record.captcha = captcha_text
            record.created_at = datetime.now()
        else:
            db.session.add(WebCaptchaModel(
                client_id=client_id,
                captcha=captcha_text
            ))
        db.session.commit()
        return jsonify({
            "code": 200,
            "captcha_image": f"data:image/png;base64,{captcha_base64}"
        })

# 登录验证码验证
# @bp.route("/login/verify", methods=['POST'])
# def login_captcha_verification():
#     if(request.method != 'POST'):
#         return "请求方式错误"
#     else:
#         client_id = request.headers.get("X-Client-ID")
#         captcha = request.form.get("captcha")
#         record = WebCaptchaModel.query.filter_by(
#             client_id=client_id,
#         ).first()
#         if not record or record.captcha != captcha:
#             return jsonify({"code": 401, "msg": "验证码错误", "data": None})
#         else:
#             return jsonify({"code": 200, "msg": "验证码正确", "data": None})

# 邮箱验证码
@bp.route("/email/captcha", methods=['POST'])
def email_captcha():
    if(request.method != 'POST'):
        return "请求方式错误"
    else:
        print(request, 123456)
        form = EmailForm(email=request.form.get('email'))

        email = form.email
        subject = "邮箱验证码"
        message = Message(subject=subject, recipients=[email])
        rand_num = ''.join(random.sample(string.digits, 4))
        message.body = f"您的验证码是{rand_num}"
        try:
            mail.send(message)
            print(email)
            # 用数据库表的方式存储
            record = EmailCaptchaModel.query.filter_by(
                email=email,
            ).first()
            # 覆盖旧的验证码
            if record:
                record.captcha = rand_num
            else:
                email_captcha = EmailCaptchaModel(email=email, captcha=rand_num)
                db.session.add(email_captcha)
            db.session.commit()
            return jsonify({"code":200,"msg":"发送成功","data":None})
        except Exception as e:
            print(e,789)
            return jsonify({"code":500,"msg":"发送失败","data":None})

# 邮箱验证码验证
@bp.route("/email/verify", methods=['POST'])
def email_captcha_verification():
    pass