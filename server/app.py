from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages',methods =['GET','POST']) 
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        message_dict = [message.to_dict() for message in messages]
        return make_response(jsonify(message_dict), 200)
    elif request.method == 'POST':
        body = request.json['body']
        username = request.json['username']
        message = Message(body=body, username=username)
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict())
@app.route('/messages/<int:id>',methods =['PATCH','DELETE'])
def messages_by_id(id):
    if request.method == 'PATCH':
        message = Message.query.get(id)
        message.body = request.json['body']
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict())
    
    elif request.method == 'DELETE':
        message = Message.query.get(id)
        db.session.delete(message)
        db.session.commit()
        return jsonify(message.to_dict())

if __name__ == '__main__':
    app.run(port=5555)
