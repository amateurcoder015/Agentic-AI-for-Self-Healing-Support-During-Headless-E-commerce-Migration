import json
import os

def load_tickets(filepath="tickets.json"):
    """
    OBSERVE: Reads the raw support tickets from the file system.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find {filepath}")
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    print(f"--> [OBSERVE] Loaded {len(data)} tickets.")
    return data

def load_system_signals(filepath="system_signals.json"):
    """
    OBSERVE (Phase 2): Reads simulated infrastructure signals.
    """
    if not os.path.exists(filepath):
        return None # Fail silently if no signal file exists
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    print(f"--> [OBSERVE] Loaded system signal: {data['signal']} ({data['value']}%)")
    return data