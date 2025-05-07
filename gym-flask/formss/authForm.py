from pydantic import BaseModel, Field, field_validator, EmailStr, model_validator
from typing import Optional
from models.auth import UserModel, EmailCaptchaModel,WebCaptchaModel

class RegisterForm(BaseModel):
    email: EmailStr  # 自动验证邮箱格式
    password: str = Field(min_length=8)
    # confirm_password: str  # 用于验证密码一致性
    captcha: str = Field(min_length=4, max_length=4, pattern=r"^\w{4}$")
    username: str = Field(min_length=3)

    # 自定义验证：邮箱是否已注册
    @field_validator("email")
    def email_unique(cls, v):
        if UserModel.query.filter_by(email=v).first():
            raise ValueError("邮箱已被注册")
        return v

    # 自定义验证：用户名是否已存在
    @field_validator("username")
    def username_unique(cls, v):
        if UserModel.query.filter_by(username=v).first():
            raise ValueError("用户名已存在")
        return v

    # 自定义验证：验证码是否正确
    @field_validator("captcha")
    def captcha_valid(cls, v, values):
        if "email" in values.data:
            if not EmailCaptchaModel.query.filter_by(
                email=values.data["email"], captcha=v
            ).first():
                raise ValueError("邮箱验证码错误")
        return v

class LoginForm(BaseModel):
    username: str = Field(min_length=3)
    client_id: str
    password: str = Field(min_length=6)
    captcha: str = Field(min_length=4, max_length=4)

    # 自定义验证：验证码是否正确
    @field_validator("captcha")
    def web_captcha_valid(cls, v, values):
        print(values,123)
        if not WebCaptchaModel.query.filter_by(
            client_id=values.data["client_id"], captcha=v
        ).first():
            raise ValueError("验证码错误")
        return v

    # 自定义验证：用户名和密码是否匹配
    @model_validator(mode='after')  # 在所有字段验证后执行
    def validate_credentials(self):
        user = UserModel.query.filter_by(username=self.username).first()

        if not user:
            raise ValueError("用户不存在")
        if user.password != self.password:  # 假设有 check_password 方法
            raise ValueError("密码错误")

        return self  # 返回模型实例本身

class EmailForm(BaseModel):
    email: EmailStr  # 自动验证邮箱格式