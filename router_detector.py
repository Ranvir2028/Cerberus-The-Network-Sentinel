"""
Router Detector Module

This module is for detecting the router IP addresses and network information.
This is a custom module which serves the main Cerberus module.

Usage:
    from router_detector import RouterDetector
    
    detector = RouterDetector()
"""

import netifaces

class RouterDetector:
    """
    I made this class for detecting router and network information. So,
    This class will has methods that will retrieve the router's IP address(gateway) and network information including local IP and interface.
    """
    
    @staticmethod
    def get_router_ip():
        """
        It will get the router's IP address(gateway).
        
        Returns:
            str: The router's IPv4 address.
            
        Example:
            detector = RouterDetector()
            router_ip = detector.get_router_ip()
            print(router_ip)
            '192.168.1.1'
        """
        try:
            gateways = netifaces.gateways()
            # ye just samjhne ke liye hai age ke code ke liye
            # Example gateways structure:
            # {
            #     'default': {
            #         2: ('192.168.1.1', 'eth0', True),   # AF_INET (IPv4)
            #         10: ('fe80::1', 'eth0', True)       # AF_INET6 (IPv6)
            #     }
            # }
            
            if 'default' in gateways and netifaces.AF_INET in gateways['default']:
                return gateways['default'][netifaces.AF_INET][0]
                
        except Exception:
            pass
            
        return None


    @staticmethod
    def get_network_info():
        """
        It will fetch the network information for monitoring.
        
        Returns:
            dict: It will return a dictionary containing network information with key value pairs:
                  - router_ip: The gateway IP address
                  - local_ip: The local machine's IP address
                  - interface: The network interface name
        """
        try:
            gateways = netifaces.gateways()
            
            if 'default' not in gateways:
                return None
            
            # Get default IPv4 gateway
            if netifaces.AF_INET in gateways['default']:
                gateway_ip, interface = gateways['default'][netifaces.AF_INET][:2]
                
                # Get local IP on that interface
                try:
                    addrs = netifaces.ifaddresses(interface)
                    
                    if netifaces.AF_INET in addrs:
                        local_ip = addrs[netifaces.AF_INET][0].get('addr')
                        
                        return {
                            'router_ip': gateway_ip,
                            'local_ip': local_ip,
                            'interface': interface
                        }
                        
                except Exception:
                    return {
                        'router_ip': gateway_ip,
                        'interface': interface
                    }
            
            return None
            
        except Exception as e:
            print(f"Network detection error: {e}")
            return None
        

    @staticmethod
    def get_network_with_mask():
        """
        It will fetch network address with correct subnet mask detection.
        Returns:
            Network address in CIDR notation (eg, 192.168.1.0/24)
        """
        try:
            gateways = netifaces.gateways()

            if 'default' not in gateways or netifaces.AF_INET not in gateways['default']:
                return None
            
            gateway_ip, interface = gateways['default'][netifaces.AF_INET][:2]

            # It fetches network information for the interface
            addrs = netifaces.ifaddresses(interface)

            if netifaces.AF_INET in addrs:
                addr_info = addrs[netifaces.AF_INET][0]
                ip_address = addr_info['addr']
                netmask = addr_info['netmask']

                ip_parts = [int(part) for part in ip_address.split('.')]
                mask_parts = [int(part) for part in netmask.split('.')]
            
                network_parts = [ip_parts[i] & mask_parts[i] for i in range(4)]
                network_addr = '.'.join(str(part) for part in network_parts)
                
                cidr = sum(bin(int(x)).count('1') for x in netmask.split('.'))
                
                return f"{network_addr}/{cidr}"
                
        except Exception as e:
            print(f"Network detection error: {e}")
        
        return None

