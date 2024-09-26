#!/usr/bin/env python3

# Script for generating flask SECRET_KEY
import os
import base64

# Generate a random 24-byte secret key
secret_key = base64.urlsafe_b64encode(os.urandom(64)).decode('utf-8')

print("Your Flask SECRET_KEY is:", secret_key)