# 🚀 Quick Deploy Commands

## Push to GitHub (Choose One Method)

### Method 1: SSH (Recommended)

```bash
cd /Users/rajsingh/Projects/trello_mcp
git remote set-url sprint-bot git@github.com:aquarioustechnology-alt/trello-sprint-bot.git
git push sprint-bot master:main
```

### Method 2: Personal Access Token

1. Create token at: https://github.com/settings/tokens
2. Push with token:

```bash
cd /Users/rajsingh/Projects/trello_mcp
git push https://YOUR_TOKEN@github.com/aquarioustechnology-alt/trello-sprint-bot.git master:main
```

---

## Setup GitHub Secrets

Go to: https://github.com/aquarioustechnology-alt/trello-sprint-bot/settings/secrets/actions

Add these 3 secrets:

| Secret Name | Value |
|-------------|-------|
| `TRELLO_API_KEY` | Your Trello API Key (from https://trello.com/app-key) |
| `TRELLO_API_TOKEN` | Your Trello API Token (generate from same page) |
| `WEEKLY_BOARD_ID` | Your Weekly Milestone Board ID |

---

## Enable GitHub Actions

1. Go to repository: https://github.com/aquarioustechnology-alt/trello-sprint-bot
2. Click "Actions" tab
3. Enable workflows if prompted
4. Manual trigger: Actions → Weekly Milestone Sync → Run workflow

---

## Test Locally Anytime

```bash
cd /Users/rajsingh/Projects/trello_mcp
uv run python weekly_milestone_sync.py
```

---

## Check Logs

```bash
# Latest log
tail -f /Users/rajsingh/Projects/trello_mcp/logs/weekly_sync_*.log

# List all logs
ls -lt /Users/rajsingh/Projects/trello_mcp/logs/
```

---

## Quick Links

- **Repository**: https://github.com/aquarioustechnology-alt/trello-sprint-bot
- **Weekly Board**: https://trello.com/b/ikF8RJkK/weekly-milestone
- **Workspace**: https://trello.com/w/aquariousagile
- **GitHub Actions**: https://github.com/aquarioustechnology-alt/trello-sprint-bot/actions
- **Settings**: https://github.com/aquarioustechnology-alt/trello-sprint-bot/settings

---

## What Happens After Push?

✅ Repository will have all files  
✅ GitHub Actions workflow will be visible  
✅ Once secrets are added, automation runs automatically  
✅ Runs every hour from 9 AM - 12 PM IST  
✅ Logs available in GitHub Actions runs  

---

**Status**: 🎊 All tests passed, ready to deploy!

