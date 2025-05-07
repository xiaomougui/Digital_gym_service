# 反馈与评价
from flask import Blueprint,jsonify,request
from exts import db
from models.auth import UserModel
from datetime import datetime
from models.feedback import FeedbackModel

bp = Blueprint('feedback', __name__, url_prefix='/feedback')

# 创建反馈
@bp.route('/create', methods=['POST'])
def create_feedback():
    try:
        print(request.form)
        user_id = request.form.get('user_id')
        message = request.form.get('message')
        if not all([user_id, message]):
            return jsonify({'code': 401, 'msg': '参数不完整'})
        feedback = FeedbackModel()
        feedback.user_id = user_id
        feedback.message = message
        # feedback.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.add(feedback)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '反馈成功，静候佳音'})
    except Exception as e:
        print(e)

# 查看反馈
@bp.route('/list', methods=['GET'])
def list_feedback():
    feedbacks = FeedbackModel.query.all()
    feedback_list = []
    for feedback in feedbacks:
        feedback_dict = {
            'id': feedback.id,
            'user_id': feedback.user_id,
            'message': feedback.message,
            'solved': feedback.solved,
            'date': feedback.date
        }
        feedback_list.append(feedback_dict)
    return jsonify({'code': 200, 'data': feedback_list})

# 查看我的反馈
@bp.route('/my_feedback', methods=['GET'])
def my_feedback():
    user_id = request.args.get('user_id')
    feedbacks = FeedbackModel.query.filter_by(user_id=user_id).all()
    feedback_list = []
    for feedback in feedbacks:
        feedback_dict = {
            'id': feedback.id,
            'user_id': feedback.user_id,
            'message': feedback.message,
            'date': feedback.date,
            'solved': feedback.solved,
            'reason': feedback.reason
        }
        feedback_list.append(feedback_dict)
    return jsonify({'code': 200, 'data': feedback_list})

# 处理反馈
@bp.route('/handle', methods=['POST'])
def handle_feedback():
    feedback_id = request.form.get('id')
    reason = request.form.get('reason')
    solved = request.form.get('solved')
    feedback = FeedbackModel.query.filter_by(id=feedback_id).first()
    feedback.reason = reason
    feedback.solved = bool(solved)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '反馈处理已提交'})

# 删除反馈