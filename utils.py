import json
import os
from datetime import datetime
import shutil

SAVE_FILE = "save.json"
BACKUP_DIR = "saves_backup"

def save_game(state):
    """Save game with backup and error handling"""
    try:
        # Create backup directory if it doesn't exist
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # Create backup of existing save
        if os.path.exists(SAVE_FILE):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(BACKUP_DIR, f"save_backup_{timestamp}.json")
            shutil.copy2(SAVE_FILE, backup_file)
        
        # Add metadata to save
        enhanced_state = {
            "version": "2.0",
            "saved_at": datetime.now().isoformat(),
            "game_data": state
        }
        
        # Save with atomic write
        temp_file = f"{SAVE_FILE}.tmp"
        with open(temp_file, "w", encoding='utf-8') as f:
            json.dump(enhanced_state, f, indent=2, ensure_ascii=False)
        
        # Atomic rename
        os.replace(temp_file, SAVE_FILE)
        
        # Clean old backups (keep last 5)
        cleanup_old_backups()
        
        return True
        
    except Exception as e:
        print(f"Save failed: {e}")
        return False

def load_game():
    """Load game with better error handling"""
    if not os.path.exists(SAVE_FILE):
        return None
    
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle different save formats
        if "version" in data and "game_data" in data:
            return data["game_data"]  # New format
        else:
            return data  # Legacy format
            
    except json.JSONDecodeError as e:
        print(f"Save file corrupted: {e}")
        return try_backup_recovery()
    except Exception as e:
        print(f"Load failed: {e}")
        return None

def try_backup_recovery():
    """Attempt to recover from backup files"""
    if not os.path.exists(BACKUP_DIR):
        return None
    
    backup_files = [f for f in os.listdir(BACKUP_DIR) if f.startswith("save_backup_")]
    if not backup_files:
        return None
    
    # Try most recent backup
    backup_files.sort(reverse=True)
    
    for backup_file in backup_files[:3]:  # Try last 3 backups
        try:
            backup_path = os.path.join(BACKUP_DIR, backup_file)
            with open(backup_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"Recovered from backup: {backup_file}")
            return data.get("game_data", data)
            
        except Exception:
            continue
    
    return None

def cleanup_old_backups(keep_count=5):
    """Keep only the most recent backup files"""
    if not os.path.exists(BACKUP_DIR):
        return
    
    backup_files = [f for f in os.listdir(BACKUP_DIR) if f.startswith("save_backup_")]
    if len(backup_files) <= keep_count:
        return
    
    # Sort by creation time and remove oldest
    backup_paths = [(f, os.path.getctime(os.path.join(BACKUP_DIR, f))) for f in backup_files]
    backup_paths.sort(key=lambda x: x[1], reverse=True)
    
    for file_name, _ in backup_paths[keep_count:]:
        try:
            os.remove(os.path.join(BACKUP_DIR, file_name))
        except Exception:
            pass

def get_save_info():
    """Get information about the current save file"""
    if not os.path.exists(SAVE_FILE):
        return None
    
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if "saved_at" in data:
            return {
                "saved_at": data["saved_at"],
                "version": data.get("version", "1.0"),
                "has_game_data": "game_data" in data
            }
        else:
            # Legacy save file
            stat = os.stat(SAVE_FILE)
            return {
                "saved_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "version": "1.0 (legacy)",
                "has_game_data": True
            }
            
    except Exception:
        return None
