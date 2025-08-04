from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "version":"v2"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "version":"v2"}
]

echo "# trigger build"

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "flask-demo-app",
        "version": "1.0.0"
    }), 200

@app.route('/users', methods=['GET'])
def get_users():
    """GET endpoint to retrieve all users"""
    return jsonify({
        "success": True,
        "data": users,
        "count": len(users)
    }), 200

@app.route('/users', methods=['POST'])
def create_user():
    """POST endpoint to create a new user"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({
                "success": False,
                "error": "Missing required fields: name and email"
            }), 400
        
        # Create new user
        new_user = {
            "id": len(users) + 1,
            "name": data['name'],
            "email": data['email']
        }
        
        # Add to users list
        users.append(new_user)
        
        return jsonify({
            "success": True,
            "message": "User created successfully",
            "data": new_user
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        "message": "Flask Demo API",
        "endpoints": {
            "health": "GET /health",
            "get_users": "GET /users",
            "create_user": "POST /users"
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)