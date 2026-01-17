# OSINT Tools Collection

Complete collection of OSINT (Open Source Intelligence) tools for gathering information.

## 🔍 Available Tools

### 1. Instagram OSINT
**File:** `osint_instagram.py` or `ig_osint.py`

```bash
# Full featured tool
python3 osint_instagram.py <username> <command>

# Quick tool with session
python3 ig_osint.py <username> likes
python3 ig_osint.py <username> posts
python3 ig_osint.py <username> followers
```

**Commands:** info, followers, followings, posts, tagged, comments, hashtags, captions, likes, photodes, stories, propic, addrs, wcommented, wtagged, fwersemail, fwingsemail

---

### 2. Sherlock - Username Search
**Find username across 300+ social networks**

```bash
# Install
pip3 install sherlock-project

# Usage
sherlock username
sherlock ftt.khushi
```

Searches: Instagram, Twitter, Facebook, TikTok, GitHub, Reddit, YouTube, and 300+ more sites.

---

### 3. Holehe - Email Checker
**Check if email is registered on various platforms**

```bash
# Install
pip3 install holehe

# Usage
holehe email@example.com
python3 holehe_tool.py email@example.com
```

Checks: Instagram, Twitter, Snapchat, GitHub, Spotify, Netflix, Amazon, and more.

---

### 4. Phone Number OSINT
**File:** `phone_osint.py`

```bash
python3 phone_osint.py +919876543210
python3 phone_osint.py +14155552671
```

**Shows:**
- Country and region
- Carrier/operator
- Timezone
- Number type (mobile/landline)
- Formatted versions

---

### 5. IP Address OSINT
**File:** `ip_osint.py`

```bash
python3 ip_osint.py 8.8.8.8
python3 ip_osint.py 1.1.1.1
```

**Shows:**
- Geolocation (country, city, coordinates)
- ISP and organization
- Timezone
- Google Maps link
- Hostname

---

### 6. Twitter/X OSINT
**File:** `twitter_osint.py`

```bash
# Install twint
pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint

# Usage
python3 twitter_osint.py username info
python3 twitter_osint.py username tweets
python3 twitter_osint.py username followers
```

**Commands:** info, tweets, followers, following, search

---

## 🚀 Quick Start

### Install All Dependencies

```bash
# Instagram
pip3 install instaloader

# Username search
pip3 install sherlock-project

# Email checker
pip3 install holehe

# Phone numbers
pip3 install phonenumbers

# IP lookup (no install needed, uses requests)
pip3 install requests

# Twitter
pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
```

---

## 📋 Common Use Cases

### Find Someone's Online Presence
```bash
# 1. Search username across all platforms
sherlock username

# 2. Check Instagram
python3 osint_instagram.py username info

# 3. Check Twitter
python3 twitter_osint.py username info
```

### Email Investigation
```bash
# Check where email is registered
holehe email@example.com

# If found on Instagram, lookup profile
python3 osint_instagram.py username info
```

### Phone Number Lookup
```bash
# Get carrier and location
python3 phone_osint.py +1234567890
```

### IP Address Investigation
```bash
# Get location and ISP
python3 ip_osint.py 192.168.1.1
```

---

## ⚠️ Important Notes

### Rate Limits
- **Instagram:** Wait 10-15 minutes between heavy requests
- **Twitter:** Twint has built-in rate limiting
- **Sherlock:** Can take 2-5 minutes for full scan

### Privacy & Ethics
- Only use for legitimate purposes
- Respect privacy laws in your jurisdiction
- Don't harass or stalk people
- Public information only

### Login Requirements
- **Instagram private accounts:** Need to follow them first
- **Twitter:** No login needed with twint
- **Most tools:** Work without authentication

---

## 🛠️ Troubleshooting

### Instagram Rate Limit
```
Error: 401 Unauthorized - Please wait a few minutes
```
**Solution:** Wait 10-15 minutes, then try again

### Sherlock Too Slow
```bash
# Search specific sites only
sherlock username --site Instagram --site Twitter
```

### Phone Number Invalid
```
Make sure to include country code: +1234567890
```

### IP Lookup Failed
```bash
# Try different IP
python3 ip_osint.py 8.8.8.8
```

---

## 📚 Additional Resources

- **Instagram credentials:** Stored in `Osintgram/config/credentials.ini`
- **Session files:** Saved as `session-username` (reusable)
- **Output:** All tools print to console, redirect to file with `> output.txt`

---

## 🎯 Pro Tips

1. **Combine tools:** Use Sherlock first, then deep dive with specific tools
2. **Save sessions:** Instagram session files avoid repeated logins
3. **Batch processing:** Create scripts to check multiple targets
4. **Export data:** Redirect output to files for analysis
5. **Stay updated:** Tools get updated, reinstall periodically

---

## 📞 Tool Comparison

| Tool | Speed | Login Required | Data Depth | Best For |
|------|-------|----------------|------------|----------|
| Sherlock | Medium | No | Shallow | Username discovery |
| Instagram OSINT | Slow | Optional | Deep | Instagram analysis |
| Holehe | Fast | No | Medium | Email verification |
| Phone OSINT | Fast | No | Medium | Phone validation |
| IP OSINT | Fast | No | Medium | IP geolocation |
| Twitter OSINT | Medium | No | Deep | Twitter analysis |

---

Made with ❤️ for ethical OSINT research
