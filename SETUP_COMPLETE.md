# ✅ Weekly Milestone Automation - Setup Complete!

**Date Created:** October 24, 2025  
**Status:** ✅ Fully functional and tested

---

## 🎉 What You Got

A fully automated system that syncs cards from multiple Trello boards into a centralized Weekly Milestone board. When you add a "This Week" label to any card on your project boards, it automatically appears on the Weekly board for team visibility.

### Your New Board
**Weekly Milestone Board:** https://trello.com/b/ikF8RJkK/weekly-milestone

---

## 🚀 Quick Start (3 Steps)

### Step 1: Test It Right Now (30 seconds)

```bash
# Go to any project board and add "This Week" label to a card, then:
cd /Users/rajsingh/Projects/trello_mcp
uv run python weekly_milestone_sync.py

# Check your Weekly board - the card should appear!
```

### Step 2: Set Up GitHub Actions (5 minutes)

This makes it run automatically in the cloud without your Mac needing to be on.

1. **Create a GitHub repository** (if you don't have one already)

2. **Push the code:**
   ```bash
   cd /Users/rajsingh/Projects/trello_mcp
   git init
   git add .
   git commit -m "Add Weekly Milestone automation"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

3. **Add 3 secrets to GitHub:**
   - Go to your repo → Settings → Secrets and variables → Actions
   - Click "New repository secret" three times and add:
   
   | Secret Name | Secret Value |
   |------------|--------------|
   | `TRELLO_API_KEY` | Your Trello API Key (from https://trello.com/app-key) |
   | `TRELLO_API_TOKEN` | Your Trello API Token (generate from same page) |
   | `WEEKLY_BOARD_ID` | Your Weekly Milestone Board ID |

4. **Enable the workflow:**
   - Go to Actions tab
   - Click "I understand my workflows, go ahead and enable them"

5. **Test it:**
   - Click on "Weekly Milestone Sync" workflow
   - Click "Run workflow" → "Run workflow"
   - Watch it run!

### Step 3: Tell Your Team

Share this with your team:

> **New: Weekly Milestone Board!**
> 
> Want your card to appear on the team's weekly board?
> 1. Add the "This Week" label (orange) to your card
> 2. It'll automatically appear on https://trello.com/b/ikF8RJkK/weekly-milestone
> 3. Remove the label when you're done, and it disappears from the weekly board
> 
> Your original card stays on the project board - this is just a copy for visibility!

---

## 📊 How It Works

```
┌────────────────────────────────────────────────────────────┐
│  PROJECT BOARDS                                            │
│  • B2B Marketplace                                         │
│  • Finomatic Investor App                                  │
│  • Used Oil India                                          │
│                                                            │
│  Card with "This Week" label added                        │
└─────────────────┬──────────────────────────────────────────┘
                  │
                  │ Automation runs every hour
                  │ (9 AM - 12 PM IST, daily)
                  ↓
┌────────────────────────────────────────────────────────────┐
│  WEEKLY MILESTONE BOARD                                    │
│  https://trello.com/b/ikF8RJkK/weekly-milestone           │
│                                                            │
│  Lists:                                                    │
│  • This Week (new cards land here)                        │
│  • In Progress (move cards here when working)             │
│  • Completed (mark done)                                   │
│  • Blocked (issues/waiting)                                │
│                                                            │
│  Each card is labeled by project:                         │
│  🟦 B2B Marketplace | 🟩 Finomatic | 🟨 Used Oil         │
└────────────────────────────────────────────────────────────┘
```

---

## 🎯 Usage Guide

### For Team Members

**Adding a card to weekly board:**
1. Open any card on B2B, Finomatic, or Used Oil board
2. Click "Labels"
3. Add "This Week" label (orange color)
4. Wait for next sync (or ask admin to run it)
5. Card appears on Weekly Milestone board!

**Removing a card:**
1. Go back to the original card
2. Remove "This Week" label
3. On next sync, it disappears from Weekly board
4. Original card stays on project board

**Updating status:**
- Move cards on Weekly board between lists
- Status updates sync back to original cards
- Original cards get comment notifications

### For You (Admin)

**Run sync manually anytime:**
```bash
cd /Users/rajsingh/Projects/trello_mcp
uv run python weekly_milestone_sync.py
```

**View logs:**
```bash
tail -f /Users/rajsingh/Projects/trello_mcp/logs/weekly_sync_*.log
```

**Check latest sync result:**
```bash
ls -t /Users/rajsingh/Projects/trello_mcp/logs/*.log | head -1 | xargs cat
```

---

## 🤖 Automation Options

### Option A: GitHub Actions (Recommended)

✅ **Pros:**
- Runs in the cloud (your Mac doesn't need to be on)
- Free for public repos
- Runs automatically every hour from 9 AM - 12 PM IST
- No maintenance needed
- Logs stored for 30 days

❌ **Cons:**
- Requires GitHub account
- Requires pushing code to GitHub

**Status after setup:** Runs automatically, no intervention needed!

### Option B: Local Mac Scheduler

✅ **Pros:**
- Everything stays local
- No GitHub account needed
- Full control

❌ **Cons:**
- Mac must be on and awake
- You have to maintain it
- Logs only local

**To enable:**
```bash
launchctl load ~/Library/LaunchAgents/com.trello.weekly.sync.plist
```

**To disable:**
```bash
launchctl unload ~/Library/LaunchAgents/com.trello.weekly.sync.plist
```

---

## 📁 What Was Created

### Trello
- ✅ Weekly Milestone board with 4 lists
- ✅ 3 project labels (B2B, Finomatic, Used Oil)
- ✅ "This Week" trigger label on all project boards

### Code Files
```
trello_mcp/
├── weekly_milestone_sync.py          ← Main automation script
├── weekly_config.json                ← Board IDs and settings
├── weekly_sync_mapping.json          ← Card mappings (auto-managed)
├── requirements.txt                  ← Python dependencies
├── .gitignore                        ← Git ignore rules
├── QUICKSTART.md                     ← Quick start guide (this file)
├── WEEKLY_SYNC_README.md             ← Full documentation
├── SETUP_COMPLETE.md                 ← This guide
├── logs/                             ← Execution logs
└── .github/workflows/
    └── weekly-milestone-sync.yml     ← GitHub Actions config
```

### System Files
```
~/Library/LaunchAgents/
└── com.trello.weekly.sync.plist      ← Local scheduler (disabled by default)
```

---

## 🧪 Testing Checklist

Test the automation with these steps:

- [ ] **Test 1: Pull a card**
  1. Add "This Week" label to a card on any project board
  2. Run: `cd /Users/rajsingh/Projects/trello_mcp && uv run python weekly_milestone_sync.py`
  3. Check Weekly Milestone board - card should appear
  4. Card should have project-specific label
  5. Card should link back to original

- [ ] **Test 2: Remove a card**
  1. Remove "This Week" label from original card
  2. Run sync again
  3. Card should disappear from Weekly board
  4. Original card should have comment about removal

- [ ] **Test 3: GitHub Actions**
  1. Push to GitHub
  2. Add secrets
  3. Manually trigger workflow
  4. Check Actions tab for successful run
  5. Check Weekly board for any changes

- [ ] **Test 4: Team Usage**
  1. Have a team member add "This Week" label
  2. Run sync (or wait for scheduled run)
  3. Verify they can see the card on Weekly board

---

## 🐛 Troubleshooting

### Cards not appearing on Weekly board

**Check:**
1. Does the card have "This Week" label (orange)?
2. Did the sync run? Check logs: `ls -lt logs/`
3. Any errors in logs? `tail logs/weekly_sync_*.log`

**Solution:**
Run manually and watch output:
```bash
cd /Users/rajsingh/Projects/trello_mcp
uv run python weekly_milestone_sync.py
```

### GitHub Actions not running

**Check:**
1. Are all 3 secrets added correctly?
2. Go to Actions → Select workflow → Check for errors
3. Is the workflow enabled?

**Solution:**
Manually trigger the workflow from GitHub UI to test.

### Local scheduler not working

**Check:**
1. Is it loaded? `launchctl list | grep trello.weekly`
2. Is your Mac awake during scheduled times?
3. Check error log: `cat logs/weekly_sync_error.log`

**Solution:**
Unload and reload:
```bash
launchctl unload ~/Library/LaunchAgents/com.trello.weekly.sync.plist
launchctl load ~/Library/LaunchAgents/com.trello.weekly.sync.plist
```

### Script fails with "Module not found"

**Solution:**
Install dependencies:
```bash
cd /Users/rajsingh/Projects/trello_mcp
uv pip install -r requirements.txt
```

---

## 📊 Monitoring

### View Sync Statistics

Each sync logs:
- Cards Pulled (new cards added to Weekly board)
- Status Synced (status updates between boards)
- Cards Removed (cards cleaned up)
- Errors (API errors or failures)
- Total Mapped Cards (currently synced)

**View latest stats:**
```bash
cd /Users/rajsingh/Projects/trello_mcp
tail logs/weekly_sync_*.log | grep "SYNC SUMMARY" -A 6
```

### GitHub Actions Logs

1. Go to repo → Actions
2. Click on any workflow run
3. Click on "sync-cards" job
4. View detailed logs
5. Download log artifacts (kept for 30 days)

---

## 🔐 Security Notes

- API credentials stored in:
  - GitHub Secrets (encrypted, only accessible to workflows)
  - Local `weekly_config.json` (for manual runs)
- `.gitignore` prevents sensitive files from being committed
- Logs don't contain API keys or tokens
- Card mapping only stores IDs, not content

**⚠️ Important:** Never commit `weekly_config.json` to a public repository!

---

## 🔄 Maintenance

### Weekly

- Check GitHub Actions runs (if using)
- Review Weekly board with team
- Clean up completed work

### Monthly

- Review logs for any recurring errors
- Update documentation if workflow changes
- Check disk space used by logs

### As Needed

- Update Trello API credentials if they change
- Modify board IDs if boards are recreated
- Adjust schedule if team needs change

---

## 📚 Documentation

### For Quick Reference
- **QUICKSTART.md** - Get started in 5 minutes
- **SETUP_COMPLETE.md** - This file

### For Detailed Information
- **WEEKLY_SYNC_README.md** - Complete technical documentation

### For Code
- **weekly_milestone_sync.py** - Main script (well-commented)
- **weekly_config.json** - Configuration reference

---

## 💡 Tips & Best Practices

1. **Use labels consistently** - Only add "This Week" to cards you actively need visibility on
2. **Keep Weekly board clean** - Remove labels when work is done
3. **Move cards through workflow** - Use the 4 lists to show progress
4. **Check logs periodically** - Catch issues early
5. **Run manual sync before meetings** - Get latest state for standups
6. **Use project labels for filtering** - Click label to see only one project
7. **Link back to originals** - Each card has a link - use it!

---

## 🎓 Training Your Team

Share this guide with your team:

### 1-Minute Version
"Add 'This Week' label to any card to see it on the Weekly board. Remove the label when done."

### 5-Minute Version
1. Show them the Weekly Milestone board
2. Demonstrate adding "This Week" label
3. Run sync and show card appearing
4. Show them how to navigate back to original
5. Demonstrate removing label

### Team Meeting
1. Present the Weekly board
2. Explain the workflow (4 lists)
3. Show live demo of adding/removing cards
4. Answer questions
5. Encourage usage for one week
6. Gather feedback

---

## 🤝 Support & Help

**If you need help:**

1. Check this guide and WEEKLY_SYNC_README.md
2. Review logs for error messages
3. Test manually to isolate issue
4. Check GitHub Actions runs (if using)

**Common questions:**

Q: Can I change the label name from "This Week"?  
A: Yes! Edit `weekly_config.json` and change `trigger_label` value.

Q: Can I add more project boards?  
A: Yes! Add them to `project_boards` array in `weekly_config.json`.

Q: Can I change the schedule?  
A: Yes! Edit `.github/workflows/weekly-milestone-sync.yml` cron values.

Q: What if I want the script to run more often?  
A: Add more cron entries in the GitHub Actions workflow file.

---

## ✅ Next Actions

- [ ] Test the automation with a real card
- [ ] Push to GitHub and set up Actions
- [ ] Share Weekly board with team
- [ ] Run first team meeting with the board
- [ ] Collect feedback after one week
- [ ] Adjust workflow as needed

---

## 🎉 You're Done!

Everything is set up and ready to use. The automation is working, tested, and documented.

**Your Weekly Milestone board:** https://trello.com/b/ikF8RJkK/weekly-milestone

Happy syncing! 🚀

---

*Created: October 24, 2025*  
*Version: 1.0*  
*Status: Production Ready ✅*

