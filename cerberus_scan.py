from scapy.all import ARP, Ether, srp, IP, ICMP, send
import time
import json
import cerberus_logger
from router_detector import RouterDetector
from npcap_installer import handle_npcap_installation
import platform
import sys

# Import npcap installer for Windows compatibility
try:
    NPCAP_INSTALLER_AVAILABLE = True
except ImportError:
    NPCAP_INSTALLER_AVAILABLE = False
    print("⚠️ Warning: npcap_installer module not found. Windows users may need to install Npcap manually.")

# CONFIGURATION
KNOWN_DEVICES_FILE = "known_devices.json"
TARGET_NETWORK = None    
SCAN_INTERVAL = 60

# This line is for logging module.
logger = cerberus_logger.setup_logging()

def load_known_devices():
    """It loads the list of trusted MAC addresses from a file."""
    try:
        with open(KNOWN_DEVICES_FILE, 'r') as f:
            devices = json.load(f)
        logger.info(f"Loaded {len(devices)} known devices.")
        return devices
    except FileNotFoundError:
        logger.warning("No known devices file found. Starting learning mode.")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Error reading devices file: {e}")
        return []

def save_known_devices(devices):
    """Saves the list of trusted MAC addresses to a file."""
    try:
        with open(KNOWN_DEVICES_FILE, 'w') as f:
            json.dump(devices, f, indent=4)
        logger.info(f"Saved {len(devices)} devices.")
    except Exception as e:
        logger.error(f"Failed to save devices: {e}.")

def scan_network():
    """Isme wakeup call add kiya hai matlab ping karega har device ko pehle."""
    logger.info(f"Scanning {TARGET_NETWORK}")
    
    try:
        broadcast_ip = '.'.join(TARGET_NETWORK.split('/')[0].split('.')[:3]) + '.255'
        send(IP(dst=broadcast_ip)/ICMP(), verbose=0)
        logger.debug("Sent wake-up broadcast ping to all devices.")
        time.sleep(1)
    except Exception as e:
        logger.debug(f"Wake-up call failed (non-critical): {e}.")

    try:
        # ARP Scan rahega hi taki scapy sabko packet bhej sake. 
        arp_request = ARP(pdst=TARGET_NETWORK)
        ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether_frame / arp_request

        answered_list = srp(packet, timeout=3, verbose=0)[0]
        
        clients = []
        for sent, received in answered_list:
            clients.append({"ip": received.psrc, "mac": received.hwsrc})
        
        logger.info(f"Found {len(clients)} devices.")

        # Har device jo mila hai use log karega ye
        for device in clients:
            logger.debug(f" Device: {device['ip']} -> {device['mac']}")

        return clients
        
    except Exception as e:
        logger.error(f"Scan failed: {e}.")
        return []

def learn_network_mode():
    """First-time setup: Learn all current devices as trusted."""
    logger.info("No known devices list. Starting learning mode now...")
    
    current_devices = scan_network()
    
    if not current_devices:
        logger.error("No devices found!")
        return []
    
    known_macs = [device["mac"] for device in current_devices]
    save_known_devices(known_macs)
    
    logger.info(f"Learned {len(known_macs)} devices:")
    for device in current_devices:
        logger.info(f"  {device["ip"]} -> {device["mac"]}")
        logger.info("They are now trusted.")
    
    return known_macs

def surveillance_mode(known_macs):
    """Main surveillance loop - the eternal watch. Kya Cool naam rakhta hu me😎"""
    logger.info("Cerberus is watching.")
    logger.info(f"Starting surveillance with {len(known_macs)} known devices. Press Ctrl+C to stop.")
    
    scan_count = 0
    
    try:
        while True:
            scan_count += 1
            logger.info(f"------------------------- Scan {scan_count} -------------------------")
            
            current_devices = scan_network()
            
            if not current_devices:
                logger.warning("No devices found!")
                time.sleep(SCAN_INTERVAL)
                continue
            
            unknown_devices = []
            
            for device in current_devices:
                if device["mac"] not in known_macs:
                    unknown_devices.append(device)
                    ip = device["ip"]
                    mac = device["mac"]
                    logger.warning(f"Unknown: {ip} - {mac}")
            
            # Alert if intruders detected.
            if unknown_devices:
                logger.critical(f"ALERT: {len(unknown_devices)} intruder(s) device detected!")
                for intruder in unknown_devices:
                    logger.critical(f"INTRUDER: {intruder["ip"]} - {intruder["mac"]}")
            else:
                logger.info("All devices are trusted.")
            


            time.sleep(SCAN_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("Surveillance stopped by user.")
        raise
    except Exception as e:
        logger.exception("Error in surveillance.")
        raise

def check_npcap_requirement():
    """
    Check and handle Npcap installation on Windows.
    Returns True if ready to proceed, False if should exit.
    """
    # Only check on Windows
    
    if platform.system() != "Windows":
        logger.info("Non-Windows platform detected - Npcap not required.")
        return True
    
    logger.info("Windows platform detected - checking Npcap availability...")
    
    if not NPCAP_INSTALLER_AVAILABLE:
        logger.warning("Npcap installer module not available.")
        print("\n" + "="*70)
        print("⚠️  WINDOWS USERS: NPCAP REQUIRED")
        print("="*70)
        print("\nCerberus requires Npcap for network scanning on Windows.")
        print("Please download and install Npcap from: https://npcap.com/")
        print("\nAfter installation, restart this program.")
        print("="*70)
        
        choice = input("\nContinue anyway with limited functionality? (y/n): ").lower()
        if choice != 'y':
            logger.info("User chose to exit for Npcap installation.")
            return False
        logger.warning("User chose to continue without Npcap verification.")
        return True
    
    # Use the npcap installer's interactive installation flow
    try:
        npcap_ready = handle_npcap_installation()
        
        if not npcap_ready:
            logger.error("Npcap installation/setup failed or was cancelled.")
            return False
        
        logger.info("Npcap is ready - proceeding with Cerberus.")
        return True
        
    except Exception as e:
        logger.error(f"Error during Npcap check: {e}")
        print(f"\n❌ Error checking Npcap: {e}")
        print("You may need to install Npcap manually from: https://npcap.com/")
        
        choice = input("\nContinue anyway? (y/n): ").lower()
        return choice == 'y'


def main():
    """Main execution flow - the brain of the operation."""
    logger.info("=" * 50)
    logger.info("PROJECT CERBERUS: The Network Sentinel")
    logger.info("=" * 50)
    
    # CRITICAL: Check Npcap on Windows BEFORE attempting any scans.
    if not check_npcap_requirement():
        logger.info("Exiting due to Npcap requirement not met.")
        sys.exit(0)

    # Ye auto detect karega router_detector module ki madad se.
    detector = RouterDetector()
    network_info = detector.get_network_info()

    if not network_info:
        logger.critical("Could not detect network! Check your connection.")
        return
    
    global TARGET_NETWORK

    router_ip = network_info.get('router_ip', 'Unknown')

    # It will try to detect actual subnet mask first then only it will search that range.
    network_cidr = detector.get_network_with_mask()

    if network_cidr:
        TARGET_NETWORK = network_cidr
        logger.info(f"✔️ Network detected with correct subnet: {TARGET_NETWORK}.")
    else:
        # Ye else case hai toh upar ka nahi chala toh network range /24 hai assume karlega, mostl cases me vahi range rehti hai jaise(192.168.1.0/24)
        network_base = '.'.join(router_ip.split('.')[:-1]) + '.0/24'
        TARGET_NETWORK = network_base
        logger.warning(f"⚠️ Using default /24 network assumption: {TARGET_NETWORK}.")

    logger.info(f"Router detected: {router_ip}")
    logger.info(f"Scanning network: {TARGET_NETWORK}")
    logger.info(f"Your IP: {network_info.get('local_ip', 'Unknown')}")
    logger.info(f"Interface: {network_info.get('interface', 'Unknown')}")
    logger.info("-" * 50)

    try:
        known_macs = load_known_devices()
        
        if not known_macs:
            known_macs = learn_network_mode()
            if not known_macs:
                return
        
        # ENTER THE ETERNAL WATCH: Ek ko bhi nahi chodega apun😎😤
        surveillance_mode(known_macs)
        
    except KeyboardInterrupt:
        logger.info("Program stopped.")
    except Exception as e:
        logger.exception("Fatal error.")
    finally:
        logger.info("Cerberus is shutting down. Buh-bieeeee.")


if __name__ == "__main__":
    main()