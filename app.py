#!/usr/bin/env python3
"""
Flask Web App for Router SMS Reader
"""

from flask import Flask, render_template, request, jsonify, session
from router_script import get_auth_cookies, get_latest_sms_messages
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/', methods=['GET', 'POST'])
def index():
    messages = []
    error = None
    
    if request.method == 'POST':
        router_ip = request.form.get('router_ip')
        admin_password = request.form.get('admin_password')
        
        if not router_ip or not admin_password:
            error = "Please enter both IP address and password"
        else:
            try:
                # Get authentication cookies
                auth_cookies = get_auth_cookies(router_ip, admin_password)
                
                # Get SMS messages
                messages = get_latest_sms_messages(router_ip, auth_cookies, n=10)
                
                # Don't store password in session!
                session['last_router_ip'] = router_ip
                
            except Exception as e:
                error = f"Error: {str(e)}"
    else:
        # Pre-fill with last used IP if available
        router_ip = session.get('last_router_ip', '')
    
    return render_template('index.html', messages=messages, error=error, router_ip=router_ip)

@app.route('/api/messages', methods=['POST'])
def api_messages():
    """API endpoint for getting messages (returns JSON)"""
    data = request.get_json()
    router_ip = data.get('router_ip')
    admin_password = data.get('admin_password')
    
    if not router_ip or not admin_password:
        return jsonify({'error': 'Missing IP or password'}), 400
    
    try:
        auth_cookies = get_auth_cookies(router_ip, admin_password)
        messages = get_latest_sms_messages(router_ip, auth_cookies, n=10)
        return jsonify({'messages': messages})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)