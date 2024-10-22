import re
from flask import request, abort, jsonify
from functools import wraps
from time import time

# Dictionary to hold rate limiting data (e.g., IP: [request_count, first_request_time])
rate_limit_data = {}

# Rate limiting configuration (max 100 requests per minute per IP)
RATE_LIMIT_MAX_REQUESTS = 100
RATE_LIMIT_PERIOD = 60  # 60 seconds

# List of known malicious IPs (for demo purposes)
blocked_ips = ['192.168.1.100', '10.0.0.100']

# List of whitelisted IPs
whitelisted_ips = ['127.0.0.1']

# Define advanced attack patterns for SQL injection, XSS, etc.
attack_patterns = {
    'sql_injection': [
        r"(?:')|(?:--)|(/\\*(?:.|[\\n\\r])*?\\*/)|(\b(select|union|insert|update|delete|drop|exec|grant|alter|truncate)\b)",
        r"(\b(and|or)\b.+?(>|<|=|!))", 
        r"(\bunion\b.+?\bselect\b)", 
        r"select.+from", 
        r"insert.+into", 
        r"delete.+from"
    ],
    'xss': [
        r"(<|%3C)(script|img|iframe|object|embed|svg|form|body|input|link|style|meta)(>|%3E)", 
        r"(onload=|onerror=|javascript:|vbscript:|data:text|src=|href=)", 
        r"<.*?(alert|prompt|confirm).*?>"
    ]
}

def apply_middleware(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        check_ip_blocking()
        rate_limit_check()
        waf_middleware()
        return func(*args, **kwargs)
    return wrapper

def check_ip_blocking():
    """ Block or allow requests based on IP addresses. """
    ip = request.remote_addr
    if ip in blocked_ips:
        log_request_details(reason="Blocked IP")
        abort(403, jsonify({"error": "Your IP address has been blocked due to suspicious activity."}))
    
    if ip in whitelisted_ips:
        print(f"Whitelisted IP detected: {ip}")
        return  # Allow trusted IPs without further checks

def rate_limit_check():
    """ Simple rate limiting to prevent brute force attacks. """
    ip = request.remote_addr
    current_time = time()

    if ip not in rate_limit_data:
        rate_limit_data[ip] = [1, current_time]
    else:
        request_count, first_request_time = rate_limit_data[ip]
        
        # If time period is within limit
        if current_time - first_request_time <= RATE_LIMIT_PERIOD:
            rate_limit_data[ip][0] += 1
        else:
            rate_limit_data[ip] = [1, current_time]

        # Check rate limit
        if rate_limit_data[ip][0] > RATE_LIMIT_MAX_REQUESTS:
            log_request_details(reason="Rate limit exceeded")
            abort(429, jsonify({"error": "Too many requests. Please slow down."}))

def waf_middleware():
    """ Advanced WAF Middleware """
    # Get request data (query parameters and form data)
    data = {**request.args.to_dict(), **request.form.to_dict()}

    # Inspect request for SQL Injection and XSS
    for value in data.values():
        check_attack_patterns(value)

def check_attack_patterns(value):
    """ Check for malicious patterns (SQL Injection, XSS) in the request. """
    for pattern in attack_patterns['sql_injection']:
        if re.search(pattern, value, re.IGNORECASE):
            log_request_details(reason="SQL Injection attempt", data=value)
            abort(403, jsonify({"error": "Request blocked due to suspicious activity."}))
    
    for pattern in attack_patterns['xss']:
        if re.search(pattern, value, re.IGNORECASE):
            log_request_details(reason="XSS attempt", data=value)
            abort(403, jsonify({"error": "Request blocked due to XSS attack attempt."}))

def enforce_allowed_methods(allowed_methods):
    """ Enforce allowed HTTP methods on routes """
    if request.method not in allowed_methods:
        log_request_details(reason="Disallowed method")
        abort(405, jsonify({"error": f"Method {request.method} not allowed on this route."}))

def check_file_uploads():
    """ Inspect file uploads to block dangerous files """
    if 'file' in request.files:
        file = request.files['file']
        if file:
            # Example: Only allow text and image file types
            allowed_extensions = ['txt', 'png', 'jpg', 'jpeg', 'gif']
            if not file.filename.split('.')[-1].lower() in allowed_extensions:
                log_request_details(reason="Blocked dangerous file upload", data=file.filename)
                abort(403, jsonify({"error": "File type not allowed."}))

def log_request_details(reason=None, data=None):
    """ Log the details of suspicious requests for auditing """
    log_entry = {
        'ip': request.remote_addr,
        'path': request.path,
        'method': request.method,
        'user_agent': request.user_agent.string,
        'reason': reason,
        'data': data
    }
    # Log this to a centralized log system (file, external service, etc.)
    print(f"Suspicious request logged: {log_entry}")
