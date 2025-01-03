# Landmark-Based Localisation Library

This repository provides a Python library for managing and localising geodetic and Cartesian landmarks using Pydantic-based data models. It includes functionality for adding, storing, retrieving, and processing landmark data. Additionally, a WiFi-based global localisation example is implemented to demonstrate practical usage in real-world scenarios.

---

## Features

- **Landmark Management**: Store, retrieve, and process geodetic and Cartesian landmarks with `LandmarkStore`.
- **Global Localisation**: Compute approximate locations using geodetic or Cartesian landmark data.
- **WiFi-Based Localisation**: Leverage WiFi SSIDs and MAC addresses for localisation by associating them with known geodetic landmarks.
- **Data Persistence**: Save and load landmark data to/from JSON files.

---

## Project Structure

```
src/
├── locomapper/
│   ├── landmark_store.py       # Core LandmarkStore class
│   ├── localisation.py         # Localisation classes for geodetic and Cartesian landmarks
│   ├── data_models.py          # Pydantic data models for landmarks
├── examples/
│   ├── wifi_gps.py             # Example for WiFi-based localisation with GPS coordinates
```

---

## Installation

### Prerequisites
- Python 3.8 or later
- Install the required Python packages:
  ```bash
  pip install -r requirements.txt
  ```

### Dependencies
#### Required
- [Pydantic](https://docs.pydantic.dev/) for data validation and management.

#### Optional for examples
- [nmcli](https://pypi.org/project/python-nmcli/) for interacting with WiFi networks (optional, for WiFi-based localisation).
---

## Usage

### 1. Manage Geodetic and Cartesian Landmarks
```python
from locomapper.localisation import GlobalLocalisation, CartesianLocalisation

# Geodetic example
geo_localiser = GlobalLocalisation()
geo_localiser.add_data(
    identifier="landmark1",
    latitude_deg=47.6097,
    longitude_deg=-122.3331,
    altitude_m=30.0
)
print(geo_localiser.get_data("landmark1"))

# Cartesian example
cart_localiser = CartesianLocalisation()
cart_localiser.add_data(
    identifier="landmarkA",
    x_m=10.0,
    y_m=20.0,
    z_m=5.0
)
print(cart_localiser.get_data("landmarkA"))
```

### 2. WiFi-Based Localisation
```python
from locomapper.wifi_localisation import WifiGlobalLocalisation

wifi_localiser = WifiGlobalLocalisation()
wifi_localiser.add_wifi_data(
    ssid="HomeNetwork",
    mac="00:11:22:33:44:55",
    latitude_deg=47.6097,
    longitude_deg=-122.3331,
    altitude_m=30.0
)
location = wifi_localiser.localise_wifi("HomeNetwork", "00:11:22:33:44:55")
print(location)
```

---

## Example

The `wifi_gps.py` script demonstrates a simple workflow for WiFi-based global localisation. To run the script:
```bash
python wifi_gps.py
```

---

## Saving and Loading Data
```python
# Save landmarks to a file
geo_localiser.save("landmarks.json")

# Load landmarks from a file
geo_localiser.load("landmarks.json")
```

---

## Contributing

Feel free to submit issues and feature requests. Pull requests are welcome!

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.