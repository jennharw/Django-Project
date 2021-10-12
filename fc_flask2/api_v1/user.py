from . import api
from flask import jsonify, request
from flask_jwt import jwt_required
from models import Fcuser, db
@api.route('/test')
def test():
    return jsonify
    #data json 형태 반환 (+ 상태코드)

#회원가입 data 
@api.route('/users', methods = ['GET', 'POST'])
@jwt_required()
def users():
    #form 대신 request
    if request.method == 'POST': #회원 등록 api
        data = request.get_json()
        print(data)

        userid = data.get('userid')
        username = data.get('username')
        password = data.get('password')
        re_password = data.get('re-password')

        if not (userid and username and password and re_password):
            return jsonify({'error':'Nor arguments'}), 400
        if password != re_password:
            return jsonify({'error':'Wrong Password'}), 400
        fcuser = Fcuser()
        fcuser.userid = userid
        fcuser.username = username
        fcuser.password = password
        db.session.add(fcuser)
        db.session.commit()
        return jsonify(), 201
    
    #회원목록 api
    users = Fcuser.query.all() #serializable? Object 
    return jsonify([user.serialize for user in users])

#수정 삭제 조회 - 회원상세
@api.route('/users/<uid>', methods = ['GET', 'PUT', 'DELETE'])
def user_detail(uid):
    if request.method == 'GET':
        user = Fcuser.query.filter(Fcuser.id == uid).first()
        return jsonify(user.serialize)
    elif request.method =='DELETE':
        user = Fcuser.query.delete(Fcuser.id == uid)
        return jsonify(), 204

    #request.form 이 아니라
    data = request.get_json()
    # userid = data.get('userid')
    # username = data.get('username')
    # password = data.get('password')

    # update_data = {}
    # if userid:
    #     update_data['user'] = userid
    # if username:
    #     update_data['username'] = username
    # if password:
    #     update_data['password'] = password
    
    Fcuser.query.filter(Fcuser.id == uid).update(data)
    user = Fcuser.query.filter(Fcuser.id == uid).first()
    return jsonify(user.serialize)

    


