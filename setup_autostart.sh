#!/bin/bash
# Setup script for Mechanical Keyboard Sound service

echo "=== Mechanical Keyboard Sound - Auto-start Setup ==="
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "❌ Please DO NOT run this script as root/sudo"
    echo "   Run it as your regular user: ./setup_autostart.sh"
    exit 1
fi

# Get the current user and paths
CURRENT_USER=$(whoami)
SCRIPT_DIR=$(pwd)
SCRIPT_PATH="$SCRIPT_DIR/mech_keyboard_sound.py"

# Check if the Python script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Error: mech_keyboard_sound.py not found in current directory"
    echo "   Please run this script from the directory containing mech_keyboard_sound.py"
    exit 1
fi

# Make the Python script executable
chmod +x "$SCRIPT_PATH"

echo "Choose auto-start method:"
echo "1. Desktop Autostart (recommended) - starts with your desktop session"
echo "2. Systemd User Service - more control, runs in background"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" == "1" ]; then
    # Desktop Autostart method
    AUTOSTART_DIR="$HOME/.config/autostart"
    DESKTOP_FILE="$AUTOSTART_DIR/mech-keyboard-sound.desktop"
    
    mkdir -p "$AUTOSTART_DIR"
    
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Type=Application
Name=Mechanical Keyboard Sounds
Comment=Play mechanical keyboard sounds when typing
Exec=python3 $SCRIPT_PATH
Icon=input-keyboard
Terminal=false
Categories=Utility;
X-GNOME-Autostart-enabled=true
EOF
    
    chmod +x "$DESKTOP_FILE"
    
    echo ""
    echo "✓ Desktop autostart configured!"
    echo ""
    echo "The app will now start automatically when you log in."
    echo ""
    echo "To test now, run: python3 $SCRIPT_PATH"
    echo "To disable autostart: rm $DESKTOP_FILE"
    
elif [ "$choice" == "2" ]; then
    # Systemd user service
    SERVICE_DIR="$HOME/.config/systemd/user"
    SERVICE_FILE="$SERVICE_DIR/mech-keyboard.service"
    
    mkdir -p "$SERVICE_DIR"
    
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=Mechanical Keyboard Sound Simulator
After=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $SCRIPT_PATH
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF
    
    echo ""
    echo "✓ Systemd user service created!"
    echo ""
    echo "Run these commands to enable and start:"
    echo "  systemctl --user daemon-reload"
    echo "  systemctl --user enable mech-keyboard.service"
    echo "  systemctl --user start mech-keyboard.service"
    echo ""
    echo "Useful commands:"
    echo "  Status:  systemctl --user status mech-keyboard.service"
    echo "  Stop:    systemctl --user stop mech-keyboard.service"
    echo "  Restart: systemctl --user restart mech-keyboard.service"
    echo "  Disable: systemctl --user disable mech-keyboard.service"
    echo "  Logs:    journalctl --user -u mech-keyboard.service -f"
    
else
    echo "Invalid choice. Exiting."
    exit 1
fi

echo ""
