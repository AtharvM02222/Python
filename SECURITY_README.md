# Security & Credentials Setup

## ⚠️ Important: Never Commit Credentials

Your Instagram credentials and session files are now protected and should NEVER be committed to Git.

## Setup Instructions

### 1. Configure Credentials

Copy the example file and add your credentials:

```bash
cd Python/Osintgram/config
cp credentials.ini.example credentials.ini
nano credentials.ini  # or use any text editor
```

Edit `credentials.ini`:
```ini
[Credentials]
username =your_instagram_username
password =your_instagram_password
hikerapi_token =
```

### 2. Protected Files

The following files are automatically ignored by Git (see `.gitignore`):

- `Osintgram/config/credentials.ini` - Your login credentials
- `session-*` - Instagram session files
- `*.session` - Any session files

### 3. Best Practices

✅ **DO:**
- Keep credentials in `credentials.ini` (it's gitignored)
- Use strong, unique passwords
- Enable 2FA on your Instagram account
- Delete session files when done: `rm session-*`

❌ **DON'T:**
- Commit credentials to Git
- Share your credentials.ini file
- Use your main Instagram account for automation
- Hardcode passwords in scripts

### 4. If You Accidentally Committed Credentials

If you already pushed credentials to GitHub:

```bash
# 1. Change your Instagram password immediately
# 2. Remove from Git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch Python/Osintgram/config/credentials.ini" \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push
git push origin --force --all
```

### 5. Create Credentials File

When setting up on a new machine:

```bash
cd Python/Osintgram/config
cp credentials.ini.example credentials.ini
# Edit credentials.ini with your details
```

### 6. Environment Variables (Alternative)

For extra security, use environment variables:

```bash
export IG_USERNAME="your_username"
export IG_PASSWORD="your_password"
```

Then modify scripts to read from environment:
```python
import os
USERNAME = os.getenv('IG_USERNAME')
PASSWORD = os.getenv('IG_PASSWORD')
```

---

## Current Status

✅ Credentials cleared from `credentials.ini`
✅ Session files deleted
✅ `.gitignore` configured
✅ Example file created

You're now safe to commit to Git!
