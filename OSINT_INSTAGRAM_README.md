# Instagram OSINT Tool

A comprehensive Instagram OSINT (Open Source Intelligence) tool with all the features from Osintgram, but actually working with modern Instagram.

## Installation

```bash
pip3 install instaloader
```

## Usage

### Interactive Mode
```bash
python3 osint_instagram.py <username>
```

### Direct Commands
```bash
python3 osint_instagram.py <username> <command>
```

## Available Commands

### Basic Information
- **info** - Get profile information (followers, following, bio, etc.)
- **propic** - Get profile picture URL

### Followers & Following
- **followers** - List followers (up to 50)
- **followings** - List following (up to 50)
- **fwersemail** - Find followers with email in bio
- **fwingsemail** - Find followings with email in bio

### Posts & Content
- **posts** - Show recent posts with likes and comments
- **tagged** - Show posts where user is tagged
- **photodes** - Show photos from posts
- **stories** - Show active stories (requires login)
- **captions** - Show captions from recent posts
- **likes** - Show likes statistics

### Engagement
- **comments** - Show comments from recent posts
- **wcommented** - Show users who commented most
- **wtagged** - Show users tagged in posts

### Analysis
- **hashtags** - Extract and count hashtags used
- **addrs** - Show locations from posts

## Examples

```bash
# Get profile info
python3 osint_instagram.py cristiano info

# List followers
python3 osint_instagram.py cristiano followers

# Show recent posts
python3 osint_instagram.py cristiano posts

# Extract hashtags
python3 osint_instagram.py cristiano hashtags

# Interactive mode (all commands available)
python3 osint_instagram.py cristiano
```

## Features

✅ Works without login for public accounts
✅ All Osintgram commands implemented
✅ Modern and actively maintained
✅ No API deprecation issues
✅ Rate limit friendly
✅ Clean output format

## Notes

- **Private accounts**: Most commands require the account to be public or you need to follow them
- **Stories**: Requires login to view
- **Rate limits**: The tool respects Instagram's rate limits to avoid blocks
- **Login**: Optional, only needed for private accounts or stories

## Comparison with Osintgram

| Feature | Osintgram | This Tool |
|---------|-----------|-----------|
| Works in 2026 | ❌ Broken | ✅ Yes |
| No login needed | ❌ Required | ✅ Optional |
| All commands | ✅ Yes | ✅ Yes |
| Active maintenance | ❌ No | ✅ Yes |
| Modern API | ❌ Deprecated | ✅ Current |

## Command Reference (Osintgram Compatible)

All original Osintgram commands are supported:
- info, followers, followings, posts, tagged, comments
- hashtags, captions, likes, photodes, stories, propic
- addrs, wcommented, wtagged, fwersemail, fwingsemail

Type `list` in interactive mode to see all commands.
