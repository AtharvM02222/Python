"""
Instagram User Info Finder
Fetches public information about Instagram users
"""

from instagrapi import Client
import json
import sys

def get_user_info(username):
    """
    Fetch public information about an Instagram user
    
    Args:
        username: Instagram username to lookup
    """
    try:
        cl = Client()
        
        # Get user info by username
        user_id = cl.user_id_from_username(username)
        user_info = cl.user_info(user_id)
        
        # Extract relevant information
        info = {
            "username": user_info.username,
            "full_name": user_info.full_name,
            "biography": user_info.biography,
            "followers": user_info.follower_count,
            "following": user_info.following_count,
            "posts": user_info.media_count,
            "is_verified": user_info.is_verified,
            "is_private": user_info.is_private,
            "profile_pic_url": user_info.profile_pic_url,
            "external_url": user_info.external_url,
            "is_business": user_info.is_business,
        }
        
        return info
        
    except Exception as e:
        return {"error": str(e)}

def main():
    if len(sys.argv) < 2:
        print("Usage: python instagram_user_finder.py <username>")
        sys.exit(1)
    
    username = sys.argv[1]
    print(f"\nFetching info for @{username}...\n")
    
    user_info = get_user_info(username)
    
    if "error" in user_info:
        print(f"Error: {user_info['error']}")
    else:
        print(json.dumps(user_info, indent=2))

if __name__ == "__main__":
    main()
