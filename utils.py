import json
import os
import tkinter as tk
from tkinter import messagebox

def load_config():
    """Load configuration from file or return defaults"""
    default_config = {
        'dark_mode': False,
        'input_lang': 'English',
        'output_lang': 'Hindi',
        'output_lang_2': 'French'
    }
    
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default_config

def save_config(config):
    """Save configuration to file"""
    with open('config.json', 'w') as f:
        json.dump(config, f)

def load_icon(window, icon_path="icon.png"):
    """Load window icon with error handling"""
    try:
        icon = tk.PhotoImage(file=icon_path)
        window.iconphoto(False, icon)
    except Exception as e:
        print(f"Could not load icon: {e}")
