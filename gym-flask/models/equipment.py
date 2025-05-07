from exts import db
from datetime import datetime
from sqlalchemy import Enum as SqlEnum  # 使用 SQLAlchemy 的 Enum


class EquipmentRentalModel(db.Model):
    __tablename__ = 'equipment_rental'

    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('sports_equipment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rental_quantity = db.Column(db.Integer, nullable=False)
    rental_date = db.Column(db.DateTime, default=datetime.utcnow)
    expected_return_date = db.Column(db.DateTime, nullable=False)
    actual_return_date = db.Column(db.DateTime)
    rental_status = db.Column(db.Enum('租借中', '已归还', '超期未还', '已取消',
                                      name='rental_status'), default='租借中')
    deposit = db.Column(db.Numeric(10, 2))
    rental_fee = db.Column(db.Numeric(10, 2))
    notes = db.Column(db.Text)

    # def __init__(self, **kwargs):
    #     super(EquipmentRental, self).__init__(**kwargs)
    #     # 确保租借数量为正数
    #     if self.rental_quantity <= 0:
    #         raise ValueError("租借数量必须大于0")
    #
    # def __repr__(self):
    #     return f'<EquipmentRental {self.id}>'


class SportsEquipmentModel(db.Model):
    __tablename__ = 'sports_equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum('篮球类', '足球类', '羽毛球类', '乒乓球类','球类', '健身器材', '户外装备', '水上器材', '其他',
                             name='equipment_type'), nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False, default=0)
    available_quantity = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text)
    status = db.Column(db.Enum('正常', '维修中', '报废',
                               name='equipment_status'), default='正常')
    purchase_date = db.Column(db.Date)
    price = db.Column(db.Numeric(10, 2))
    location = db.Column(db.String(100))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now())

    # 与租赁表的关系
    rentals = db.relationship('EquipmentRentalModel', backref='equipment', lazy=True)

    # def __init__(self, **kwargs):
    #     super(SportsEquipment, self).__init__(**kwargs)
    #     # 确保可用数量不大于总数
    #     if self.available_quantity > self.total_quantity:
    #         raise ValueError("可用数量不能大于总数量")
    #
    # def __repr__(self):
    #     return f'<SportsEquipment {self.name}>'