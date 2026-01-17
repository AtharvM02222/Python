#!/usr/bin/env python3
import sys
import configparser
sys.path.insert(0, '.')

from osint_instagram import InstagramOSINT

# Read credentials from config file
config = configparser.ConfigParser()
config.read('Osintgram/config/credentials.ini')

USERNAME = config.get('Credentials', 'username').strip()
PASSWORD = config.get('Credentials', 'password').strip()

# Get target from command line or default
TARGET = sys.argv[1] if len(sys.argv) > 1 else "ftt.khushi"

osint = InstagramOSINT(TARGET)

print(f"Logging in as {USERNAME}...")
if osint.login(USERNAME, PASSWORD):
    print("✓ Login successful!\n")
    osint.likes()
else:
    print("✗ Login failed")
