import json
import os

def load_config():
    """Load configuration from a JSON file."""
    config_file='setup/config.json'
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config


def load_model_config():
    """Load configuration from a JSON file."""
    config_file='setup/model_config.json'
    with open(config_file, 'r') as file:
        model_config = json.load(file)
    return model_config

def ensure_directory_exists(directory):
    """Ensure the specified directory exists; create it if not."""
    
    if not os.path.exists(directory):
        os.makedirs(directory)
