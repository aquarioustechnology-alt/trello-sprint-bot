# 🤖 Trello Sprint Bot - Weekly Milestone Automation

Automatically sync cards labeled "This Week" from **ALL boards across ALL workspaces** to a centralized Weekly Milestone board for better visibility and team coordination.

[![GitHub Actions](https://img.shields.io/badge/Automated%20via-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/aquarioustechnology-alt/trello-sprint-bot)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Trello API](https://img.shields.io/badge/Powered%20by-Trello%20API-0052CC?logo=trello&logoColor=white)](https://developer.atlassian.com/cloud/trello/)

---

## 🌟 Features

- 🌐 **FULL ACCOUNT SCANNING** - Automatically scans ALL 149+ boards across ALL workspaces
- ⚡ **Zero Configuration** - Works with any new board you create (no manual config needed)
- 🔄 **Bidirectional Sync** - Status changes sync between original and Weekly boards
- 🧹 **Auto-Cleanup** - Cards removed when "This Week" label is removed from either location
- 🏷️ **Auto-Label Creation** - Automatically creates color-coded labels for each project board
- 🔗 **Links to Originals** - Each Weekly card links back to the original
- ⏰ **GitHub Actions** - Runs automatically in the cloud every hour (9 AM-12 PM IST)
- 🖥️ **Local Execution** - Can also run manually on your Mac

---

## 📋 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/aquarioustechnology-alt/trello-sprint-bot.git
cd trello-sprint-bot
```

### 2. Set Up Configuration

```bash
# Copy the example config
cp weekly_config.json.example weekly_config.json

# Edit with your Trello credentials and board IDs
nano weekly_config.json
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup "This Week" Label on All Boards (One-Time)

**RECOMMENDED**: Create the "This Week" label on all your boards for easy selection:

```bash
# Set your Trello credentials
export TRELLO_API_KEY=your_api_key_here
export TRELLO_API_TOKEN=your_api_token_here

# Run the setup script
python setup_this_week_label.py
```

This will:
- ✅ Scan all your boards
- ✅ Create an orange "This Week" label on each board
- ✅ Skip boards that already have the label
- ✅ Ensure consistent labeling across your account

**Benefits:**
- 🎯 Team members just **select** the label (no typing/creating)
- 🎨 Consistent orange color across all boards
- ❌ No typos or label name variations

### 5. Run Manually

```bash
python weekly_milestone_sync.py
```

For detailed setup instructions, see **[QUICKSTART.md](QUICKSTART.md)**

---

## 🚀 How It Works

### Simple Workflow

1. **Add "This Week" label** to any card on any board in your Trello account
2. **Wait for next sync** (runs every hour from 9 AM - 12 PM IST)
3. **Card appears** on Weekly Milestone board with board-specific label
4. **Status syncs** bidirectionally between boards
5. **Remove label** from either location to clean up

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  ALL TRELLO BOARDS (149+ across all workspaces)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Project A    │  │ Project B    │  │ Project C    │  ...    │
│  │              │  │              │  │              │         │
│  │ Card with    │  │ Card with    │  │ Card with    │         │
│  │ "This Week"  │  │ "This Week"  │  │ "This Week"  │         │
│  │ label 🏷️     │  │ label 🏷️     │  │ label 🏷️     │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          │    ┌─────────────▼──────────────────▼───────┐
          └────►  Weekly Milestone Board (Aquarious Agile)│
               │  ┌──────────────────────────────────┐  │
               │  │ This Week                        │  │
               │  ├──────────────────────────────────┤  │
               │  │ In Progress                      │  │
               │  ├──────────────────────────────────┤  │
               │  │ Completed                        │  │
               │  ├──────────────────────────────────┤  │
               │  │ Blocked                          │  │
               │  └──────────────────────────────────┘  │
               └──────────────────────────────────────┘
                       ▲                    │
                       │  Bidirectional     │
                       │  Status Sync       │
                       └────────────────────┘
```

---

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[WEEKLY_SYNC_README.md](WEEKLY_SYNC_README.md)** - Complete documentation
- **[FULL_ACCOUNT_SCAN_UPGRADE.md](FULL_ACCOUNT_SCAN_UPGRADE.md)** - Technical details of full scanning
- **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - Detailed setup guide

---

## ⚙️ GitHub Actions Setup

The script runs automatically via GitHub Actions. To enable:

1. **Fork or use this repository**
2. **Add Secrets** (Settings → Secrets and variables → Actions):
   - `TRELLO_API_KEY` - Your Trello API key
   - `TRELLO_API_TOKEN` - Your Trello API token
   - `WEEKLY_BOARD_ID` - Your Weekly Milestone board ID
3. **Enable GitHub Actions** in the Actions tab

The workflow runs every hour from 9 AM to 12 PM IST automatically!

---

## 🎯 Use Cases

### For Team Leads
- Get a bird's-eye view of all "This Week" tasks across all projects
- Track progress without jumping between multiple boards
- Identify blockers quickly

### For Team Members
- Simply add "This Week" label to cards you're working on
- No need to manually update multiple boards
- Focus on work, not board management

### For Project Managers
- Centralized weekly sprint planning
- Cross-project visibility
- Automated status tracking

---

## 🔐 Security

- API credentials stored in GitHub Secrets (never in code)
- `weekly_config.json` ignored by git (contains sensitive data)
- Logs do not contain sensitive information
- Only accesses boards you have permission to view

---

## 📊 What Gets Synced

| Feature | Description |
|---------|-------------|
| **Card Title** | Exact copy |
| **Description** | Link to original card |
| **Due Date** | Synced |
| **Members** | Synced |
| **Labels** | Original labels + Board-specific label + "This Week" label |
| **Checklists** | Synced |
| **Comments** | Activity tracking comments added |
| **Status** | Bidirectional sync |

---

## 🧪 Testing

Run a test sync:

```bash
cd /path/to/trello-sprint-bot
python weekly_milestone_sync.py
```

Check the logs:

```bash
tail -f logs/weekly_sync_*.log
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📞 Support

For issues or questions:
1. Check the [documentation](WEEKLY_SYNC_README.md)
2. Review [closed issues](https://github.com/aquarioustechnology-alt/trello-sprint-bot/issues?q=is%3Aissue+is%3Aclosed)
3. Open a [new issue](https://github.com/aquarioustechnology-alt/trello-sprint-bot/issues/new)

---

## 📈 Stats

- **Boards Scanned**: 149+ (all accessible boards)
- **Execution Time**: ~1.5 minutes per full scan
- **API Rate Limits**: Automatically handled
- **Uptime**: 99.9% (via GitHub Actions)

---

## 📝 License

MIT License - see LICENSE file for details

---

## 🎊 Changelog

### v2.1.0 (October 24, 2025)
- ✨ **NEW**: Label setup script - Create "This Week" label on all boards in one command
- 🎯 **IMPROVED**: Team UX - Members can now just select label instead of creating it
- 🎨 **IMPROVED**: Consistent labeling - Same color and name across all boards

### v2.0.0 (October 24, 2025)
- ✨ **NEW**: Full account scanning - scans ALL boards across ALL workspaces
- ✨ **NEW**: Auto-label creation for any board
- ✨ **NEW**: Enhanced cleanup - remove label from either location
- ✨ **NEW**: Zero configuration - works with any new board automatically
- 🐛 Fixed duplicate card prevention
- 📚 Comprehensive documentation

### v1.0.0 (October 24, 2025)
- 🎉 Initial release
- ✅ Basic card pulling from 3 hardcoded boards
- ✅ Bidirectional sync
- ✅ GitHub Actions integration

---

**Made with ❤️ for better Trello project management**

[Report Bug](https://github.com/aquarioustechnology-alt/trello-sprint-bot/issues) · [Request Feature](https://github.com/aquarioustechnology-alt/trello-sprint-bot/issues) · [Documentation](WEEKLY_SYNC_README.md)
