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

# Get target from command line
TARGET = sys.argv[1] if len(sys.argv) > 1 else "ftt.khushi"

osint = InstagramOSINT(TARGET)

print(f"Logging in as {USERNAME}...")
if osint.login(USERNAME, PASSWORD):
    print("✓ Login successful!\n")
    
    # Get target profile
    profile = osint.get_profile(TARGET)
    if profile:
        print(f"Target: @{profile.username}")
        print(f"Private: {profile.is_private}")
        print(f"Followers: {profile.followers}")
        
        # Check if we follow them
        print(f"\nChecking if you follow @{TARGET}...")
        
        # Get our own profile
        my_profile = osint.get_profile(USERNAME)
        if my_profile:
            print(f"\nYour account: @{my_profile.username}")
            print(f"You follow: {my_profile.followees} accounts")
            
            # Check if target is in our following list
            print(f"\nSearching your following list for @{TARGET}...")
            found = False
            count = 0
            for followee in my_profile.get_followees():
                if followee.username == TARGET:
                    print(f"✓ You ARE following @{TARGET}")
                    found = True
                    break
                count += 1
                if count >= 100:  # Limit search
                    break
            
            if not found:
                print(f"✗ You are NOT following @{TARGET}")
                print(f"\nTo access private account data:")
                print(f"1. Follow @{TARGET} from Instagram app")
                print(f"2. Wait for them to accept your request")
                print(f"3. Run this tool again")
else:
    print("✗ Login failed")
