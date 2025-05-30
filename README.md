![kalilinux](https://github.com/user-attachments/assets/f7fd6c55-e323-40db-9883-1b3b32071867)
![2025-05-31_00-51](https://github.com/user-attachments/assets/1eb25e62-3f18-4367-a69a-5c79f1e863ae)
![2025-05-31_00-53](https://github.com/user-attachments/assets/23aa08dc-ba2b-4ed0-a192-fc5300b5e513)

# Kali Linux Control Panel

A comprehensive GUI-based control panel for Kali Linux systems, designed to simplify common penetration testing and system administration tasks through an intuitive graphical interface.

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-linux-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Features

### System Management
- **System Updates**: Quick access to `apt update`, `apt upgrade`, and package management
- **System Cleanup**: Automated system cleaning (cache, temporary files, unused packages)
- **Package Repair**: Fix broken packages and dependencies
- **System Reboot**: Safe system restart with confirmation

### Network Interface Management
- **Interface Selection**: Dynamic detection and selection of network interfaces
- **Monitor Mode**: Switch wireless interfaces to monitor mode for packet capture
- **Managed Mode**: Return interfaces to normal managed mode
- **Interface Restart**: Reset network interfaces and NetworkManager
- **Real-time Status**: Live monitoring of interface modes

### Network Configuration
- **MAC Address Spoofing**: 
  - Random MAC generation
  - Custom MAC address assignment
  - Interface-specific MAC changes
- **IP Configuration**:
  - DHCP IP renewal
  - Static IP assignment
  - Gateway and netmask configuration
  - Support for both CIDR and dotted decimal notation

### Firewall Management
- **UFW Control**: Enable/disable Ubuntu Firewall (UFW)
- **Real-time Status**: Live firewall status monitoring
- **Firewall Reset**: Complete firewall rules reset
- **Visual Indicators**: Color-coded status display

### System Information
- **Hardware Details**: CPU, RAM, and disk usage information
- **Network Information**: Local IP, public IP, MAC addresses
- **System Status**: OS version, hostname, and system statistics
- **Firewall Status**: Current firewall configuration and rules

## 📋 Prerequisites

### System Requirements
- **Operating System**: Kali Linux (recommended) or any Debian-based Linux distribution
- **Python Version**: Python 3.6 or higher
- **Privileges**: Root/sudo access required for most features

### Required Packages

Install the necessary system packages:

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install core networking tools
sudo apt install -y aircrack-ng iw ufw network-manager

# Install network utilities
sudo apt install -y net-tools wireless-tools rfkill curl

# Install Python package manager (if not already installed)
sudo apt install -y python3-pip
```

### Python Dependencies

Install required Python packages:

```bash
# Install Python dependencies
pip3 install pillow

# Alternative installation method
sudo apt install -y python3-pil python3-pil.imagetk
```

## 🛠️ Installation

### Method 1: Git Clone (Recommended)

```bash
# Clone the repository
https://github.com/Hsiodos1988/Kali_Linux_Control_Panel.git

# Navigate to the project directory
cd kali-control-panel

# Make the script executable
chmod +x kali_control_panel.py

# Run the application
sudo python3 kali_control_panel.py
```

### Method 2: Direct Download

```bash
# Download the script directly
wget https://raw.githubusercontent.com/yourusername/kali-control-panel/main/kali_control_panel.py
https://github.com/Hsiodos1988/Kali_Linux_Control_Panel.git
# Make it executable
chmod +x kali_control_panel.py

# Run the application
sudo python3 kali_control_panel.py
```

## 🚀 Usage

### Starting the Application

```bash
# Run with sudo for full functionality
sudo python3 kali_control_panel.py

# Or run without sudo (limited functionality)
python3 kali_control_panel.py
```

### Basic Operations

1. **Interface Management**:
   - Click "Interface" button to select your network interface
   - Use "Monitor"/"Managed" buttons to switch modes
   - Monitor the "Mode" status indicator

2. **System Updates**:
   - Click "Update" to refresh package lists
   - Click "Upgrade" to install system updates
   - Use "Fix Broken" to repair package issues

3. **Network Configuration**:
   - Use "Change MAC" for MAC address spoofing
   - Use "Change IP" for network configuration
   - Monitor changes in "System Info"

4. **Firewall Control**:
   - Use "Toggle Firewall" to enable/disable UFW
   - Monitor status with color-coded indicators
   - Use "Restart Firewall" to reset rules

### Advanced Features

#### Monitor Mode Setup for WiFi Auditing
```bash
# The application handles these commands automatically:
# 1. Select your wireless interface (e.g., wlan0)
# 2. Click "Monitor" to enable monitor mode
# 3. Interface is ready for tools like airodump-ng
```

#### MAC Address Spoofing
```bash
# Automated through GUI:
# 1. Click "Change MAC"
# 2. Choose random or custom MAC
# 3. Interface automatically restarts with new MAC
```

## ⚠️ Important Notes

### Security and Legal Considerations
- **Educational Use Only**: This tool is designed for educational purposes and authorized penetration testing
- **Legal Compliance**: Only use on networks you own or have explicit permission to test
- **Responsible Use**: Always follow ethical hacking guidelines and local laws

### System Requirements
- **Root Access**: Many features require root privileges
- **Network Interfaces**: Ensure your hardware supports monitor mode (for wireless auditing)
- **Firewall**: UFW should be installed and available

### Troubleshooting

#### Common Issues and Solutions

**Issue**: "No interfaces found"
```bash
# Solution: Check network interfaces
ip link show
# Ensure network interfaces are up and available
```

**Issue**: "Permission denied" errors
```bash
# Solution: Run with sudo
sudo python3 kali_control_panel.py
```

**Issue**: Monitor mode not working
```bash
# Solution: Check if interface supports monitor mode
sudo iw phy
# Kill interfering processes
sudo airmon-ng check kill
```

**Issue**: Missing background image
```bash
# Solution: Image file is optional
# Create or download kalilinux.png in the same directory
# Or run without - the application will use a dark theme
```

## 🤝 Contributing

We welcome contributions to improve the Kali Linux Control Panel!

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/kali-control-panel.git

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip3 install pillow
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is provided for educational and authorized testing purposes only. Users are responsible for complying with all applicable laws and regulations. The developers assume no liability for misuse of this software.

## 🔧 Technical Details

### Architecture
- **GUI Framework**: Tkinter (Python standard library)
- **Image Processing**: PIL/Pillow for graphics
- **System Integration**: subprocess module for system commands
- **Network Operations**: Native Linux networking tools (iw, ip, etc.)

### Supported Commands
- `apt update/upgrade` - Package management
- `iw` - Wireless interface configuration
- `ip` - Network interface management  
- `ufw` - Firewall management
- `airmon-ng` - Monitor mode management
- `dhclient` - DHCP operations

## 📞 Support

If you encounter issues or have questions:

1. Check the [Issues](https://github.com/yourusername/kali-control-panel/issues) section
2. Create a new issue with detailed information
3. Include system information and error messages

---

**Made with ❤️ for the cybersecurity community**
