import re
from flask import request, abort, jsonify
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

def check_ip_blocking():
    """ Block or allow requests based on IP addresses. """
    ip = request.remote_addr

    if ip in blocked_ips:
        print(f"Blocked IP attempt: {ip}")
        abort(403, "Your IP address has been blocked due to suspicious activity.")
    
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
            print(f"Rate limit exceeded for {ip}")
            abort(429, "Too many requests. Please slow down.")

def waf_middleware():
    """ Advanced WAF Middleware """
    check_ip_blocking()
    rate_limit_check()

    # Get request data (query parameters and form data)
    request_data = request.args.to_dict()
    form_data = request.form.to_dict()
    data = {**request_data, **form_data}

    # Inspect request for SQL Injection and XSS
    for value in data.values():
        for pattern in attack_patterns['sql_injection']:
            if re.search(pattern, value, re.IGNORECASE):
                print(f"SQL Injection attempt detected: {value}")
                abort(403, "Request blocked due to suspicious activity.")
        
        for pattern in attack_patterns['xss']:
            if re.search(pattern, value, re.IGNORECASE):
                print(f"XSS attempt detected: {value}")
                abort(403, "Request blocked due to XSS attack attempt.")

def enforce_allowed_methods(allowed_methods):
    """ Enforce allowed HTTP methods on routes """
    if request.method not in allowed_methods:
        abort(405, f"Method {request.method} not allowed on this route.")

def check_file_uploads():
    """ Inspect file uploads to block dangerous files """
    if 'file' in request.files:
        file = request.files['file']
        if file:
            # Example: Only allow text and image file types
            allowed_extensions = ['txt', 'png', 'jpg', 'jpeg', 'gif']
            if not file.filename.split('.')[-1] in allowed_extensions:
                print(f"Blocked dangerous file upload attempt: {file.filename}")
                abort(403, "File type not allowed.")
    
# Example of how to use allowed methods enforcement
def apply_http_method_restrictions():
    enforce_allowed_methods(['GET', 'POST'])

def log_request_details():
    """ Log the details of suspicious requests for auditing """
    print(f"Suspicious request from {request.remote_addr}")
    print(f"Path: {request.path}")
    print(f"Method: {request.method}")
    print(f"User-Agent: {request.user_agent}")
    print(f"Data: {request.args} | {request.form}")

