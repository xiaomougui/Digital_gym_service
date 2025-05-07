from exts import db
from enum import Enum
from datetime import time
from sqlalchemy import Enum as SqlEnum, CheckConstraint, func

# 场馆类型枚举
class VenueType(Enum):
    BASKETBALL = 'basketball'
    BADMINTON = 'badminton'
    SWIMMING = 'swimming'
    GYM = 'gym'
    TENNIS = 'tennis'

# 场馆状态枚举
class VenueStatus(Enum):
    ACTIVE = 'active'
    MAINTENANCE = 'maintenance'
    CLOSED = 'closed'

# 场馆表
class VenueModel(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(SqlEnum('basketball', 'badminton', 'swimming','gym','tennis', name='type'), nullable=False)
    # 场馆容量
    capacity = db.Column(db.Integer, nullable=False)
    # 场馆总数和可用数量
    total_count = db.Column(db.Integer, nullable=False)
    available_count = db.Column(db.Integer, nullable=False)
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)
    status = db.Column(SqlEnum('active', 'maintenance','closed',name='status'), default='active')
    location = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint('available_count <= total_count', name='check_capacity'),
        CheckConstraint('close_time > open_time', name='check_time'),
        {'comment': '场馆信息表'}
    )

    # # 定义关系（如果关联预约表）
    # reservations = db.relationship('ReservationModel', backref='venue', cascade='all, delete-orphan')
    #
    # def __repr__(self):
    #     return f'<Venue {self.name} ({self.type.value})>'

# 预约状态枚举
class ReservationStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'

# 预约表
class ReservationModel(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(SqlEnum('pending', 'confirmed','cancelled','completed',name='status'), default='pending')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())
    notes = db.Column(db.Text)

    # 关系定义
    # user = db.relationship("UserModel", back_populates="reservations")
    # venue = db.relationship("VenueModel", back_populates="reservations")

    __table_args__ = (
        CheckConstraint('end_time > start_time', name='check_time_range'),
        {'comment': '场馆预约表'}
    )

    # def __repr__(self):
    #     return f'<Reservation {self.id} ({self.status.value})>'