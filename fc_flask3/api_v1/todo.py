from . import api
from flask import json, jsonify
from flask import request, session
import requests 
import datetime
from model import Todo, db, Fcuser

def send_slack(msg):
    res = requests.post('https://hooks.slack.com/services/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',json={
            'text': 'harim %s' % msg
        }, headers = {'Content-Type':'application/json'})

#TODO update api -> view home.html jquery
@api.route('/todos/done', methods = ['PUT'])
def todos_done():
    userid = session.get('userid', None)
    if not userid:
            return jsonify(), 401
    data =  request.get_json()
    todo_id = data.get('todo_id')
    todo = Todo.query.filter_by(id=todo_id).first()
    fcuser = Fcuser.query.filter_by(userid=userid).first()

    if todo.fcuser_id != fcuser.id:
        return jsonify(), 400
    
    todo.status = 1

    #db.session.update(todo)
    db.session.commit()
    return jsonify()


#TODO CRUD api -> view, jquery 
@api.route('/todos', methods = ['GET', 'POST', 'DELETE'])
def todos():
    userid = session.get('userid', None)
    if not userid:
            return jsonify(), 401
    if request.method == "POST": # data {'title':' ', 'due':''08/21/2019'}
        data =  request.get_json()

        todo = Todo()
        todo.title = data.get('title')

        fcuser = Fcuser.query.filter_by(userid=userid).first()
        todo.fcuser_id = fcuser.id
        todo.due = data.get('due')
        todo.status =  0

        db.session.add(todo)
        db.session.commit()      

        send_slack('TODO가 생성됨') #사용자 정보, 할일 제목, 기한
        
        return jsonify(), 201
    elif request.method == "GET":
        todos = Todo.query.filter_by(fcuserid = userid)
        return jsonify([t.serialize for t in todos])

    else: # data {'todo_id':' '} DELETE post 아니라 
        data = request.get_json()
        todo_id = data.get('todo_id')
        todo = Todo.query.filter_by(id = todo_id).first()
        db.session.delete(todo)
        db.session.commit()
        return jsonify(), 203
    return jsonify(data)


#slack command
@api.route('/test', methods = ['POST'])
def test():
    res = request.form['text']
    print(res)
    return jsonify(res)

@api.route('/slack/todos', methods = ['POST'])
def slack_todos():
    res = request.form['text'].split(' ')
    cmd , *args = res


    #/flasktodo create aaaa
    #/flasktodo list
    ret_msg = ''

    if cmd == 'create':
        todo_user_id = args[0]
        todo_name = args[1]
        todo_due = args[2]

        fcuser = Fcuser.query.filter_by(userid=todo_user_id).first()

        todo  = Todo()
        todo.fcuser_id = fcuser.id
        todo.title = todo_name
        todo.due = todo_due
        todo.status = 0


        db.session.add(todo)
        db.session.commit()

        ret_msg = 'todo가 생성되었습니다'
        send_slack('할일을 만들었습니다 [%s] %s' % (str(datetime.datetime.now()), todo_name))

    elif cmd == 'list':
        todo_user_id = args[0]
        fcuser = Fcuser.query.filter_by(userid=todo_user_id).first()

        todos = Todo.query.filter_by(fcuser_id=fcuser.id)
        for idx, todo in enumerate(todos):
            ret_msg += '%d, %s (~ %s) \n'%(idx+1, todo.title, todo.due)

    return ret_msg