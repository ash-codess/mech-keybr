# 🎹 Mechanical Keyboard Sound Simulator for Linux

A lightweight Linux application that plays mechanical keyboard sounds as you type. Perfect for enjoying that satisfying Cherry MX click without the actual mechanical keyboard!
<img width="228" height="128" alt="image" src="https://github.com/user-attachments/assets/a977827a-40fc-480d-9b0d-d5a187d66e0d" />


![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)

## ✨ Features

- 🎵 **Multiple Sound Profiles** - Switch between different keyboard types (Cherry MX Blue, Brown, Black, etc.)
- 🎯 **Key-Specific Sounds** - Each key plays its unique sound (Space, Enter, Backspace, etc.)
- 📦 **Sprite Sheet Support** - Space-efficient audio format (single .ogg file + config.json)
- 🔊 **Volume Control** - Adjust sound levels to your preference
- 🚀 **Auto-start on Boot** - Set it up once, enjoy forever
- 🐛 **Debug Mode** - See exactly which keys are being pressed and sounds played
- 🪶 **Lightweight** - Minimal resource usage, runs silently in background

## 📋 Requirements

- Python 3.8+
- Linux with X11 or Wayland
- Audio output device

## 🚀 Quick Start

### 1. Install Dependencies

```bash
sudo apt update
sudo apt install python3-pygame python3-pynput python3-tk -y
```

### 2. Download or Clone

```bash
git clone https://github.com/yourusername/mech-keyboard-sound.git
cd mech-keyboard-sound
```

### 3. Run the Application

```bash
python3 mech_keyboard_sound.py
```

### 4. Add Sound Profile

1. Click **"Add Profile"**
2. Enter a name (e.g., "Cherry MX Brown")
3. Select folder containing:
   - `sound.ogg` - Master audio file with all key sounds
   - `config.json` - Key mapping definitions

### 5. Enable Sounds

1. Select your profile from dropdown
2. Adjust volume if needed
3. Click **"Enable Sounds"**
4. Start typing! 🎉

## 🔧 Auto-start Setup

To automatically start the app when you log in:

```bash
chmod +x setup_autostart.sh
./setup_autostart.sh
```

Choose option 1 (Desktop Autostart) for easiest setup.

### Manual Autostart Setup

Create `~/.config/autostart/mech-keyboard-sound.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Mechanical Keyboard Sounds
Exec=python3 /full/path/to/mech_keyboard_sound.py
Terminal=false
X-GNOME-Autostart-enabled=true
```

## 📁 Sound Profile Format

### Sprite Sheet Format (Recommended)

Most space-efficient. Your profile folder should contain:

```
my-keyboard-sound/
├── sound.ogg      # Single audio file with all sounds
└── config.json    # Key mappings
```

**config.json structure:**

```json
{
  "defines": {
    "KeyA": [31542, 170],
    "KeyB": [40621, 214],
    "Space": [51541, 287],
    "Return": [36902, 234],
    ...
  },
  "name": "Cherry MX Brown",
  "key_define_type": "single"
}
```

Format: `"KeyName": [start_millisecond, duration_millisecond]`

### Supported Keys

All standard keyboard keys are supported:
- Letters: `KeyA` to `KeyZ`
- Numbers: `Num0` to `Num9`
- Special: `Space`, `Return`, `Backspace`, `Tab`, `Escape`
- Modifiers: `ShiftLeft`, `ShiftRight`, `ControlLeft`, `ControlRight`, `Alt`, `AltGr`
- Function keys: `F1` to `F12`
- Navigation: `UpArrow`, `DownArrow`, `LeftArrow`, `RightArrow`, `Home`, `End`, `PageUp`, `PageDown`
- And more!

## 🎨 Finding Sound Packs

You can:
1. **Extract from existing mechanical keyboard simulators**
2. **Record your own** mechanical keyboard
3. **Download free sound packs** (search for "mechanical keyboard sound pack")
4. **Use the included sample** (if provided)

### Creating Your Own Sound Pack

Record individual key sounds and organize them as:

```
my-recording/
├── sound.ogg
└── config.json
```

Use audio editing software (Audacity, ffmpeg) to:
1. Record all keys in sequence
2. Note timestamps for each key
3. Create config.json with mappings

## 🎮 Usage

### GUI Controls

- **Sound Profile**: Select which keyboard sound to use
- **Add Profile**: Add a new sound profile folder
- **Remove Profile**: Delete selected profile
- **Enable/Disable**: Toggle keyboard sounds on/off
- **Volume**: Adjust sound volume (0-100%)
- **Debug Mode**: Show key press events in terminal

### Keyboard Shortcuts

- Type normally - sounds play automatically
- Each key triggers its specific sound from the profile

## 🐛 Troubleshooting

### No sound when typing

1. Check volume slider is not at 0
2. Enable Debug Mode to see if keys are detected
3. Verify sound.ogg and config.json exist in profile folder
4. Test system audio with another application

### Keys not detected

1. Ensure python3-pynput is installed
2. Check you're running with proper permissions
3. Some keys might need X11 (won't work over SSH)

### App doesn't start automatically

1. Verify autostart file exists: `ls ~/.config/autostart/`
2. Check file permissions: `chmod +x ~/.config/autostart/mech-keyboard-sound.desktop`
3. Test manually first: `python3 mech_keyboard_sound.py`

### High CPU usage

- This is normal during rapid typing
- Sprite sheet format is more efficient than individual files
- Reduce number of simultaneous channels if needed

## 🔊 Audio Optimization Tips

For best performance and smallest file size:

```bash
# Convert to OGG with optimal settings
ffmpeg -i input.wav -c:a libvorbis -q:a 4 -ar 44100 -ac 1 output.ogg

# Parameters:
# -q:a 4       : Quality level 4 (good balance)
# -ar 44100    : 44.1kHz sample rate
# -ac 1        : Mono (stereo not needed for keyboard sounds)
```

## 📝 Configuration

Settings are stored in `~/.mech_keyboard_config.json`:

```json
{
  "profiles": {
    "Cherry MX Brown": "/path/to/sound/folder"
  },
  "current_profile": "Cherry MX Brown"
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### To-Do List

- [ ] Add more default sound profiles
- [ ] Support for individual .wav/.ogg files (non-sprite sheet)
- [ ] GUI theme customization
- [ ] Per-key volume adjustment
- [ ] Sound randomization options
- [ ] Wayland-specific improvements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [pygame](https://www.pygame.org/) for audio
- [pynput](https://github.com/moses-palmer/pynput) for keyboard detection
- Inspired by various mechanical keyboard enthusiasts

## 💬 Support

Found a bug? Have a feature request? [Open an issue](https://github.com/yourusername/mech-keyboard-sound/issues)

---

**Enjoy your virtual mechanical keyboard! 🎹✨**
