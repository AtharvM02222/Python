#!/usr/bin/env python3
"""
Holehe - Check if email is registered on various sites
Install: pip3 install holehe
"""

import subprocess
import sys

def check_email(email):
    """Check email across multiple platforms"""
    print(f"\n{'='*60}")
    print(f"Checking email: {email}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(['holehe', email], capture_output=True, text=True)
        print(result.stdout)
    except FileNotFoundError:
        print("Holehe not installed. Install with:")
        print("  pip3 install holehe")
        print("\nThen run:")
        print(f"  holehe {email}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python holehe_tool.py <email>")
        print("Example: python holehe_tool.py test@gmail.com\n")
        sys.exit(1)
    
    check_email(sys.argv[1])
