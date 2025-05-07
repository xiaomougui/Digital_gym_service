from exts import db
from datetime import datetime
from sqlalchemy import Enum as SqlEnum  # 使用 SQLAlchemy 的 Enum

# 用户表
class UserModel(db.Model):
    __tablename__ = "users"  # 使用复数形式更符合数据库命名惯例

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(20))  # 联系电话
    id_card = db.Column(db.String(20))  # 身份证号
    real_name = db.Column(db.String(50))  # 真实姓名
    avatar = db.Column(db.String(255))  # 头像URL或Base64编码
    balance = db.Column(db.Numeric(10, 2), default=0.00)  # 账户余额
    status = db.Column(db.Boolean, default=True)  # 账户状态(True-启用/False-禁用)
    join_time = db.Column(db.DateTime, default=datetime.now)  # 注册时间
    last_login = db.Column(db.DateTime)  # 最后登录时间
    permission_level = db.Column(
        SqlEnum('superadmin', 'admin', 'common', name='permission_level'),
        nullable=False,
        default='common'
    )
    gender = db.Column(
        SqlEnum('男', '女', name='gender'),
        nullable=False,
        default='男'
    )

    # 关系定义
    # bookings = db.relationship('BookingModel', backref='user', lazy=True)  # 用户的预约记录
    # equipment_rentals = db.relationship('EquipmentRentalModel', backref='user', lazy=True)  # 设备租赁记录
    # event_participations = db.relationship('EventParticipationModel', backref='user', lazy=True)  # 赛事参与记录

# 邮箱验证码
class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)

# 登录验证码
class WebCaptchaModel(db.Model):
    __tablename__ = "client_captcha"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(64), index=True)  # 客户端唯一标识
    captcha = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # 添加联合唯一约束（确保每个client_id只有一个有效验证码）
    # __table_args__ = (
    #     db.UniqueConstraint('client_id', 'is_used', name='uq_client_unused_captcha',postgresql_where=(is_used == False)),
    # )