from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
import jwt
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

@app.route("/authentication", methods=["POST"])
def authentication():
    
    hardcoded_csrf_token = "9394949"
    encoded_jwt = jwt.encode(
        {
            "id": request.json["id"],
            "password": request.json["password"]
        },
        "secret", algorithm="HS256")
    response = make_response(jsonify({"status": "Logged in", "csrf_token": hardcoded_csrf_token}), 200)
    response.set_cookie(key="token", value=encoded_jwt, httponly=True, secure=True, samesite="None")
    response.set_cookie(key="csrf_token", value=hardcoded_csrf_token, httponly=True, secure=True, samesite="None")
    
    return response

@app.route("/get_info", methods=["GET"])
def get_info():
    csrf_token_match = request.headers.get('csrf_token') and request.headers.get('csrf_token') == request.cookies.get('csrf_token')
    if csrf_token_match:
        payload = jwt.decode(request.cookies.get("token"), "secret", algorithms="HS256")
        return f"Hello, {payload['id']}"
    return jsonify({"status": "Unauthorized"}), 401

if __name__ == "__main__":
    app.run(ssl_context=("../certification/cert.crt", "../certification/cert.key")
            if os.path.exists("../certification/cert.crt") else None, threaded=True, debug=True)
 