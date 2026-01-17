#!/usr/bin/env python3
"""
Modern Instagram OSINT Tool
Works without login for public profiles
"""

import instaloader
import sys
import json
import os
from datetime import datetime
from collections import Counter

class InstagramOSINT:
    def __init__(self, username=None):
        self.L = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False
        )
        self.target = username
        self.profile = None
        
    def login(self, username, password):
        """Login to Instagram (optional, for private accounts)"""
        try:
            self.L.login(username, password)
            print(f"✓ Logged in as {username}")
            return True
        except Exception as e:
            print(f"✗ Login failed: {e}")
            return False
        
    def get_profile(self, username=None):
        """Get profile object"""
        if username is None:
            username = self.target
        try:
            if self.profile is None or self.profile.username != username:
                self.profile = instaloader.Profile.from_username(self.L.context, username)
            return self.profile
        except Exception as e:
            print(f"Error loading profile: {e}")
            return None
    
    def info(self, username=None):
        """Get detailed profile information"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        print(f"\n{'='*60}")
        print(f"PROFILE INFORMATION: @{profile.username}")
        print(f"{'='*60}\n")
        
        print(f"Full Name:          {profile.full_name}")
        print(f"Biography:          {profile.biography}")
        print(f"Followers:          {profile.followers:,}")
        print(f"Following:          {profile.followees:,}")
        print(f"Total Posts:        {profile.mediacount:,}")
        print(f"Is Verified:        {'✓ Yes' if profile.is_verified else '✗ No'}")
        print(f"Is Private:         {'✓ Yes' if profile.is_private else '✗ No'}")
        print(f"Is Business:        {'✓ Yes' if profile.is_business_account else '✗ No'}")
        
        if profile.external_url:
            print(f"External URL:       {profile.external_url}")
        
        if profile.business_category_name:
            print(f"Business Category:  {profile.business_category_name}")
        
        print(f"\nProfile URL:        https://instagram.com/{profile.username}")
        print(f"Profile Picture:    {profile.profile_pic_url}")
        print(f"User ID:            {profile.userid}")
        
        # Engagement metrics
        if profile.mediacount > 0:
            ratio = profile.followers / profile.followees if profile.followees > 0 else 0
            print(f"\nFollower/Following: {ratio:.2f}")
            print(f"Avg per post:       {profile.followers / profile.mediacount:.0f} followers")
        
        print(f"\n{'='*60}\n")
    
    def followers(self, username=None, limit=50):
        """Get followers list"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        print(f"\n{'='*60}")
        print(f"FOLLOWERS: @{profile.username}")
        print(f"{'='*60}\n")
        
        try:
            count = 0
            for follower in profile.get_followers():
                if count >= limit:
                    break
                print(f"  @{follower.username} - {follower.full_name}")
                count += 1
            print(f"\nShowing {count} of {profile.followers:,} followers")
        except Exception as e:
            print(f"Error: {e}")
        
        print(f"\n{'='*60}\n")
    
    def followings(self, username=None, limit=50):
        """Get following list"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        print(f"\n{'='*60}")
        print(f"FOLLOWING: @{profile.username}")
        print(f"{'='*60}\n")
        
        try:
            count = 0
            for followee in profile.get_followees():
                if count >= limit:
                    break
                print(f"  @{followee.username} - {followee.full_name}")
                count += 1
            print(f"\nShowing {count} of {profile.followees:,} following")
        except Exception as e:
            print(f"Error: {e}")
        
        print(f"\n{'='*60}\n")
    
    def posts(self, username=None, limit=10):
        """Get recent posts"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        print(f"\n{'='*60}")
        print(f"RECENT POSTS: @{profile.username}")
        print(f"{'='*60}\n")
        
        try:
            count = 0
            for post in profile.get_posts():
                if count >= limit:
                    break
                
                print(f"\nPost #{count + 1}")
                print(f"  Date:     {post.date_local}")
                print(f"  Likes:    {post.likes:,}")
                print(f"  Comments: {post.comments:,}")
                print(f"  Caption:  {post.caption[:100] if post.caption else 'No caption'}...")
                print(f"  URL:      https://instagram.com/p/{post.shortcode}")
                
                if post.is_video:
                    print(f"  Type:     Video ({post.video_view_count:,} views)")
                else:
                    print(f"  Type:     Photo")
                
                count += 1
            
            if count == 0:
                print("  No posts found or account is private and you don't follow them")
        except Exception as e:
            print(f"  Error: {e}")
            print(f"  Note: Make sure you follow this account and they accepted your request")
        
        print(f"\n{'='*60}\n")
    
    def tagged(self, username=None, limit=10):
        """Get posts where user is tagged"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        if profile.is_private:
            print(f"\n⚠️  Account is private. Cannot access tagged posts.\n")
            return
        
        print(f"\n{'='*60}")
        print(f"TAGGED POSTS: @{profile.username}")
        print(f"{'='*60}\n")
        
        try:
            count = 0
            for post in profile.get_tagged_posts():
                if count >= limit:
                    break
                
                print(f"\nTagged Post #{count + 1}")
                print(f"  By:       @{post.owner_username}")
                print(f"  Date:     {post.date_local}")
                print(f"  Likes:    {post.likes:,}")
                print(f"  URL:      https://instagram.com/p/{post.shortcode}")
                
                count += 1
            
            if count == 0:
                print("  No tagged posts found")
        except Exception as e:
            print(f"Error: {e}")
        
        print(f"\n{'='*60}\n")
    
    def comments(self, username=None, limit=10):
        """Get comments from recent posts"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        if profile.is_private:
            print(f"\n⚠️  Account is private. Cannot access comments.\n")
            return
        
        print(f"\n{'='*60}")
        print(f"RECENT COMMENTS: @{profile.username}")
        print(f"{'='*60}\n")
        
        try:
            post_count = 0
            for post in profile.get_posts():
                if post_count >= 5:  # Check last 5 posts
                    break
                
                print(f"\nPost: https://instagram.com/p/{post.shortcode}")
                comment_count = 0
                for comment in post.get_comments():
                    if comment_count >= limit:
                        break
                    print(f"  @{comment.owner.username}: {comment.text[:80]}")
                    comment_count += 1
                
                post_count += 1
        except Exception as e:
            print(f"Error: {e}")
        
        print(f"\n{'='*60}\n")
    
    def hashtags(self, username=None, limit=20):
        """Extract hashtags from recent posts"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        if profile.is_private:
            print(f"\n⚠️  Account is private. Cannot access posts.\n")
            return
        
        print(f"\n{'='*60}")
        print(f"HASHTAGS USED: @{profile.username}")
        print(f"{'='*60}\n")
        
        hashtags = {}
        count = 0
        
        for post in profile.get_posts():
            if count >= limit:
                break
            
            if post.caption:
                words = post.caption.split()
                for word in words:
                    if word.startswith('#'):
                        tag = word.lower().rstrip('.,!?')
                        hashtags[tag] = hashtags.get(tag, 0) + 1
            
            count += 1
        
        if hashtags:
            sorted_tags = sorted(hashtags.items(), key=lambda x: x[1], reverse=True)
            for tag, count in sorted_tags:
                print(f"  {tag}: {count} times")
        else:
            print("  No hashtags found")
        
        print(f"\n{'='*60}\n")
    
    def captions(self, username=None, limit=10):
        """Get captions from recent posts"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        if profile.is_private:
            print(f"\n⚠️  Account is private. Cannot access captions.\n")
            return
        
        print(f"\n{'='*60}")
        print(f"CAPTIONS: @{profile.username}")
        print(f"{'='*60}\n")
        
        count = 0
        for post in profile.get_posts():
            if count >= limit:
                break
            
            if post.caption:
                print(f"\nPost {count + 1} ({post.date_local.strftime('%Y-%m-%d')}):")
                print(f"  {post.caption}\n")
            
            count += 1
        
        print(f"\n{'='*60}\n")
    
    def likes(self, username=None, limit=10):
        """Get likes statistics from recent posts"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        print(f"\n{'='*60}")
        print(f"LIKES STATISTICS: @{profile.username}")
        print(f"{'='*60}\n")
        
        try:
            likes_list = []
            count = 0
            
            for post in profile.get_posts():
                if count >= limit:
                    break
                likes_list.append(post.likes)
                print(f"  Post {count + 1}: {post.likes:,} likes ({post.date_local.strftime('%Y-%m-%d')})")
                count += 1
            
            if likes_list:
                avg_likes = sum(likes_list) / len(likes_list)
                print(f"\n  Average: {avg_likes:,.0f} likes")
                print(f"  Max:     {max(likes_list):,} likes")
                print(f"  Min:     {min(likes_list):,} likes")
            else:
                print("  No posts found")
        except Exception as e:
            print(f"  Error: {e}")
            print(f"  Note: Make sure you follow this account and they accepted your request")
        
        print(f"\n{'='*60}\n")
    
    def photodes(self, username=None, limit=10):
        """Download photos (metadata only)"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        if profile.is_private:
            print(f"\n⚠️  Account is private. Cannot access photos.\n")
            return
        
        print(f"\n{'='*60}")
        print(f"PHOTOS: @{profile.username}")
        print(f"{'='*60}\n")
        
        count = 0
        for post in profile.get_posts():
            if count >= limit:
                break
            
            if not post.is_video:
                print(f"\nPhoto {count + 1}:")
                print(f"  URL:   {post.url}")
                print(f"  Date:  {post.date_local}")
                print(f"  Likes: {post.likes:,}")
                count += 1
        
        print(f"\n{'='*60}\n")
    
    def stories(self, username=None):
        """Get user stories (requires login)"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        print(f"\n{'='*60}")
        print(f"STORIES: @{profile.username}")
        print(f"{'='*60}\n")
        
        try:
            stories = self.L.get_stories(userids=[profile.userid])
            count = 0
            for story in stories:
                for item in story.get_items():
                    print(f"\nStory {count + 1}:")
                    print(f"  Date: {item.date_local}")
                    print(f"  Type: {'Video' if item.is_video else 'Photo'}")
                    print(f"  URL:  {item.url}")
                    count += 1
            
            if count == 0:
                print("  No active stories")
        except Exception as e:
            print(f"Error: {e}")
            print("Note: Stories require login")
        
        print(f"\n{'='*60}\n")
    
    def propic(self, username=None):
        """Get profile picture"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        print(f"\n{'='*60}")
        print(f"PROFILE PICTURE: @{profile.username}")
        print(f"{'='*60}\n")
        print(f"  URL: {profile.profile_pic_url}")
        print(f"\n{'='*60}\n")
    
    def fwersemail(self, username=None):
        """Get followers with email in bio"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        print(f"\n{'='*60}")
        print(f"FOLLOWERS WITH EMAIL: @{profile.username}")
        print(f"{'='*60}\n")
        
        try:
            count = 0
            found = 0
            for follower in profile.get_followers():
                if count >= 100:  # Limit to avoid rate limits
                    break
                
                follower_profile = instaloader.Profile.from_username(self.L.context, follower.username)
                if follower_profile.biography and '@' in follower_profile.biography:
                    print(f"  @{follower.username}: {follower_profile.biography}")
                    found += 1
                
                count += 1
            
            print(f"\nFound {found} followers with email in bio (checked {count})")
        except Exception as e:
            print(f"Error: {e}")
        
        print(f"\n{'='*60}\n")
    
    def fwingsemail(self, username=None):
        """Get followings with email in bio"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        print(f"\n{'='*60}")
        print(f"FOLLOWINGS WITH EMAIL: @{profile.username}")
        print(f"{'='*60}\n")
        
        try:
            count = 0
            found = 0
            for followee in profile.get_followees():
                if count >= 100:
                    break
                
                followee_profile = instaloader.Profile.from_username(self.L.context, followee.username)
                if followee_profile.biography and '@' in followee_profile.biography:
                    print(f"  @{followee.username}: {followee_profile.biography}")
                    found += 1
                
                count += 1
            
            print(f"\nFound {found} followings with email in bio (checked {count})")
        except Exception as e:
            print(f"Error: {e}")
        
        print(f"\n{'='*60}\n")
    
    def addrs(self, username=None, limit=10):
        """Get addresses from posts"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        if profile.is_private:
            print(f"\n⚠️  Account is private. Cannot access posts.\n")
            return
        
        print(f"\n{'='*60}")
        print(f"LOCATIONS: @{profile.username}")
        print(f"{'='*60}\n")
        
        count = 0
        found = 0
        for post in profile.get_posts():
            if count >= limit:
                break
            
            if post.location:
                print(f"\n  Location: {post.location.name}")
                print(f"  Post:     https://instagram.com/p/{post.shortcode}")
                found += 1
            
            count += 1
        
        if found == 0:
            print("  No locations found")
        
        print(f"\n{'='*60}\n")
    
    def wcommented(self, username=None, limit=10):
        """Get users who commented on posts"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        if profile.is_private:
            print(f"\n⚠️  Account is private. Cannot access comments.\n")
            return
        
        print(f"\n{'='*60}")
        print(f"USERS WHO COMMENTED: @{profile.username}")
        print(f"{'='*60}\n")
        
        commenters = Counter()
        
        try:
            post_count = 0
            for post in profile.get_posts():
                if post_count >= 10:
                    break
                
                for comment in post.get_comments():
                    commenters[comment.owner.username] += 1
                
                post_count += 1
            
            for user, count in commenters.most_common(limit):
                print(f"  @{user}: {count} comments")
        except Exception as e:
            print(f"Error: {e}")
        
        print(f"\n{'='*60}\n")
    
    def wtagged(self, username=None, limit=10):
        """Get users who are tagged in posts"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        if profile.is_private:
            print(f"\n⚠️  Account is private. Cannot access posts.\n")
            return
        
        print(f"\n{'='*60}")
        print(f"USERS TAGGED: @{profile.username}")
        print(f"{'='*60}\n")
        
        tagged_users = Counter()
        
        try:
            count = 0
            for post in profile.get_posts():
                if count >= limit:
                    break
                
                for tag in post.tagged_users:
                    tagged_users[tag.username] += 1
                
                count += 1
            
            if tagged_users:
                for user, count in tagged_users.most_common():
                    print(f"  @{user}: tagged {count} times")
            else:
                print("  No tagged users found")
        except Exception as e:
            print(f"Error: {e}")
        
        print(f"\n{'='*60}\n")
    
    def interactive_mode(self, username):
        """Interactive OSINT mode"""
        profile = self.get_profile(username)
        if not profile:
            return
        
        while True:
            print(f"\n{'='*60}")
            print(f"Instagram OSINT Tool - @{username}")
            print(f"{'='*60}")
            print("\nAvailable Commands:")
            print("  info          - Show profile information")
            print("  followers     - List followers")
            print("  followings    - List followings")
            print("  posts         - Show recent posts")
            print("  tagged        - Show tagged posts")
            print("  comments      - Show comments")
            print("  hashtags      - Show hashtags used")
            print("  captions      - Show post captions")
            print("  likes         - Show likes statistics")
            print("  photodes      - Show photos")
            print("  stories       - Show stories (requires login)")
            print("  propic        - Show profile picture")
            print("  addrs         - Show locations from posts")
            print("  wcommented    - Show who commented")
            print("  wtagged       - Show who is tagged")
            print("  fwersemail    - Followers with email")
            print("  fwingsemail   - Followings with email")
            print("  list          - Show this menu")
            print("  exit          - Exit")
            print(f"{'='*60}\n")
            
            choice = input("Enter command: ").strip().lower()
            
            if choice == 'info':
                self.info()
            elif choice == 'followers':
                self.followers()
            elif choice == 'followings':
                self.followings()
            elif choice == 'posts':
                self.posts()
            elif choice == 'tagged':
                self.tagged()
            elif choice == 'comments':
                self.comments()
            elif choice == 'hashtags':
                self.hashtags()
            elif choice == 'captions':
                self.captions()
            elif choice == 'likes':
                self.likes()
            elif choice == 'photodes':
                self.photodes()
            elif choice == 'stories':
                self.stories()
            elif choice == 'propic':
                self.propic()
            elif choice == 'addrs':
                self.addrs()
            elif choice == 'wcommented':
                self.wcommented()
            elif choice == 'wtagged':
                self.wtagged()
            elif choice == 'fwersemail':
                self.fwersemail()
            elif choice == 'fwingsemail':
                self.fwingsemail()
            elif choice == 'list':
                continue
            elif choice in ['exit', 'quit', 'q']:
                print("\nGoodbye!\n")
                break
            else:
                print("\n❌ Invalid command. Type 'list' to see all commands.\n")

def main():
    if len(sys.argv) < 2:
        print("\nInstagram OSINT Tool")
        print("="*60)
        print("\nUsage:")
        print("  python osint_instagram.py <username>                - Interactive mode")
        print("  python osint_instagram.py <username> <command>      - Run specific command")
        print("  python osint_instagram.py -l <username>             - Login and interactive mode")
        print("\nCommands:")
        print("  info, followers, followings, posts, tagged, comments")
        print("  hashtags, captions, likes, photodes, stories, propic")
        print("  addrs, wcommented, wtagged, fwersemail, fwingsemail")
        print("\nExamples:")
        print("  python osint_instagram.py cristiano")
        print("  python osint_instagram.py cristiano info")
        print("  python osint_instagram.py -l ftt.khushi  (for private accounts)\n")
        sys.exit(1)
    
    # Check for login flag
    login_mode = False
    if sys.argv[1] == '-l' and len(sys.argv) >= 3:
        login_mode = True
        username = sys.argv[2].replace('@', '')
        osint = InstagramOSINT(username)
        
        # Prompt for login
        print("\n⚠️  Login required for private accounts")
        ig_user = input("Your Instagram username: ").strip()
        ig_pass = input("Your Instagram password: ").strip()
        
        if osint.login(ig_user, ig_pass):
            print("✓ Login successful!\n")
        else:
            print("✗ Login failed. Continuing without login...\n")
        
        # Interactive mode after login
        osint.interactive_mode(username)
        sys.exit(0)
    
    username = sys.argv[1].replace('@', '')
    osint = InstagramOSINT(username)
    
    if len(sys.argv) == 2:
        # Interactive mode
        osint.interactive_mode(username)
    else:
        command = sys.argv[2].lower()
        
        # Map commands to methods
        commands = {
            'info': osint.info,
            'followers': osint.followers,
            'followings': osint.followings,
            'posts': osint.posts,
            'tagged': osint.tagged,
            'comments': osint.comments,
            'hashtags': osint.hashtags,
            'captions': osint.captions,
            'likes': osint.likes,
            'photodes': osint.photodes,
            'stories': osint.stories,
            'propic': osint.propic,
            'addrs': osint.addrs,
            'wcommented': osint.wcommented,
            'wtagged': osint.wtagged,
            'fwersemail': osint.fwersemail,
            'fwingsemail': osint.fwingsemail,
        }
        
        if command in commands:
            commands[command]()
        else:
            print(f"\n❌ Unknown command: {command}")
            print("Run without command to see all available commands\n")

if __name__ == "__main__":
    main()
