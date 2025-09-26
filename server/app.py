from flask import Flask, request, session, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from models import db, User, Article  # use your models.py

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "super-secret-key"

# Bind the existing db instance to this app
db.init_app(app)
api = Api(app)

# -------------------------
# Authentication Resources
# -------------------------
class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            session['user_id'] = user.id
            return jsonify({'id': user.id, 'username': user.username})
        return jsonify({'error': 'User not found'}), 404

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return '', 204

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            return {'id': user.id, 'username': user.username}, 200
        # Return empty JSON object with 401 status
        return {}, 401

# -------------------------
# Optional /clear route for tests
# -------------------------
@app.route('/clear')
def clear_session():
    session.clear()
    return '', 204

# -------------------------
# API Routes
# -------------------------
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

# -------------------------
# Run server
# -------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # make sure tables exist
    app.run(port=5555, debug=True)

