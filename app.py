from flask import Flask, request, jsonify, render_template
import uuid
import bcrypt

app = Flask(__name__, template_folder='templates')

# In-memory user storage for demonstration purposes
users = {}

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400

        if username in users:
            return jsonify({'status': 'error', 'message': 'User already exists'}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users[username] = {
            'password': hashed_password,
            'preferences': {}
        }
        return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400

        user = users.get(username)
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401

        token = str(uuid.uuid4())
        return jsonify({'status': 'success', 'token': token, 'user': {'username': username, 'preferences': user['preferences']}}), 200

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5001)