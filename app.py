from flask import Flask,jsonify,request,make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api,Resource
from flask_jwt_extended import create_access_token,JWTManager,get_jwt_identity,jwt_required
app=Flask(__name__)
app.config['SECRET_KEY']='thissecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db=SQLAlchemy(app)
api=Api(app)
jwt=JWTManager(app)

class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(50))
    password=db.Column(db.String(50))



class UserRegistration(Resource):
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']

        if not username or not password:
            return {'message':'password and username ismissing'},400
        if User.query.filter_by(username=username).first():
            return {'message':'username allredy exist'}
        new_user=User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return {"meaasge":'new user created sucssessfully'},200
    

class UserLogin(Resource):
    def post(self):
        data=request.get_json()
        username=data['username']
        password=data['password']
        user=User.query.filter_by(username=username).first()
        if user and user.password==password :
            access_token=create_access_token(identity=user.id)

            return {'access_token':access_token},200
       
        return {"meaasge":'invalid credential'},401
    
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id=get_jwt_identity()
        return {'mesage':f'hello user{current_user_id}you access aprotected resourse'},200



api.add_resource(UserRegistration,'/register')
api.add_resource(UserLogin,'/login')
api.add_resource(ProtectedResource,'/secure')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
