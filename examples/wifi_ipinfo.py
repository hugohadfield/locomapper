"""
This example creates a GlobalLocalisation class that uses WiFi data to localise the device against 
latitudes and longitudes estimated from the ipinfo library.

To use this example, you will need to install the ipinfo library:
```
pip install ipinfo
```
You will also need to sign up for an access token at https://ipinfo.io/ and replace the access_token with your own.
"""

import hashlib
from typing import Tuple, Optional, List

from locomapper.localisation import GlobalLocalisation
from locomapper.data_models import GeodeticLandmark

import ipinfo
import nmcli


def get_gps_coords() -> Optional[Tuple]:
    """ This uses the ipinfo library to get an estimate of the current GPS coordinates.
    To use this for your own purposes, you will need to sign up for an access token at
    https://ipinfo.io/ and replace the access_token with your own."""
    access_token = '123456789abc'  # Put your own access token here
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails()
    latitude_deg = float(details.latitude)
    longitude_deg = float(details.longitude)
    return latitude_deg, longitude_deg, 0.0


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
