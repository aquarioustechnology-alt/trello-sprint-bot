#!/usr/bin/env python3
"""
Setup "This Week" Label on All Boards
Creates the "This Week" label on all boards for easy selection by users.
"""

import os
import sys
import requests
from typing import List, Dict

# Color for "This Week" label (orange)
LABEL_COLOR = 'orange'
LABEL_NAME = 'This Week'

class LabelSetup:
    def __init__(self):
        self.api_key = os.getenv('TRELLO_API_KEY')
        self.api_token = os.getenv('TRELLO_API_TOKEN')
        
        if not self.api_key or not self.api_token:
            print("Error: TRELLO_API_KEY and TRELLO_API_TOKEN environment variables required")
            sys.exit(1)
        
        self.base_url = 'https://api.trello.com/1'
        self.stats = {
            'boards_scanned': 0,
            'labels_created': 0,
            'labels_already_exist': 0,
            'errors': 0
        }
    
    def api_request(self, method: str, endpoint: str, params: Dict = None) -> any:
        """Make API request to Trello"""
        url = f"{self.base_url}/{endpoint}"
        auth_params = {'key': self.api_key, 'token': self.api_token}
        
        if params:
            auth_params.update(params)
        
        try:
            if method == 'GET':
                response = requests.get(url, params=auth_params)
            elif method == 'POST':
                response = requests.post(url, params=auth_params)
            else:
                print(f"Error: Unsupported method {method}")
                return None
            
            response.raise_for_status()
            return response.json() if response.text else None
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            self.stats['errors'] += 1
            return None
    
    def get_all_boards(self) -> List[Dict]:
        """Get all boards user has access to"""
        boards = self.api_request('GET', 'members/me/boards', {'fields': 'name,id'})
        return boards if boards else []
    
    def board_has_label(self, board_id: str) -> bool:
        """Check if board already has 'This Week' label"""
        labels = self.api_request('GET', f'boards/{board_id}/labels')
        if not labels:
            return False
        
        return any(label.get('name') == LABEL_NAME for label in labels)
    
    def create_label(self, board_id: str, board_name: str) -> bool:
        """Create 'This Week' label on a board"""
        result = self.api_request('POST', 'labels', {
            'name': LABEL_NAME,
            'color': LABEL_COLOR,
            'idBoard': board_id
        })
        
        if result:
            print(f"  ✅ Created label on: {board_name}")
            self.stats['labels_created'] += 1
            return True
        else:
            print(f"  ❌ Failed to create label on: {board_name}")
            return False
    
    def setup_all_boards(self):
        """Setup 'This Week' label on all boards"""
        print("=" * 80)
        print(f"SETTING UP '{LABEL_NAME}' LABEL ON ALL BOARDS")
        print("=" * 80)
        print()
        
        # Get all boards
        print("Fetching all boards...")
        boards = self.get_all_boards()
        self.stats['boards_scanned'] = len(boards)
        print(f"Found {len(boards)} boards\n")
        
        if not boards:
            print("No boards found!")
            return
        
        print(f"Creating '{LABEL_NAME}' labels...\n")
        
        # Process each board
        for board in boards:
            board_id = board['id']
            board_name = board['name']
            
            # Check if label already exists
            if self.board_has_label(board_id):
                self.stats['labels_already_exist'] += 1
            else:
                # Create the label
                self.create_label(board_id, board_name)
        
        # Print summary
        print()
        print("=" * 80)
        print("SETUP SUMMARY")
        print("=" * 80)
        print(f"Boards Scanned: {self.stats['boards_scanned']}")
        print(f"Labels Created: {self.stats['labels_created']}")
        print(f"Labels Already Exist: {self.stats['labels_already_exist']}")
        print(f"Errors: {self.stats['errors']}")
        print("=" * 80)
        print()
        
        if self.stats['labels_created'] > 0:
            print(f"✅ Successfully created '{LABEL_NAME}' label on {self.stats['labels_created']} boards!")
        else:
            print(f"ℹ️  All boards already have the '{LABEL_NAME}' label.")
        
        if self.stats['errors'] > 0:
            print(f"⚠️  {self.stats['errors']} errors occurred during setup.")


if __name__ == '__main__':
    setup = LabelSetup()
    setup.setup_all_boards()

