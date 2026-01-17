#!/usr/bin/env python3
"""
Instagram User Info Tool using Instaloader
More reliable than Osintgram for basic info gathering
"""

import instaloader
import sys
from datetime import datetime

def get_user_info(username):
    """Fetch Instagram user information"""
    
    # Create instance
    L = instaloader.Instaloader()
    
    try:
        # Load profile
        profile = instaloader.Profile.from_username(L.context, username)
        
        print(f"\n{'='*50}")
        print(f"Instagram Profile: @{profile.username}")
        print(f"{'='*50}\n")
        
        print(f"Full Name:        {profile.full_name}")
        print(f"Biography:        {profile.biography}")
        print(f"Followers:        {profile.followers:,}")
        print(f"Following:        {profile.followees:,}")
        print(f"Posts:            {profile.mediacount:,}")
        print(f"Is Verified:      {'✓' if profile.is_verified else '✗'}")
        print(f"Is Private:       {'✓' if profile.is_private else '✗'}")
        print(f"Is Business:      {'✓' if profile.is_business_account else '✗'}")
        
        if profile.external_url:
            print(f"Website:          {profile.external_url}")
        
        if profile.business_category_name:
            print(f"Business Type:    {profile.business_category_name}")
        
        print(f"\nProfile URL:      https://instagram.com/{profile.username}")
        print(f"Profile Pic:      {profile.profile_pic_url}")
        
        # Additional stats
        if profile.mediacount > 0:
            avg_likes = profile.get_posts().total_count
            print(f"\nEngagement:       ~{profile.followers / profile.mediacount:.0f} followers per post")
        
        print(f"\n{'='*50}\n")
        
        return True
        
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"\n❌ Error: Profile '@{username}' does not exist")
        return False
    except instaloader.exceptions.ConnectionException as e:
        print(f"\n❌ Connection Error: {e}")
        print("Try again in a few minutes (rate limit)")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python instagram_info.py <username>")
        print("Example: python instagram_info.py cristiano")
        sys.exit(1)
    
    username = sys.argv[1].replace('@', '')
    get_user_info(username)

if __name__ == "__main__":
    main()
