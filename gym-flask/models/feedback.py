from exts import db
from datetime import datetime
from sqlalchemy import Enum as SqlEnum  # 使用 SQLAlchemy 的 Enum

class FeedbackModel(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    reason = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.now)
    solved = db.Column(db.Boolean, default=False)
    soluser_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # 关联 UserModel
    user = db.relationship('UserModel', foreign_keys=[user_id])
    solver = db.relationship('UserModel', foreign_keys=[soluser_id])
