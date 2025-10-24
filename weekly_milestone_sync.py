#!/usr/bin/env python3
"""
Weekly Milestone Board Sync Script
Automatically syncs cards labeled "This Week" from project boards to a centralized Weekly Milestone board.
"""

import json
import os
import sys
import requests
from datetime import datetime
from typing import Dict, List, Optional, Set
import logging

# Set up logging
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f'weekly_sync_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class TrelloWeeklySync:
    def __init__(self, config_path='weekly_config.json', mapping_path='weekly_sync_mapping.json'):
        """Initialize the sync manager"""
        self.config_path = config_path
        self.mapping_path = mapping_path
        self.config = self.load_config()
        self.mapping = self.load_mapping()
        
        # Get API credentials from config or environment
        self.api_key = os.getenv('TRELLO_API_KEY', self.config.get('api_key'))
        self.api_token = os.getenv('TRELLO_API_TOKEN', self.config.get('api_token'))
        self.weekly_board_id = os.getenv('WEEKLY_BOARD_ID', self.config.get('weekly_board_id'))
        
        self.base_url = 'https://api.trello.com/1'
        self.stats = {
            'pulled': 0,
            'synced': 0,
            'removed': 0,
            'errors': 0
        }
        
        # Auto-load lists if not configured (for GitHub Actions)
        if not self.config.get('lists'):
            self.config['lists'] = self.get_board_lists()
    
    def get_board_lists(self) -> Dict:
        """Get board lists and map them by name"""
        lists_response = self.api_request('GET', f'boards/{self.weekly_board_id}/lists')
        if not lists_response:
            logger.warning("Could not get board lists, using first list as default")
            return {'this_week': None}
        
        # Map lists by name (lowercase, replace spaces with underscores)
        lists_map = {}
        for list_item in lists_response:
            key = list_item['name'].lower().replace(' ', '_')
            lists_map[key] = list_item['id']
        
        # Use first list as this_week if not found
        if 'this_week' not in lists_map and lists_response:
            lists_map['this_week'] = lists_response[0]['id']
            logger.info(f"Using first list '{lists_response[0]['name']}' as 'This Week' list")
        
        return lists_map
    
    def load_config(self) -> Dict:
        """Load configuration file or use environment variables"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # If running in GitHub Actions or env vars are set, use minimal config
            if os.getenv('TRELLO_API_KEY') and os.getenv('TRELLO_API_TOKEN') and os.getenv('WEEKLY_BOARD_ID'):
                logger.info("Config file not found, using environment variables")
                return {
                    'trigger_label': 'This Week',
                    'lists': {}  # Will be determined from board if needed
                }
            else:
                logger.error(f"Config file not found and environment variables not set: {self.config_path}")
                sys.exit(1)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            sys.exit(1)
    
    def load_mapping(self) -> Dict:
        """Load card mapping file"""
        try:
            with open(self.mapping_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'mappings': [], 'last_updated': None}
        except json.JSONDecodeError:
            logger.warning("Invalid mapping file, starting fresh")
            return {'mappings': [], 'last_updated': None}
    
    def save_mapping(self):
        """Save card mapping to file"""
        self.mapping['last_updated'] = datetime.now().isoformat()
        with open(self.mapping_path, 'w') as f:
            json.dump(self.mapping, f, indent=2)
        logger.info(f"Mapping saved with {len(self.mapping['mappings'])} entries")
    
    def api_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Optional[Dict]:
        """Make API request to Trello"""
        url = f"{self.base_url}/{endpoint}"
        auth_params = {'key': self.api_key, 'token': self.api_token}
        
        if params:
            auth_params.update(params)
        
        try:
            if method == 'GET':
                response = requests.get(url, params=auth_params)
            elif method == 'POST':
                response = requests.post(url, params=auth_params, json=data)
            elif method == 'PUT':
                response = requests.put(url, params=auth_params, json=data)
            elif method == 'DELETE':
                response = requests.delete(url, params=auth_params)
            else:
                logger.error(f"Unsupported HTTP method: {method}")
                return None
            
            response.raise_for_status()
            return response.json() if response.text else {}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            self.stats['errors'] += 1
            return None
    
    def get_cards_with_label(self, board_id: str, label_name: str) -> List[Dict]:
        """Get all cards on a board with a specific label"""
        cards = self.api_request('GET', f'boards/{board_id}/cards', {'fields': 'all'})
        if not cards:
            return []
        
        filtered_cards = []
        for card in cards:
            for label in card.get('labels', []):
                if label.get('name') == label_name:
                    filtered_cards.append(card)
                    break
        
        return filtered_cards
    
    def get_card(self, card_id: str) -> Optional[Dict]:
        """Get card details"""
        return self.api_request('GET', f'cards/{card_id}', {'fields': 'all'})
    
    def find_mapping(self, original_card_id: str = None, weekly_card_id: str = None) -> Optional[Dict]:
        """Find mapping entry"""
        for mapping in self.mapping['mappings']:
            if original_card_id and mapping['original_card_id'] == original_card_id:
                return mapping
            if weekly_card_id and mapping['weekly_card_id'] == weekly_card_id:
                return mapping
        return None
    
    def add_mapping(self, original_card_id: str, weekly_card_id: str, original_board_id: str, original_list_id: str):
        """Add new mapping entry"""
        self.mapping['mappings'].append({
            'original_card_id': original_card_id,
            'weekly_card_id': weekly_card_id,
            'original_board_id': original_board_id,
            'original_list_id': original_list_id,
            'synced_at': datetime.now().isoformat()
        })
    
    def remove_mapping(self, original_card_id: str = None, weekly_card_id: str = None):
        """Remove mapping entry"""
        self.mapping['mappings'] = [
            m for m in self.mapping['mappings']
            if not ((original_card_id and m['original_card_id'] == original_card_id) or
                   (weekly_card_id and m['weekly_card_id'] == weekly_card_id))
        ]
    
    def copy_card_to_weekly(self, original_card: Dict, project_board: Dict):
        """Copy a card to the Weekly Milestone board"""
        # Check if already copied
        if self.find_mapping(original_card_id=original_card['id']):
            logger.info(f"Card already on Weekly board: {original_card['name']}")
            return
        
        # Prepare card description with link to original
        original_url = original_card.get('shortUrl', original_card.get('url', ''))
        new_description = f"**Original Card:** {original_url}\n\n{original_card.get('desc', '')}"
        
        # Create new card on Weekly board
        new_card_params = {
            'idList': self.config['lists']['this_week'],
            'name': original_card['name'],
            'desc': new_description,
            'pos': 'top'
        }
        
        # Copy due date if exists
        if original_card.get('due'):
            new_card_params['due'] = original_card['due']
        
        new_card = self.api_request('POST', 'cards', params=new_card_params)
        
        if not new_card:
            logger.error(f"Failed to create card: {original_card['name']}")
            return
        
        logger.info(f"✓ Created card on Weekly board: {original_card['name']}")
        
        # Add project label
        label_id = project_board['weekly_label_id']
        self.api_request('POST', f"cards/{new_card['id']}/idLabels", params={'value': label_id})
        
        # Add "This Week" label to Weekly card so it can be removed from either location
        self.api_request('POST', f"cards/{new_card['id']}/labels", params={'color': 'orange', 'name': 'This Week'})
        
        # Copy members
        for member_id in original_card.get('idMembers', []):
            self.api_request('POST', f"cards/{new_card['id']}/idMembers", params={'value': member_id})
        
        # Add comment to original card
        board_url = self.config.get('weekly_board_url', f"https://trello.com/b/{self.weekly_board_id}")
        comment = f"📅 This card has been added to the [Weekly Milestone board]({board_url})"
        self.api_request('POST', f"cards/{original_card['id']}/actions/comments", params={'text': comment})
        
        # Store mapping
        self.add_mapping(
            original_card['id'],
            new_card['id'],
            project_board['id'],
            original_card['idList']
        )
        
        self.stats['pulled'] += 1
    
    def sync_card_status(self, mapping: Dict):
        """Sync status between original and weekly cards"""
        original_card = self.get_card(mapping['original_card_id'])
        weekly_card = self.get_card(mapping['weekly_card_id'])
        
        if not original_card or not weekly_card:
            logger.warning(f"Card not found for mapping: {mapping}")
            return
        
        # Check if weekly card moved to "Completed"
        if weekly_card['idList'] == self.config['lists']['completed']:
            # Move original card to completed (if it has a completed-like list)
            # For now, just add a comment
            if not original_card.get('closed', False):
                comment = "✅ Marked as completed on Weekly Milestone board"
                self.api_request('POST', f"cards/{original_card['id']}/actions/comments", params={'text': comment})
                logger.info(f"Synced completion: {original_card['name']}")
                self.stats['synced'] += 1
        
        # Check if original card is closed/archived
        if original_card.get('closed', False):
            # Move weekly card to completed
            if weekly_card['idList'] != self.config['lists']['completed']:
                self.api_request('PUT', f"cards/{weekly_card['id']}", params={'idList': self.config['lists']['completed']})
                logger.info(f"Moved to completed (original closed): {weekly_card['name']}")
                self.stats['synced'] += 1
    
    def cleanup_removed_labels(self):
        """Remove cards from Weekly board when 'This Week' label is removed"""
        for mapping in self.mapping['mappings'][:]:  # Copy list to allow modification during iteration
            original_card = self.get_card(mapping['original_card_id'])
            weekly_card = self.get_card(mapping['weekly_card_id'])
            
            if not original_card:
                # Original card was deleted
                logger.info(f"Original card deleted, removing from Weekly board")
                if weekly_card:
                    self.api_request('DELETE', f"cards/{mapping['weekly_card_id']}")
                self.remove_mapping(weekly_card_id=mapping['weekly_card_id'])
                self.stats['removed'] += 1
                continue
            
            if not weekly_card:
                # Weekly card was manually deleted
                logger.info(f"Weekly card deleted manually, cleaning up mapping")
                comment = "🔄 Removed from Weekly Milestone board (card deleted)"
                self.api_request('POST', f"cards/{original_card['id']}/actions/comments", params={'text': comment})
                self.remove_mapping(weekly_card_id=mapping['weekly_card_id'])
                self.stats['removed'] += 1
                continue
            
            # Check if "This Week" label still exists on EITHER card
            original_has_label = any(label.get('name') == self.config['trigger_label'] for label in original_card.get('labels', []))
            weekly_has_label = any(label.get('name') == self.config['trigger_label'] for label in weekly_card.get('labels', []))
            
            # If label removed from either card, clean up
            if not original_has_label or not weekly_has_label:
                removed_from = "original card" if not original_has_label else "Weekly board"
                logger.info(f"'This Week' label removed from {removed_from}: {original_card['name']}")
                
                # Delete from Weekly board
                self.api_request('DELETE', f"cards/{mapping['weekly_card_id']}")
                
                # Add comment to original
                comment = f"🔄 Removed from Weekly Milestone board (label removed from {removed_from})"
                self.api_request('POST', f"cards/{original_card['id']}/actions/comments", params={'text': comment})
                
                # Remove mapping
                self.remove_mapping(weekly_card_id=mapping['weekly_card_id'])
                self.stats['removed'] += 1
    
    def get_all_boards(self) -> List[Dict]:
        """Get all boards user has access to across all workspaces"""
        boards = self.api_request('GET', 'members/me/boards', {'fields': 'name,id'})
        if not boards:
            return []
        
        # Filter out the Weekly Milestone board itself
        filtered_boards = [b for b in boards if b['id'] != self.weekly_board_id]
        return filtered_boards
    
    def get_or_create_project_label(self, board_name: str) -> str:
        """Get or create label for a project board on Weekly board"""
        # Check if label already exists
        weekly_labels = self.api_request('GET', f'boards/{self.weekly_board_id}/labels')
        if weekly_labels:
            for label in weekly_labels:
                if label.get('name') == board_name:
                    return label['id']
        
        # Create new label (cycle through colors)
        colors = ['blue', 'green', 'yellow', 'orange', 'red', 'purple', 'pink', 'lime', 'sky', 'black']
        color_index = len(weekly_labels or []) % len(colors)
        
        new_label = self.api_request('POST', 'labels', params={
            'name': board_name,
            'color': colors[color_index],
            'idBoard': self.weekly_board_id
        })
        
        return new_label['id'] if new_label else None
    
    def pull_cards_to_weekly(self):
        """Pull all cards with 'This Week' label from ALL boards to Weekly board"""
        logger.info("=" * 80)
        logger.info("PULLING CARDS TO WEEKLY BOARD (SCANNING ALL BOARDS)")
        logger.info("=" * 80)
        
        # Get all boards user has access to
        all_boards = self.get_all_boards()
        logger.info(f"\nFound {len(all_boards)} boards across all workspaces")
        logger.info("Scanning for 'This Week' label...\n")
        
        boards_with_cards = 0
        
        for board in all_boards:
            board_id = board['id']
            board_name = board['name']
            
            logger.info(f"Scanning: {board_name}")
            cards = self.get_cards_with_label(board_id, self.config['trigger_label'])
            
            if len(cards) > 0:
                boards_with_cards += 1
                logger.info(f"  ✓ Found {len(cards)} card(s) with '{self.config['trigger_label']}' label")
                
                # Get or create label for this board
                label_id = self.get_or_create_project_label(board_name)
                
                # Create pseudo project_board object for compatibility
                project_board = {
                    'id': board_id,
                    'name': board_name,
                    'weekly_label_id': label_id
                }
                
                for card in cards:
                    self.copy_card_to_weekly(card, project_board)
        
        logger.info(f"\nScan complete: {boards_with_cards} boards had cards with 'This Week' label")
    
    def sync_status_changes(self):
        """Sync status changes between boards"""
        logger.info("\n" + "=" * 80)
        logger.info("SYNCING STATUS CHANGES")
        logger.info("=" * 80)
        
        for mapping in self.mapping['mappings']:
            self.sync_card_status(mapping)
    
    def run(self):
        """Main execution"""
        logger.info("╔" + "=" * 78 + "╗")
        logger.info("║" + " " * 20 + "WEEKLY MILESTONE SYNC STARTED" + " " * 29 + "║")
        logger.info("║" + f" {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ".center(78) + "║")
        logger.info("╚" + "=" * 78 + "╝")
        
        try:
            # Step 1: Pull cards with "This Week" label
            self.pull_cards_to_weekly()
            
            # Step 2: Sync status changes
            self.sync_status_changes()
            
            # Step 3: Cleanup removed labels
            self.cleanup_removed_labels()
            
            # Save mapping
            self.save_mapping()
            
            # Print summary
            logger.info("\n" + "=" * 80)
            logger.info("SYNC SUMMARY")
            logger.info("=" * 80)
            logger.info(f"Cards Pulled: {self.stats['pulled']}")
            logger.info(f"Status Synced: {self.stats['synced']}")
            logger.info(f"Cards Removed: {self.stats['removed']}")
            logger.info(f"Errors: {self.stats['errors']}")
            logger.info(f"Total Mapped Cards: {len(self.mapping['mappings'])}")
            logger.info("=" * 80)
            
            if self.stats['errors'] > 0:
                sys.exit(1)
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            sys.exit(1)


if __name__ == '__main__':
    sync = TrelloWeeklySync()
    sync.run()

