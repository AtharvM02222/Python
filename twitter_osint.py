#!/usr/bin/env python3
"""
Twitter/X OSINT Tool
Uses twint (no API key needed)
Install: pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
"""

import subprocess
import sys

def twitter_lookup(username, command="info"):
    """Lookup Twitter/X user"""
    
    commands = {
        "info": f"twint -u {username} --user-full",
        "tweets": f"twint -u {username} -l 20",
        "followers": f"twint -u {username} --followers",
        "following": f"twint -u {username} --following",
        "search": f"twint -s 'from:{username}' -l 20"
    }
    
    if command not in commands:
        print(f"Unknown command: {command}")
        print("Available: info, tweets, followers, following, search")
        return
    
    print(f"\n{'='*60}")
    print(f"Twitter OSINT: @{username} - {command}")
    print(f"{'='*60}\n")
    
    try:
        subprocess.run(commands[command], shell=True)
    except Exception as e:
        print(f"Error: {e}")
        print("\nInstall twint with:")
        print("  pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\nUsage: python twitter_osint.py <username> [command]")
        print("\nCommands:")
        print("  info      - User information")
        print("  tweets    - Recent tweets")
        print("  followers - Followers list")
        print("  following - Following list")
        print("  search    - Search user's tweets")
        print("\nExample:")
        print("  python twitter_osint.py elonmusk info\n")
        sys.exit(1)
    
    username = sys.argv[1].replace('@', '')
    command = sys.argv[2] if len(sys.argv) > 2 else "info"
    twitter_lookup(username, command)
