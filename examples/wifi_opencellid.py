"""
This example uses opencellid to estimate location and train the localiser using WiFi data.
Note this doesn't include any command to call out to a library to get the acutal cell tower info
to do the lookup.
"""

import hashlib
from typing import Tuple, Optional, Dict, List

import requests
import nmcli

from locomapper.localisation import GlobalLocalisation
from locomapper.data_models import GeodeticLandmark


def get_cell_tower_data() -> Dict:
    """ Here is where you would call out to a cell tower module to get a list of the 
    cell tower data in the vicinity. For the purposes of this example, we will return a dummy value.
    """
    return {"mcc": 234, #mobileCountryCode
        "mnc": 15, #mobileNetworkCode
        "lac": 24708, #locationAreaCode
        "cell_id": 2561566 #CellId
    }


def get_gps_coords() -> Optional[Tuple]:
    """ This uses the opencellid API to get an estimate of the current GPS coordinates
    based on cell tower data."""
    cell_tower_data = get_cell_tower_data()
    url = "https://opencellid.org/ajax/searchCell.php"
    res = requests.get(url, params=cell_tower_data)
    if not res.ok:
        print('Error: '+res.text)
        return None
    else:
        res_json = res.json()
        return float(res_json['lat']), float(res_json['lon']), 0.0
        
        
def scan_wifi() -> List:
    """Scan for WiFi networks."""
    try:
        nmcli.device.wifi_rescan()
    except Exception as e:
        pass
    wifi_data = nmcli.device.wifi()
    return wifi_data


def get_wifi_data() -> Tuple:
    """ Here is where you would call out to a WiFi module to get a list of the 
    SSID and MAC addresses of the WiFi networks in the vicinity."""
    wifi_data = scan_wifi()
    return [(wifi.ssid, wifi.bssid) for wifi in wifi_data]


def hash_wifi(ssid: str, mac: str) -> str:
    """Hashes the SSID and MAC address of a WiFi network."""
    return hashlib.md5(f"{ssid}{mac}".encode()).hexdigest()


class WifiGlobalLocalisation(GlobalLocalisation):
    def add_wifi_data(self, ssid: str, mac: str, latitude_deg: float, longitude_deg: float, altitude_m: float):
        """Add WiFi data to the store."""
        identifier = hash_wifi(ssid, mac)
        self.add_data(identifier, latitude_deg, longitude_deg, altitude_m)

    def get_wifi_data(self, ssid: str, mac: str) -> Tuple:
        """Get WiFi data from the store."""
        identifier = hash_wifi(ssid, mac)
        return self.get_data(identifier)

    def localise_wifi(self, ssid: str, mac: str) -> Optional[GeodeticLandmark]:
        """Localise based on a single WiFi network."""
        identifier = hash_wifi(ssid, mac)
        return self.localise(identifier)

    def localise_multiple(self, wifi_tuple: Tuple[Tuple[str, str]]) -> Tuple[float, float, float]:
        """Localise based on multiple WiFi networks."""
        latitude_deg = 0.0
        longitude_deg = 0.0
        altitude_m = 0.0
        for ssid, mac in wifi_tuple:
            landmark = self.localise_wifi(ssid, mac)
            if landmark is not None:
                latitude_deg += landmark.latitude_deg
                longitude_deg += landmark.longitude_deg
                altitude_m += landmark.altitude_m
        latitude_deg /= len(wifi_tuple)
        longitude_deg /= len(wifi_tuple)
        altitude_m /= len(wifi_tuple)
        return latitude_deg, longitude_deg, altitude_m


if __name__ == '__main__':
    import time

    # Create a localiser
    localiser = WifiGlobalLocalisation()

    # Train the localiser for N_train_seconds seconds
    N_train_seconds = 100
    for i in range(N_train_seconds):
        latitude_deg, longitude_deg, altitude_m = get_gps_coords()
        wifi_data = get_wifi_data()
        for ssid, mac in wifi_data:
            localiser.add_wifi_data(ssid, mac, latitude_deg, longitude_deg, altitude_m)
        print(f"{i}/{N_train_seconds}: Added {len(wifi_data)} WiFi networks at {latitude_deg}, {longitude_deg}, {altitude_m}, total landmarks: {len(localiser)}")
        time.sleep(1)

    # Save the store
    localiser.save("wifi_landmarks.json")

    # Load the store
    localiser.load("wifi_landmarks.json")

    # Localise based on the WiFi data for N_train_seconds seconds
    for i in range(N_train_seconds):
        wifi_data = get_wifi_data()
        latitude_deg, longitude_deg, altitude_m = localiser.localise_multiple(wifi_data)
        print(f"{i}/{N_train_seconds}: Localised at {latitude_deg}, {longitude_deg}, {altitude_m}")
        time.sleep(1)