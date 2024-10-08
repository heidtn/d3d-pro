from wpasupplicant import WpaSupplicant
from utils.dbuswpasupplicant import PropertyError
import time
from hostapd import HostAP


class WifiManager:
    # TODO(heidt) should do system query to get interfaces
    def __init__(self, 
                 interface="wlp7s0",
                 hostapd_config="/etc/hostapd/hostapd.conf",
                 wpas_config="/etc/wpa_supplicant/wpa_supplicant.conf",
                 p2p_config="/etc/wpa_supplicant/p2p_supplicant.conf",
                 hostname_config='/etc/hostname'):
        self.interface = interface
        self.hotspot = HostAP(interface, hostapd_config, hostname_config)
        self.wpasupplicant = WpaSupplicant(interface, wpas_config, p2p_config)
        
    def get_current_network_ssid(self):
        try:
            return self.wpasupplicant.get_current_network_ssid()
        except PropertyError:
            return None
        
    def is_connected(self):
        return self.get_current_network_ssid()

    def wait_connected(self, seconds):
        for i in range(seconds):
            if self.is_connected():
                return True
            time.sleep(1)
        return False

    def scan_all_SSIDs(self):
        self.wpasupplicant.scan()
        return self.wpasupplicant.get_scan_results()
    
    def start_host_mode(self, SSID_name="d3d-pro-printer"):
        if not self.hotspot.started():
            self.wpasupplicant.stop()
            self.hotspot.set_hostap_name(SSID_name)
            self.hotspot.start()
        return True
    
    def stop_host_mode(self):
        if self.hotspot.started():
            self.hotspot.stop()
            self.wpasupplicant.start()
        return True

def main():
    # check to see if wifi is connected
    # wait for 30 seconds or some amount of time
    # if wifi still isn't connected, search for all nearby SSIDs
    # enter AP mode
    # start server to select SSID and enter password
    # once the user hits connect, enter client mode and connect to wifi
    pass

    manager = WifiManager()
    print("Manager started")
    if manager.is_connected():
        ssid = manager.get_current_network_ssid()
        print(f"Wifi already connected to {ssid}")
        return True
    else:
        print("waiting for wifi connection...")
        succuss = manager.wait_connected(3)
        if succuss:
            return True
        else:
            print("Wifi connection failed")
    
    nearby_ssids = manager.scan_all_SSIDs()
    print(f"Found nearby SSIDs")
    for ssid in nearby_ssids:
        print(f"{ssid['ssid']}")
    
    print("entering hostmode")
    manager.start_host_mode() 

    #manager.stop_host_mode()

if __name__ == "__main__":
    main()