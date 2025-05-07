# 用户
# 登录和注册
from flask import Blueprint, jsonify
from exts import mail, db

from flask import request


from formss.authForm import LoginForm,EmailForm,RegisterForm
from models.auth import EmailCaptchaModel,WebCaptchaModel,UserModel
# from werkzeug.security import generate_password_hash, check_password_hash
from tool.generateCaptchaImg import generate_captcha_image_base64

import string
import random
from datetime import datetime

bp = Blueprint("user", __name__, url_prefix="/user")

# 查询用户列表
@bp.route("/list",methods=["GET"])
def user_list():
    list = UserModel.query.all()
    return jsonify({
        'code':200,
        'data': [{
            'id': item.id,
            'username': item.username,
            'email': item.email,
            'phone': item.phone,
            'real_name': item.real_name,
            'avatar': item.avatar,
            'balance': item.balance,
            'permission_level': item.permission_level,
            'gender':item.gender,
            'id_card':item.id_card
        }for item in list]
    })

# 删除用户
@bp.route("/delete/<int:id>/<string:permission_level>",methods=["DELETE"])
def delete_user( id ,permission_level):
    if permission_level == 'common':
        return "权限不足"
    user = UserModel.query.get(id)
    if not user:
        return "用户不存在"
    else:
        try:
            db.session.delete(user)
            db.session.commit()
            return "删除成功"
        except Exception as e:
            print(e)
            return "删除失败"

# 查询用户信息（id）
@bp.route("/info/<int:id>",methods=["GET"])
def user_info(id):
    user = UserModel.query.get(id)
    if not user:
        return "用户不存在"
    else:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            'real_name': user.real_name,
            'avatar': user.avatar,
            'balance': user.balance,
            'permission_level': user.permission_level,
            'gender':user.gender
        })

# 修改用户信息（id）
@bp.route("/update",methods=["POST"])
def update_user():
    # username password email phone avatar balance status
    form = request.form
    print(form)
    if form['phone'] != '' and form['phone'] is not None:
        user = UserModel.query.filter_by(phone=form['phone']).first()
        print(type(user.id),type(form['id']))
        if user.id != int(form['id']):
            return {'code':400,'msg':"手机号已被占用"}
    try:
        user = UserModel.query.get(form['id'])
        for key in form:
            setattr(user, key, form[key])
        db.session.add(user)
        db.session.commit()
        return {'code':200,'msg':"修改成功"}
    except Exception as e:
        print(e)
        return {'code':400,'msg':"修改失败"}
# 用户注销
@bp.route("/usercancel",methods=["POST"])
def user_cancel():
    form = request.form
    username = form['username']
    user = UserModel.query.get(username)
    if not user:
        return {'code':400,'msg':"用户不存在"}
    else:
        try:
            db.session.delete(user)
            db.session.commit()
            return {'code':200,'msg':"注销成功"}
        except Exception as e:
            print(e)
            return {'code':400,'msg':"注销失败"}

# 忘记密码
@bp.route("/updatepassword",methods=["POST"])
def update_password():
    form = request.form
    id = form['id']

    old_password = form['old_password']
    new_password = form['new_password']
    if old_password == new_password:
        return {'code':400,'msg':"新旧密码不能与旧密码相同"}
    else:
        user = UserModel.query.get(id)
        if not user:
            return {'code':400,'msg':"用户不存在"}
        else:
            if user.password != old_password:
                return {'code':400,'msg':"原密码错误"}
            else:
                try:
                    user.password = new_password
                    db.session.add(user)
                    db.session.commit()
                    return {'code':200,'msg':"修改成功"}
                except Exception as e:
                    print(e)
                    return {'code':400,'msg':"修改失败"}
