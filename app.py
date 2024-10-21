from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, JWTManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'SUPER-SECRET-KEY'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:usman123@localhost:3306/auth"

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# This will create all the tables defined above
with app.app_context():
    db.create_all()

class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'Missing username or password'}, 400
        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200

        return {'message': 'Invalid credentials'}, 401

# Fixing endpoint URLs
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')

@app.route('/')
def hello():
    return "Hello, Flask on macOS!"

if __name__ == '__main__':
    app.run(debug=True)
