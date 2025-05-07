# 场馆
import string
import random
from flask import Blueprint,jsonify,request
from exts import db
from models.venue import VenueModel,ReservationModel
from models.auth import UserModel
from formss.venueForm import ReservationForm
from datetime import datetime
from tool.checkIsOverlap import checkIsOverlap

bp = Blueprint('venue', __name__, url_prefix='/venue')
# 场馆预约 增
@bp.route('/reservation', methods=['POST'])
def reservation():
    # 一天只能预约一次
    try:
        data = request.form
        reservation = ReservationModel.query.filter_by(user_id=data["user_id"]).all()
        # 检查是否重复预约
        if len(reservation) > 5:
            return jsonify({'code': 401, 'msg': '一天只能预约五次'})
        # for r in reservation:
        #     # if(checkIsOverlap(r.start_time, r.end_time, datetime(data["start_time"]), datetime(data["end_time"]))):
        #     #     return jsonify({'code': 401, 'msg': '重复预约'})
        #     # else:
        #     if
        #         return jsonify({'code': 401, 'msg': '一天只能预约一次'})

        # 保存到数据库
        new_reservation = ReservationModel(**request.form)
        # 场馆可用数量减一
        venue = VenueModel.query.get(data['venue_id'])
        venue.available_count -= 1
        db.session.add(new_reservation)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '预约成功'})
    except Exception as e:
        print(e)
        return jsonify({'code': 500, 'msg': '预约失败'})

# 场馆信息列表 查
@bp.route('/info', methods=['GET'])
def info():
    venue = VenueModel.query.all()
    print(venue)
    if not venue:
        return jsonify({'code': 404, 'msg': '暂无场馆'})
    else:
        result= [{
            'id': v.id,
            'name': v.name,
            'type': v.type,
            'capacity': v.capacity,
            'total_count': v.total_count,
            'available_count': v.available_count,
            'open_time': v.open_time.strftime('%H:%M:%S'),
            'close_time': v.close_time.strftime('%H:%M:%S'),
            'status': v.status,
            'location': v.location,
            'description': v.description
        }for v in venue]
        print(result)
        return jsonify({'code': 200, 'msg': '获取场馆信息成功', 'data': result})

# 我的预约 查
@bp.route('/my_reservation/<int:id>', methods=['GET'])
def my_reservation(id):
    reservations = ReservationModel.query.filter_by(user_id=id).all()
    if not reservations:
        return jsonify({'code': 404, 'msg': '暂无预约'})
    else:
        result=[]
        for r in reservations:
            venue = VenueModel.query.get(r.venue_id)
            user = UserModel.query.get(r.user_id)
            result.append({
                'id': r.id,
                'venue_id': r.venue_id,
                'venue_name': venue.name,
                'type':venue.type,
                'start_time': r.start_time,
                'end_time': r.end_time,
                'status': r.status,
                'created_at': r.created_at,
                'updated_at': r.updated_at,
                'notes': r.notes})
        return jsonify({'code': 200, 'msg': '获取预约信息成功', 'data': result})


# 预约详情（admin）
@bp.route('/reservation_detail/<string:permission_level>', methods=['GET'])
def reservation_detail(permission_level):
    if(permission_level == 'common'):
        return jsonify({'code': 403, 'msg': '权限不足'})
    else:
        # 查询所有预约记录
        reservation = ReservationModel.query.all()
        if not reservation:
            return jsonify({'code': 404, 'msg': '预约列表为空'})
        else:
            result = []
            for r in reservation:
                venue = VenueModel.query.get(r.venue_id)
                user = UserModel.query.get(r.user_id)
                result.append({
                    'id': r.id,
                    'venue_id': r.venue_id,
                    'venue_name': venue.name,
                    'type': venue.type,
                    'start_time': r.start_time,
                    'end_time': r.end_time,
                    'status': r.status,
                    'user_name':user.username,
                    'created_at': r.created_at,
                    'updated_at': r.updated_at,
                    'notes': r.notes})
            return jsonify({'code': 200, 'msg': '获取预约详情成功', 'data': result})

# 取消预约 改
@bp.route('/cancel_reservation/<int:id>', methods=['PUT'])
def cancel_reservation(id):
    try:
        reservation = ReservationModel.query.get(id)
        if not reservation:
            return jsonify({'code': 404, 'msg': '预约不存在'})
        # 场馆可用数量加一
        venue = VenueModel.query.get(reservation.venue_id)
        venue.available_count += 1
        reservation.status = 'cancelled'
        db.session.commit()
        return jsonify({'code': 200, 'msg': '取消预约成功'})
    except Exception as e:
        print(e)
        return jsonify({'code': 500, 'msg': '取消预约失败'})


# 场馆创建（admin）增
@bp.route('/create', methods=['POST'])
def create():
    try:
        data = request.form
        print(data)
        venue = VenueModel(**data)
        db.session.add(venue)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '创建场馆成功'})
    except Exception as e:
        print(e)
        return jsonify({'code': 500, 'msg': '创建场馆失败'})

# 场馆修改（admin）改
@bp.route('/update', methods=['POST'])
def update():
    try:
        data = request.form
        venue = VenueModel.query.get(data['id'])
        for key, value in data.items():
            setattr(venue, key, value)
        venue.updated_at = datetime.now()
        db.session.commit()
        return jsonify({'code': 200, 'msg': '更新场馆成功'})
    except Exception as e:
        print(e)
        return jsonify({'code': 500, 'msg': '更新场馆失败'})

# 场馆删除（admin）删
@bp.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    try:
        venue = VenueModel.query.get(id)
        db.session.delete(venue)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '删除场馆成功'})
    except Exception as e:
        print(e)
        return jsonify({'code': 500, 'msg': '删除场馆失败'})
