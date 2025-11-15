#!/usr/bin/env python3
"""
Mechanical Keyboard Sound Simulator for Linux
Supports both individual sound files and sprite sheet audio with config.json
Requirements: python3-tk, python3-pynput, python3-pygame
Install: sudo apt install python3-tk python3-pynput python3-pygame
"""

import tkinter as tk
from tkinter import ttk, filedialog
import pygame
from pynput import keyboard
import os
import json
import time

class MechKeyboardSound:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mechanical Keyboard Sounds")
        self.root.geometry("350x220")
        self.root.resizable(False, False)
        
        # Initialize pygame mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(32)
        
        # Config file
        self.config_file = os.path.expanduser("~/.mech_keyboard_config.json")
        self.sound_profiles = {}
        self.current_profile = None
        self.enabled = False
        
        # Key mapping for sprite sheet mode
        self.key_map = {}
        self.sprite_mode = False
        self.master_sound = None
        
        # Load config
        self.load_config()
        
        # Setup GUI
        self.setup_gui()
        
        # Keyboard listener
        self.listener = None
        
    def setup_gui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = ttk.Label(main_frame, text="🎹 Mechanical Keyboard Sounds", 
                                font=('Arial', 12, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Label(main_frame, text="Sound Profile:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.profile_combo = ttk.Combobox(main_frame, width=25, state='readonly')
        self.profile_combo.grid(row=1, column=1, pady=5, padx=(5, 0))
        self.profile_combo.bind('<<ComboboxSelected>>', self.on_profile_change)
        
        add_btn = ttk.Button(main_frame, text="Add Profile", command=self.add_profile)
        add_btn.grid(row=2, column=0, pady=5, sticky=tk.W)
        
        remove_btn = ttk.Button(main_frame, text="Remove Profile", command=self.remove_profile)
        remove_btn.grid(row=2, column=1, pady=5, sticky=tk.E)
        
        self.toggle_btn = ttk.Button(main_frame, text="Enable Sounds", 
                                     command=self.toggle_sounds)
        self.toggle_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.status_label = ttk.Label(main_frame, text="Status: Disabled", 
                                      foreground="red")
        self.status_label.grid(row=4, column=0, columnspan=2)
        
        ttk.Label(main_frame, text="Volume:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.volume_scale = ttk.Scale(main_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                      command=self.on_volume_change)
        self.volume_scale.set(70)
        self.volume_scale.grid(row=5, column=1, pady=5, sticky=(tk.W, tk.E))
        
        self.debug_var = tk.BooleanVar(value=False)
        debug_check = ttk.Checkbutton(main_frame, text="Debug Mode", variable=self.debug_var)
        debug_check.grid(row=6, column=0, columnspan=2, pady=5)
        
        self.update_profile_list()
        
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.sound_profiles = data.get('profiles', {})
                    self.current_profile = data.get('current_profile')
            except:
                pass
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump({
                'profiles': self.sound_profiles,
                'current_profile': self.current_profile
            }, f)
    
    def update_profile_list(self):
        profiles = list(self.sound_profiles.keys())
        self.profile_combo['values'] = profiles
        if self.current_profile and self.current_profile in profiles:
            self.profile_combo.set(self.current_profile)
        elif profiles:
            self.profile_combo.set(profiles[0])
            self.current_profile = profiles[0]
    
    def add_profile(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Sound Profile")
        dialog.geometry("350x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Profile Name:").pack(pady=(10, 5))
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Select folder with sound.ogg + config.json").pack(pady=5)
        ttk.Label(dialog, text="(or folder with individual .wav/.ogg files)").pack()
        
        def select_and_add():
            name = name_entry.get().strip()
            if not name:
                return
            
            folder = filedialog.askdirectory(title="Select Sound Folder")
            if folder:
                self.sound_profiles[name] = folder
                self.save_config()
                self.update_profile_list()
                dialog.destroy()
                print(f"Added profile '{name}' from folder: {folder}")
        
        ttk.Button(dialog, text="Select Folder", command=select_and_add).pack(pady=10)
    
    def remove_profile(self):
        current = self.profile_combo.get()
        if current and current in self.sound_profiles:
            del self.sound_profiles[current]
            self.current_profile = None
            self.save_config()
            self.update_profile_list()
    
    def on_profile_change(self, event):
        self.current_profile = self.profile_combo.get()
        self.save_config()
        if self.enabled:
            self.load_sounds()
    
    def on_volume_change(self, value):
        volume = float(value) / 100.0
        if self.master_sound:
            self.master_sound.set_volume(volume)
    
    def pynput_to_config_key(self, key):
        """Convert pynput key to config.json key name"""
        try:
            # Handle character keys
            if hasattr(key, 'char') and key.char:
                char = key.char.upper()
                if char.isalpha():
                    return f"Key{char}"
                elif char.isdigit():
                    return f"Num{char}"
                else:
                    # Special characters
                    char_map = {
                        ' ': 'Space',
                        '-': 'Minus',
                        '=': 'Equal',
                        '[': 'LeftBracket',
                        ']': 'RightBracket',
                        '\\': 'BackSlash',
                        ';': 'SemiColon',
                        "'": 'Quote',
                        '`': 'BackQuote',
                        ',': 'Comma',
                        '.': 'Dot',
                        '/': 'Slash'
                    }
                    return char_map.get(char, None)
        except AttributeError:
            pass
        
        # Handle special keys
        key_map = {
            keyboard.Key.space: 'Space',
            keyboard.Key.enter: 'Return',
            keyboard.Key.backspace: 'Backspace',
            keyboard.Key.tab: 'Tab',
            keyboard.Key.shift: 'ShiftLeft',
            keyboard.Key.shift_l: 'ShiftLeft',
            keyboard.Key.shift_r: 'ShiftRight',
            keyboard.Key.ctrl: 'ControlLeft',
            keyboard.Key.ctrl_l: 'ControlLeft',
            keyboard.Key.ctrl_r: 'ControlRight',
            keyboard.Key.alt: 'Alt',
            keyboard.Key.alt_l: 'Alt',
            keyboard.Key.alt_r: 'AltGr',
            keyboard.Key.caps_lock: 'CapsLock',
            keyboard.Key.esc: 'Escape',
            keyboard.Key.up: 'UpArrow',
            keyboard.Key.down: 'DownArrow',
            keyboard.Key.left: 'LeftArrow',
            keyboard.Key.right: 'RightArrow',
            keyboard.Key.home: 'Home',
            keyboard.Key.end: 'End',
            keyboard.Key.page_up: 'PageUp',
            keyboard.Key.page_down: 'PageDown',
            keyboard.Key.insert: 'Insert',
            keyboard.Key.delete: 'Delete',
            keyboard.Key.f1: 'F1',
            keyboard.Key.f2: 'F2',
            keyboard.Key.f3: 'F3',
            keyboard.Key.f4: 'F4',
            keyboard.Key.f5: 'F5',
            keyboard.Key.f6: 'F6',
            keyboard.Key.f7: 'F7',
            keyboard.Key.f8: 'F8',
            keyboard.Key.f9: 'F9',
            keyboard.Key.f10: 'F10',
            keyboard.Key.f11: 'F11',
            keyboard.Key.f12: 'F12',
        }
        
        return key_map.get(key, None)
    
    def load_sounds(self):
        """Load sounds from profile folder"""
        if not self.current_profile or self.current_profile not in self.sound_profiles:
            print("ERROR: No profile selected")
            return
        
        folder = self.sound_profiles[self.current_profile]
        
        # Handle old config format (list instead of string)
        if isinstance(folder, list):
            print("WARNING: Old config format detected, removing profile")
            del self.sound_profiles[self.current_profile]
            self.current_profile = None
            self.save_config()
            self.update_profile_list()
            print("Please re-add the profile")
            return
        
        config_path = os.path.join(folder, 'config.json')
        sound_path = os.path.join(folder, 'sound.ogg')
        
        print(f"\n{'='*50}")
        print(f"Loading profile from: {folder}")
        print(f"{'='*50}")
        
        # Check if this is a sprite sheet profile
        if os.path.exists(config_path) and os.path.exists(sound_path):
            print("✓ Found sprite sheet mode (sound.ogg + config.json)")
            self.load_sprite_sheet(sound_path, config_path)
        else:
            print("✗ Sprite sheet mode not available")
            print("  (Missing sound.ogg or config.json)")
    
    def load_sprite_sheet(self, sound_path, config_path):
        """Load sprite sheet audio with config"""
        try:
            # Load the master sound file
            self.master_sound = pygame.mixer.Sound(sound_path)
            volume = self.volume_scale.get() / 100.0
            self.master_sound.set_volume(volume)
            
            # Load the config
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            self.key_map = config.get('defines', {})
            self.sprite_mode = True
            
            print(f"✓ Loaded {len(self.key_map)} key sounds from sprite sheet")
            print(f"  Profile name: {config.get('name', 'Unknown')}")
            
            # Show some sample mappings
            sample_keys = ['KeyA', 'Space', 'Return', 'Backspace']
            for key in sample_keys:
                if key in self.key_map:
                    start, duration = self.key_map[key]
                    print(f"  {key}: {start}ms + {duration}ms")
                    
        except Exception as e:
            print(f"ERROR loading sprite sheet: {e}")
            self.sprite_mode = False
    
    def play_key_sound(self, config_key):
        """Play sound for a specific key from sprite sheet"""
        if not self.sprite_mode or not self.master_sound:
            return
        
        if config_key not in self.key_map:
            if self.debug_var.get():
                print(f"  No sound mapping for: {config_key}")
            return
        
        try:
            start_ms, duration_ms = self.key_map[config_key]
            
            # Get the master sound as array
            sound_array = pygame.sndarray.array(self.master_sound)
            sample_rate = pygame.mixer.get_init()[0]
            
            # Calculate start and end samples
            start_sample = int((start_ms / 1000.0) * sample_rate)
            end_sample = int(((start_ms + duration_ms) / 1000.0) * sample_rate)
            
            # Extract the segment
            segment = sound_array[start_sample:end_sample]
            
            # Create a new sound from the segment
            key_sound = pygame.sndarray.make_sound(segment)
            volume = self.volume_scale.get() / 100.0
            key_sound.set_volume(volume)
            
            # Play it
            key_sound.play()
            
            if self.debug_var.get():
                print(f"  ✓ Played: {config_key} ({start_ms}ms, {duration_ms}ms)")
                
        except Exception as e:
            print(f"ERROR playing sound for {config_key}: {e}")
    
    def on_key_press(self, key):
        """Called when a key is pressed"""
        if not self.enabled:
            return
        
        # Convert pynput key to config key name
        config_key = self.pynput_to_config_key(key)
        
        if self.debug_var.get():
            print(f"[KEY] {key} -> {config_key}")
        
        if config_key:
            self.play_key_sound(config_key)
        else:
            if self.debug_var.get():
                print(f"  Unmapped key: {key}")
    
    def toggle_sounds(self):
        if not self.enabled:
            if not self.current_profile:
                print("ERROR: No profile selected!")
                return
            
            print(f"\n{'='*50}")
            print("ENABLING KEYBOARD SOUNDS")
            print(f"{'='*50}")
            
            self.load_sounds()
            
            if not self.sprite_mode or not self.master_sound:
                print("ERROR: Failed to load sounds!")
                return
            
            self.listener = keyboard.Listener(on_press=self.on_key_press)
            self.listener.start()
            
            self.enabled = True
            self.toggle_btn.config(text="Disable Sounds")
            self.status_label.config(text="Status: Enabled ✓", foreground="green")
            
            print("\n✓ Keyboard sounds ENABLED - Start typing!")
            print("  (Enable 'Debug Mode' to see key mappings)\n")
        else:
            print("\nDisabling keyboard sounds...")
            
            if self.listener:
                self.listener.stop()
                self.listener = None
            
            self.enabled = False
            self.toggle_btn.config(text="Enable Sounds")
            self.status_label.config(text="Status: Disabled", foreground="red")
            
            print("✓ Keyboard sounds DISABLED\n")
    
    def run(self):
        self.root.mainloop()

def main():
    app = MechKeyboardSound()
    app.run()

if __name__ == "__main__":
    main()
