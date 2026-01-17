#!/usr/bin/env python3
"""
Simple Instagram OSINT with session management
"""
import instaloader
import configparser
import sys
import os

# Read credentials
config = configparser.ConfigParser()
config.read('Osintgram/config/credentials.ini')

USERNAME = config.get('Credentials', 'username').strip()
PASSWORD = config.get('Credentials', 'password').strip()
TARGET = sys.argv[1] if len(sys.argv) > 1 else "ftt.khushi"
COMMAND = sys.argv[2] if len(sys.argv) > 2 else "info"

# Create instaloader with session
L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    save_metadata=False,
    compress_json=False,
    max_connection_attempts=1
)

# Try to load session
session_file = f"session-{USERNAME}"
try:
    L.load_session_from_file(USERNAME, session_file)
    print(f"✓ Loaded session for {USERNAME}")
except:
    print(f"Logging in as {USERNAME}...")
    try:
        L.login(USERNAME, PASSWORD)
        L.save_session_to_file(session_file)
        print(f"✓ Logged in and saved session")
    except Exception as e:
        print(f"✗ Login failed: {e}")
        sys.exit(1)

# Get profile
try:
    profile = instaloader.Profile.from_username(L.context, TARGET)
    
    if COMMAND == "info":
        print(f"\n{'='*60}")
        print(f"Profile: @{profile.username}")
        print(f"{'='*60}")
        print(f"Name:      {profile.full_name}")
        print(f"Bio:       {profile.biography}")
        print(f"Followers: {profile.followers:,}")
        print(f"Following: {profile.followees:,}")
        print(f"Posts:     {profile.mediacount:,}")
        print(f"Private:   {profile.is_private}")
        print(f"{'='*60}\n")
    
    elif COMMAND == "likes":
        print(f"\n{'='*60}")
        print(f"Likes: @{profile.username}")
        print(f"{'='*60}\n")
        
        count = 0
        likes_list = []
        for post in profile.get_posts():
            if count >= 10:
                break
            print(f"Post {count+1}: {post.likes:,} likes - {post.date_local.strftime('%Y-%m-%d')}")
            likes_list.append(post.likes)
            count += 1
        
        if likes_list:
            print(f"\nAverage: {sum(likes_list)/len(likes_list):,.0f} likes")
            print(f"Max: {max(likes_list):,} likes")
            print(f"Min: {min(likes_list):,} likes")
        
        print(f"\n{'='*60}\n")
    
    elif COMMAND == "posts":
        print(f"\n{'='*60}")
        print(f"Posts: @{profile.username}")
        print(f"{'='*60}\n")
        
        count = 0
        for post in profile.get_posts():
            if count >= 10:
                break
            print(f"\nPost {count+1}:")
            print(f"  Date: {post.date_local}")
            print(f"  Likes: {post.likes:,}")
            print(f"  Comments: {post.comments:,}")
            print(f"  URL: https://instagram.com/p/{post.shortcode}")
            if post.caption:
                print(f"  Caption: {post.caption[:80]}...")
            count += 1
        
        print(f"\n{'='*60}\n")
    
    elif COMMAND == "followers":
        print(f"\n{'='*60}")
        print(f"Followers: @{profile.username}")
        print(f"{'='*60}\n")
        
        count = 0
        for follower in profile.get_followers():
            if count >= 50:
                break
            print(f"  @{follower.username} - {follower.full_name}")
            count += 1
        
        print(f"\nShowing {count} of {profile.followers:,} followers")
        print(f"\n{'='*60}\n")
    
    else:
        print(f"Unknown command: {COMMAND}")
        print("Available: info, likes, posts, followers")

except Exception as e:
    print(f"\nError: {e}")
    print("\nNote: If account is private, make sure:")
    print("1. You follow the account")
    print("2. They accepted your follow request")
    print("3. Wait a few minutes if you see rate limit errors\n")
