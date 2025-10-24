# Weekly Milestone Board Automation

Automatically sync cards labeled "This Week" from **ALL boards across ALL workspaces** to a centralized Weekly Milestone board.

## 📋 Overview

This automation scans your **entire Trello account** (149+ boards) and pulls ANY card labeled "This Week" into a centralized Weekly Milestone board in the Aquarious Agile workspace for better visibility and team coordination.

## 🎯 Features

- 🌐 **FULL ACCOUNT SCANNING** - Automatically scans ALL 149+ boards across ALL workspaces
- ✅ **Zero Configuration** - Works with any new board you create (no manual config needed)
- ✅ **Automatic card pulling** - Cards labeled "This Week" from ANY board are automatically copied
- ✅ **Auto-label creation** - Automatically creates color-coded labels for each project board
- ✅ **Bidirectional sync** - Status changes sync between original and Weekly boards
- ✅ **Smart cleanup** - Cards removed when "This Week" label is removed from either location
- ✅ **Duplicate prevention** - Won't create duplicate cards
- ✅ **Links to originals** - Each Weekly card links back to the original
- ✅ **GitHub Actions** - Runs automatically in the cloud every hour (9 AM-12 PM IST)
- ✅ **Local execution** - Can also run manually on your Mac

## 🏗️ Board Structure

**Weekly Milestone Board:** https://trello.com/b/ikF8RJkK/weekly-milestone

**Lists:**
- 📅 **This Week** - Cards pulled from project boards
- 🚀 **In Progress** - Currently being worked on
- ✅ **Completed** - Finished this week
- 🔴 **Blocked** - Blocked/waiting

**Labels:**
- **Auto-created for each board** - Script automatically creates color-coded labels for any board with "This Week" cards
- Examples: B2B Marketplace, Finomatic Investor App, Used Oil India, and any other board you create!
- 🎨 **Color cycling** - Uses 10 different colors (blue, green, yellow, orange, red, purple, pink, lime, sky, black)

## 🚀 How to Use

### For Team Members

1. **Add cards to Weekly board:**
   - Open any card on **ANY board in ANY workspace**
   - Add the **"This Week"** label (orange)
   - Wait for next sync (runs every hour from 9 AM - 12 PM IST)
   - Card appears on Weekly Milestone board automatically with board-specific label!

2. **Remove cards from Weekly board:**
   - Remove the **"This Week"** label from either the original card OR the Weekly board card
   - Card will be removed from Weekly board on next sync
   - Original card stays on project board

3. **Update status:**
   - Move cards between lists on Weekly board
   - Status updates sync back to original cards

### Manual Execution (Local)

Run the script manually anytime:

```bash
cd /Users/rajsingh/Projects/trello_mcp
uv run python weekly_milestone_sync.py
```

### Test the Automation

```bash
# Manual test run
cd /Users/rajsingh/Projects/trello_mcp
uv run python weekly_milestone_sync.py

# Check logs
tail -f logs/weekly_sync_*.log
```

## ⚙️ GitHub Actions Setup

The script runs automatically via GitHub Actions every hour from 9 AM to 12 PM IST.

### Setting Up GitHub Actions

1. **Push code to GitHub:**
   ```bash
   cd /Users/rajsingh/Projects/trello_mcp
   git init
   git add .
   git commit -m "Add Weekly Milestone automation"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Add Secrets to GitHub:**
   - Go to your repo: Settings → Secrets and variables → Actions
   - Add these secrets:
     - `TRELLO_API_KEY`: Your Trello API Key (Get from https://trello.com/app-key)
     - `TRELLO_API_TOKEN`: Your Trello API Token (Generate from same page)
     - `WEEKLY_BOARD_ID`: Your Weekly Milestone Board ID

3. **Enable GitHub Actions:**
   - Go to repo → Actions tab
   - Enable workflows if prompted

4. **Manual Trigger:**
   - Go to Actions → Weekly Milestone Sync
   - Click "Run workflow" → "Run workflow"

### Schedule

The workflow runs:
- **9:00 AM IST** (3:30 AM UTC)
- **10:00 AM IST** (4:30 AM UTC)
- **11:00 AM IST** (5:30 AM UTC)
- **12:00 PM IST** (6:30 AM UTC)

Every day, including weekends.

## 🖥️ Local Scheduled Execution (Backup)

If you want the script to run locally on your Mac (as backup or primary):

### Enable Local Scheduling

```bash
# Load the launchd agent (enables scheduled runs)
launchctl load ~/Library/LaunchAgents/com.trello.weekly.sync.plist

# Check if it's running
launchctl list | grep trello.weekly

# View logs
tail -f /Users/rajsingh/Projects/trello_mcp/logs/weekly_sync.log
```

### Disable Local Scheduling

```bash
# Unload the launchd agent
launchctl unload ~/Library/LaunchAgents/com.trello.weekly.sync.plist
```

**Note:** By default, local scheduling is **disabled**. GitHub Actions is the primary method.

## 📊 How It Works

### 1. Pull Cards to Weekly Board

```
Project Board          →          Weekly Milestone Board
─────────────                     ─────────────────────
Card with                         Copy of card with:
"This Week" label    ──copy──→    • Link to original
                                  • Project label
                                  • Same members/due date
```

### 2. Sync Status Changes

```
Weekly Board: Move to "Completed"
         ↓
   (sync status)
         ↓
Original Board: Add comment "✅ Completed on Weekly board"
```

### 3. Cleanup When Label Removed

```
Project Board: Remove "This Week" label
         ↓
   (detect change)
         ↓
Weekly Board: Delete card
         ↓
Original Board: Add comment "🔄 Removed from Weekly board"
```

## 📁 Files

```
trello_mcp/
├── weekly_milestone_sync.py        # Main sync script
├── weekly_config.json              # Configuration (board IDs, credentials)
├── weekly_sync_mapping.json        # Card mappings (auto-managed)
├── logs/                           # Execution logs
│   ├── weekly_sync_YYYYMMDD_HHMMSS.log
│   └── weekly_sync_error.log
├── .github/
│   └── workflows/
│       └── weekly-milestone-sync.yml  # GitHub Actions workflow
└── WEEKLY_SYNC_README.md           # This file
```

## 🐛 Troubleshooting

### Cards not appearing on Weekly board

1. Check if card has "This Week" label (orange)
2. Wait for next scheduled run or run manually
3. Check logs: `tail -f logs/weekly_sync_*.log`

### GitHub Actions not running

1. Verify repo secrets are set correctly
2. Check Actions tab for error messages
3. Manually trigger workflow to test

### Local execution not working

```bash
# Test if uv is working
which uv

# Test if Python script runs
cd /Users/rajsingh/Projects/trello_mcp
uv run python weekly_milestone_sync.py

# Check for errors
cat logs/weekly_sync_error.log
```

## 📈 Stats & Monitoring

Each run logs:
- **Cards Pulled:** Number of new cards copied to Weekly board
- **Status Synced:** Number of status updates
- **Cards Removed:** Number of cards cleaned up
- **Errors:** Any API errors encountered
- **Total Mapped Cards:** Current number of synced cards

View logs:
```bash
# Latest log
ls -lt logs/weekly_sync_*.log | head -1 | awk '{print $NF}' | xargs tail -50

# All logs
ls -lt logs/
```

## 🔐 Security

- API credentials stored in:
  - GitHub Secrets (for GitHub Actions)
  - Local config file (for manual runs)
- Logs do not contain sensitive information
- Mapping file contains only card IDs (no content)

## 🎯 Best Practices

1. **Use labels consistently** - Add "This Week" only for cards you want on Weekly board
2. **Review Weekly board daily** - Keep it focused on current priorities
3. **Update status on Weekly board** - Move cards through the workflow
4. **Remove labels when done** - Clean up completed work
5. **Check logs weekly** - Monitor for any issues

## 📞 Support

For issues or questions:
1. Check logs: `logs/weekly_sync_*.log`
2. Run manually to test: `uv run python weekly_milestone_sync.py`
3. Check GitHub Actions runs for errors

## 🔄 Configuration

The script requires minimal configuration in `weekly_config.json`:
- **Weekly board ID** - The ID of your Weekly Milestone board
- **Workspace ID** - The Aquarious Agile workspace ID
- **Trigger label** - Default: "This Week"
- **List IDs** - The list IDs on your Weekly board

**No need to configure project boards** - The script automatically scans all boards in your account!

After changes, test manually before relying on scheduled runs.

---

**Created:** October 24, 2025
**Board URL:** https://trello.com/b/ikF8RJkK/weekly-milestone

