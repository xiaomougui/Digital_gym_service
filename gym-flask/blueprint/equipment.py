# 设备管理
# 反馈与评价
from flask import Blueprint,jsonify,request
from exts import db
from models.auth import UserModel
from datetime import datetime
from models.equipment import SportsEquipmentModel,EquipmentRentalModel

bp = Blueprint('equipment', __name__, url_prefix='/equipment')

# 获取设备列表
@bp.route('/list', methods=['GET'])
def equipment_list():
    equipments = SportsEquipmentModel.query.all()
    result = [{
        'id': e.id,
        'name': e.name,
        'type': e.type,
        'total_quantity': e.total_quantity,
        'available_quantity': e.available_quantity,
        'description': e.description,
        'status': e.status,
        'price': e.price,
        'purchase_date': e.purchase_date,
        'location': e.location,
    } for e in equipments]
    return jsonify({'code': 200, 'msg': 'success', 'data': result})

# 添加设备
@bp.route('/add', methods=['POST'])
def add_equipment():
    form = request.form
    new_equipment = SportsEquipmentModel(**form)
    db.session.add(new_equipment)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '创建成功'})

# 更新设备信息
@bp.route('/update-equipment/<int:equipment_id>', methods=['POST'])
def update_equipment(equipment_id):
    data = request.get_json()
    equipment = SportsEquipmentModel.query.filter_by(id=equipment_id).first()
    if not equipment:
        return jsonify({'code': 404, 'msg': 'not found'})
    for key, value in data.items():
        setattr(equipment, key, value)
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'success'})

# 删除设备
@bp.route('/delete-equipment/<int:equipment_id>', methods=['DELETE'])
def delete_equipment(equipment_id):
    equipment = SportsEquipmentModel.query.filter_by(id=equipment_id).first()
    if not equipment:
        return jsonify({'code': 404, 'msg': 'not found'})
    db.session.delete(equipment)
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'success'})

# 获取我的租赁列表
@bp.route('/my-rentals', methods=['GET'])
def my_rentals():
    user_id = request.args.get('user_id')
    rentals = EquipmentRentalModel.query.filter_by(user_id=user_id).all()
    result = []
    for rental in rentals:
        equipment = SportsEquipmentModel.query.filter_by(id=rental.equipment_id).first()
        result.append({
            'id': rental.id,
            'equipment_id': rental.equipment_id,
            # 添加设备名称
            'equipment_name': equipment.name,
            'rental_quantity': rental.rental_quantity,
            'rental_date': rental.rental_date,
            # 添加预期归还日期
            'expected_return_date': rental.expected_return_date,
            # 添加实际归还日期
            'actual_return_date': rental.actual_return_date,
            'rental_status': rental.rental_status,
            'deposit': rental.deposit,
            'rental_fee': rental.rental_fee
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': result})

# 租赁设备
@bp.route('/rental', methods=['POST'])
def rent_equipment():
    data = request.form
    print(data)
    # data['rental_quantity'] = int(data['rental_quantity'])
    print(data)
    # 检查设备是否存在
    equipment = SportsEquipmentModel.query.filter_by(id=data['equipment_id']).first()
    if not equipment:
        return jsonify({'code': 404, 'msg': '器材不存在'})
    if equipment.available_quantity < int(data['rental_quantity']):
        return jsonify({'code': 400, 'msg': '器材剩余数量不足'})
    equipment.available_quantity -= int(data['rental_quantity'])
    new_rental = EquipmentRentalModel(**data)
    new_rental.rental_status = '租借中'
    # new_rental.rental_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.session.add(new_rental)
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'success'})

# 取消租赁
@bp.route('/cancel-rental/<int:rental_id>', methods=['PUT'])
def cancel_rental(rental_id):
    rental = EquipmentRentalModel.query.filter_by(id=rental_id).first()
    if not rental:
        return jsonify({'code': 404, 'msg': 'not found'})
    equipment = SportsEquipmentModel.query.filter_by(id=rental.equipment_id).first()
    equipment.available_quantity += rental.rental_quantity
    rental.rental_status = 3
    db.session.commit()
    return jsonify({'code': 200, 'msg': 'success'})

# 归还设备
@bp.route('/return-equipment/<int:rental_id>', methods=['PUT'])
def return_equipment(rental_id):
    rental = EquipmentRentalModel.query.filter_by(id=rental_id).first()
    if not rental:
        return jsonify({'code': 404, 'msg': '未查找到租赁记录'})
    equipment = SportsEquipmentModel.query.filter_by(id=rental.equipment_id).first()
    equipment.available_quantity += rental.rental_quantity
    rental.rental_status = 2
    rental.actual_return_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.session.commit()
    return jsonify({'code': 200, 'msg': '成功归还'})

# 获取所有租赁记录
@bp.route('/rentals', methods=['GET'])
def get_rentals():
    rentals = EquipmentRentalModel.query.all()
    result = []
    for rental in rentals:
        equipment = SportsEquipmentModel.query.filter_by(id=rental.equipment_id).first()
        user = UserModel.query.filter_by(id=rental.user_id).first()
        result.append({
            'id': rental.id,
            'equipment_id': rental.equipment_id,
            'equipment_name': equipment.name,
            'type':equipment.type,
            'user_id': rental.user_id,
            'user_name': user.username,
            'rental_quantity': rental.rental_quantity,
            'rental_date': rental.rental_date,
            'expected_return_date': rental.expected_return_date,
            'actual_return_date': rental.actual_return_date,
            'rental_status': rental.rental_status,
            'deposit': rental.deposit,
            'rental_fee': rental.rental_fee
        })
    return jsonify({'code': 200, 'msg': 'success', 'data': result})
