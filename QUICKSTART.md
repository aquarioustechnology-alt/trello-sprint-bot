# 🚀 Quick Start Guide - Weekly Milestone Automation

## ✅ What's Already Set Up

- ✅ Weekly Milestone board created: https://trello.com/b/ikF8RJkK/weekly-milestone
- ✅ Lists created: This Week, In Progress, Completed, Blocked
- ✅ Project labels created: B2B Marketplace (blue), Finomatic (green), Used Oil (yellow)
- ✅ "This Week" trigger label added to all project boards
- ✅ Python script working and tested
- ✅ Configuration files ready
- ✅ GitHub Actions workflow configured
- ✅ Local launchd scheduler configured (disabled by default)

## 🎯 How to Use (For Team)

### Add a Card to Weekly Board

1. Open any card on B2B Marketplace, Finomatic, or Used Oil India boards
2. Add the **"This Week"** label (orange color)
3. Wait for the next hourly sync (9 AM - 12 PM IST) OR run manually
4. Card appears on Weekly Milestone board automatically!

### Remove a Card from Weekly Board

1. Open the original card on the project board
2. Remove the **"This Week"** label
3. On next sync, card disappears from Weekly board
4. Original card remains on project board unchanged

## 🖥️ Manual Execution

Run the sync anytime:

```bash
cd /Users/rajsingh/Projects/trello_mcp
uv run python weekly_milestone_sync.py
```

View logs:
```bash
tail -f /Users/rajsingh/Projects/trello_mcp/logs/weekly_sync_*.log
```

## 🐙 GitHub Actions Setup (Recommended)

### Step 1: Push to GitHub

```bash
cd /Users/rajsingh/Projects/trello_mcp

# Initialize git if not already
git init

# Add files
git add .

# Commit
git commit -m "Add Weekly Milestone automation"

# Add your GitHub repo (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push
git push -u origin main
```

### Step 2: Add GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add these three secrets:

   **Secret 1:**
   - Name: `TRELLO_API_KEY`
   - Value: `YOUR_TRELLO_API_KEY` (Get from https://trello.com/app-key)

   **Secret 2:**
   - Name: `TRELLO_API_TOKEN`
   - Value: `YOUR_TRELLO_API_TOKEN` (Generate from the same page)

   **Secret 3:**
   - Name: `WEEKLY_BOARD_ID`
   - Value: `YOUR_WEEKLY_BOARD_ID` (From your Weekly Milestone board URL)

### Step 3: Enable and Test

1. Go to **Actions** tab in your repo
2. Find "Weekly Milestone Sync" workflow
3. Click **Run workflow** → **Run workflow** (manual test)
4. Check the run to see if it succeeds

### Step 4: Let it Run Automatically

From now on, the workflow runs automatically:
- 9:00 AM IST
- 10:00 AM IST
- 11:00 AM IST
- 12:00 PM IST

Every day, including weekends!

## 🏠 Local Scheduled Execution (Optional Backup)

If you want your Mac to run the script locally:

```bash
# Enable local scheduling
launchctl load ~/Library/LaunchAgents/com.trello.weekly.sync.plist

# Check if running
launchctl list | grep trello.weekly

# Disable local scheduling
launchctl unload ~/Library/LaunchAgents/com.trello.weekly.sync.plist
```

**Note:** By default, local scheduling is **disabled**. GitHub Actions is the primary method.

## 🧪 Test with a Real Card

Let's test it right now:

1. **Go to any project board** (B2B, Finomatic, or Used Oil)
2. **Pick any card** (or create a test card: "Test Weekly Sync")
3. **Add "This Week" label** (orange)
4. **Run the script manually:**
   ```bash
   cd /Users/rajsingh/Projects/trello_mcp
   uv run python weekly_milestone_sync.py
   ```
5. **Check the Weekly Milestone board** - your card should appear!
6. **Remove the "This Week" label** from the original card
7. **Run the script again** - card disappears from Weekly board

## 📊 What Happens During Sync

```
┌─────────────────────────┐
│  Project Boards         │
│  (B2B, Finomatic, etc)  │
└───────────┬─────────────┘
            │
            │ Script scans for
            │ "This Week" label
            ↓
┌─────────────────────────┐
│  Weekly Milestone Board │
│  (Centralized view)     │
└─────────────────────────┘

Sync runs every hour from 9 AM - 12 PM IST
```

## 🔍 Monitoring

**View sync logs:**
```bash
# Latest log
ls -t /Users/rajsingh/Projects/trello_mcp/logs/*.log | head -1 | xargs cat

# Follow live
tail -f /Users/rajsingh/Projects/trello_mcp/logs/weekly_sync_*.log
```

**GitHub Actions logs:**
- Go to repo → Actions → Click on a workflow run
- View detailed logs and artifacts

## 📁 Important Files

```
trello_mcp/
├── weekly_milestone_sync.py       ← Main script
├── weekly_config.json             ← Configuration (board IDs)
├── weekly_sync_mapping.json       ← Auto-managed (card mappings)
├── requirements.txt               ← Python dependencies
├── logs/                          ← Execution logs
├── .github/workflows/
│   └── weekly-milestone-sync.yml  ← GitHub Actions
└── WEEKLY_SYNC_README.md          ← Full documentation
```

## 🐛 Troubleshooting

**Script fails with "Module not found":**
```bash
cd /Users/rajsingh/Projects/trello_mcp
uv pip install -r requirements.txt
```

**Cards not appearing:**
- Check if card has "This Week" label
- Run script manually to test
- Check logs for errors

**GitHub Actions not running:**
- Verify secrets are set correctly
- Check Actions tab for error messages
- Manually trigger to test

## 📞 Need Help?

1. Check full docs: `WEEKLY_SYNC_README.md`
2. View logs: `logs/weekly_sync_*.log`
3. Test manually: `uv run python weekly_milestone_sync.py`

## 🎉 You're All Set!

The automation is ready to use:
- ✅ Add "This Week" label to any card
- ✅ It appears on Weekly Milestone board
- ✅ Remove label, card disappears
- ✅ Works automatically via GitHub Actions
- ✅ Can run manually anytime

**Weekly Milestone Board:** https://trello.com/b/ikF8RJkK/weekly-milestone

Happy syncing! 🚀

