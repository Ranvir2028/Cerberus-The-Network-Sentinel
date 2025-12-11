# 🐕 Cerberus: The Network Sentinel

A Python-powered network monitoring tool that scans your home network, lists all connected devices, and alerts you to unknown intruders. Cerberus stands guard over your network like the mythical three-headed dog, keeping watch 24/7.

## ✨ Features

- **🔍 Automatic Network Detection** - Intelligently discovers your router and network configuration
- **📱 Device Discovery** - Lists all connected devices with IP and MAC addresses
- **🚨 Intruder Alerts** - Notifies you when unknown devices join your network
- **🎓 Learning Mode** - First-time setup learns current devices as trusted
- **📊 Comprehensive Logging** - Detailed activity logs with console/file output
- **🛠️ Network Diagnostics** - Built-in tools for debugging network setup
- **🖥️ Cross-Platform** - Works seamlessly on Linux, macOS, and Windows

## 🛠️ Tech Stack

| Layer              | Technologies       |
|--------------------|--------------------|
| **Core**           | Python 3.7+        |
| **Networking**     | Scapy, Netifaces   |
| **Data Handling**  | JSON               |
| **Architecture**   | Modular Design, OOP|

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Administrative privileges (for network scanning)

### Installation

```bash
# Clone the repository
git clone https://github.com/Ranvir2028/Cerberus-The-Network-Sentinel.git
cd Cerberus_Network_Sentinel

# Install dependencies
pip install -r requirements.txt
```

### Running Cerberus

```bash
# On Linux/Mac (requires sudo)
sudo python3 cerberus_scan.py

# On Windows (Run as Administrator)
python cerberus_scan.py
```

## 📁 Project Structure

```
cerberus/
├── cerberus_scan.py      # Main surveillance script
├── cerberus_logger.py    # Logging module
├── router_detector.py    # Network detection engine
├── requirements.txt      # Dependencies
├── known_devices.json    # Trusted devices (auto-generated)
└── cerberus.log         # Activity logs (auto-generated)
```

## 🎯 How It Works

### First Run - Learning Mode
When you run Cerberus for the first time, it enters **learning mode**:
1. Scans your entire network
2. Lists all discovered devices
3. Saves them as "trusted" in `known_devices.json`
4. You now have a baseline of approved devices

### Surveillance Mode
On every subsequent run:
1. **Scans network** every 60 seconds (configurable)
2. **Compares** found devices against trusted list
3. **Alerts** immediately if unknown devices appear
4. **Logs** all activity with timestamps

### Intelligent Detection
Cerberus uses multiple techniques:
- **ARP Scanning** for device discovery
- **Wake-up Broadcast** to detect sleeping devices
- **Router Detection** for automatic network configuration
- **MAC Address Tracking** for device identification

## 🔧 Configuration

Customize settings in `cerberus_scan.py`:

| Setting           | Default  | Description                 |
|-------------------|----------|-----------------------------|
| `SCAN_INTERVAL`   | `60`     | Seconds between scans       |
| `TARGET_NETWORK`  | `None`   | Auto-detected (recommended) |

### Advanced Logging
```python
# In cerberus_scan.py
logger = cerberus_logger.setup_logging(
    log_file="cerberus.log",
    level="INFO",  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    silent_mode=False  # Set True to disable console output
)
```

## 📊 Sample Output

```
==================================================
PROJECT CERBERUS: The Network Sentinel
==================================================
✅ Network detected: 192.168.1.0/24
🏠 Router: 192.168.1.1
📡 Your IP: 192.168.1.100
🔄 Interface: wlan0
--------------------------------------------------
Loaded 5 trusted devices
🐕 Cerberus is watching...
--------------------------------------------------
Scan #1: Found 6 devices
🚨 ALERT: 1 unknown device detected!
⚠️ INTRUDER: 192.168.1.105 - aa:bb:cc:dd:ee:ff
```

## 🛡️ Security & Ethics

**Important Disclaimer:**
- 🔒 Only scan networks you own or have explicit permission to monitor
- 📚 This tool is for **educational purposes and authorized home use**
- ⚖️ Respect privacy laws and network policies
- 🏠 Perfect for home network security, smart home monitoring, and learning

## 🐛 Troubleshooting

### Common Issues

**"Permission denied" on Linux/Mac**
```bash
# Use sudo for network scanning
sudo python3 cerberus_scan.py
```

**No devices found**
1. Check your network connection
2. Ensure you're on the correct Wi-Fi/ethernet
3. Try running `network_debug()` in main() for diagnostics

**Scapy installation issues**
```bash
# Linux fix
sudo apt-get install python3-scapy
```

## 👨‍💻 Author

**Harshwardhan S. Ranvir**  
🎓 Computer Science & Networking Enthusiast  
🔧 Creator of Project Cerberus  
💡 Passionate about network security and Python automation  
📫 [harshwardhanranvir@gmail.com]

---

*Cerberus stands guard. Your network is protected.* 🐕✨

---