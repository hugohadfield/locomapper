
from typing import Tuple, Optional

from locomapper.landmark_store import LandmarkStore
from locomapper.data_models import GeodeticLandmark, CartesianLandmark


class GlobalLocalisation:
    """Class to store and localise (at a global scale) based on data.
    """
    def __init__(self):
        """Initialise the GlobalLocalisation class."""
        self._store = LandmarkStore(GeodeticLandmark)

    def add_data(self, 
        identifier: str, 
        latitude_deg: float, 
        longitude_deg: float, 
        altitude_m: float,
        latitude_uncertainty_deg: float = 1e-6,
        longitude_uncertainty_deg: float = 1e-6,
        altitude_uncertainty_m: float = 10.0
    ):
        """Add data to the store."""
        landmark = GeodeticLandmark(
            identifier=identifier, 
            latitude_deg=latitude_deg, 
            longitude_deg=longitude_deg, 
            altitude_m=altitude_m,
            latitude_uncertainty_deg=latitude_uncertainty_deg,
            longitude_uncertainty_deg=longitude_uncertainty_deg,
            altitude_uncertainty_m=altitude_uncertainty_m
        )
        self._store.put(landmark)

    def get_data(self, identifier: str) -> Tuple[GeodeticLandmark]:
        """Get data from the store."""
        return self._store.get(identifier)
        
    def __len__(self) -> int:
        """Return the number of elements in the store."""
        return len(self._store)

    def localise(self, identifier: str) -> Optional[GeodeticLandmark]:
        """Localise based on data."""
        landmark_tuple = self.get_data(identifier)
        if len(landmark_tuple) == 0:
            return None
        # Average the data, this is probably not a great way to do this, but it works
        latitude_deg = 0.0
        longitude_deg = 0.0
        altitude_m = 0.0
        for landmark in landmark_tuple:
            latitude_deg += landmark.latitude_deg
            longitude_deg += landmark.longitude_deg
            altitude_m += landmark.altitude_m
        latitude_deg /= len(landmark_tuple)
        longitude_deg /= len(landmark_tuple)
        altitude_m /= len(landmark_tuple)
        return GeodeticLandmark(
            identifier=identifier,
            latitude_deg=latitude_deg,
            longitude_deg=longitude_deg,
            altitude_m=altitude_m,
            latitude_uncertainty_deg=1e-6,
            longitude_uncertainty_deg=1e-6,
            altitude_uncertainty_m=10.0
        )

    def save(self, filename: str):
        """Save the store to a file."""
        self._store.save(filename)

    def load(self, filename: str):
        """Load the store from a file."""
        self._store.load(filename)


class CartesianLocalisation:
    """Class to store and localise (in a cartesian frame) based on data.
    """
    def __init__(self):
        """Initialise the CartesianLocalisation class."""
        self._store = LandmarkStore(CartesianLandmark)

    def add_data(self, 
        identifier: str, 
        x_m: float, 
        y_m: float, 
        z_m: float,
        uncertainty_m: float = 0.1
    ):
        """Add data to the store."""
        landmark = CartesianLandmark(
            identifier=identifier, 
            x_m=x_m, 
            y_m=y_m, 
            z_m=z_m,
            uncertainty_m=uncertainty_m
        )
        self._store.put(landmark)

    def get_data(self, identifier: str) -> Tuple[CartesianLandmark]:
        """Get data from the store."""
        return self._store.get(identifier)
        
    def __len__(self) -> int:
        """Return the number of elements in the store."""
        return len(self._store)

    def localise(self, identifier: str) -> Optional[CartesianLandmark]:
        """Localise based on data."""
        landmark_tuple = self.get_data(identifier)
        if len(landmark_tuple) == 0:
            return None
        # Average the data, this is probably not a great way to do this, but it works
        x_m = 0.0
        y_m = 0.0
        z_m = 0.0
        for landmark in landmark_tuple:
            x_m += landmark.x_m
            y_m += landmark.y_m
            z_m += landmark.z_m
        x_m /= len(landmark_tuple)
        y_m /= len(landmark_tuple)
        z_m /= len(landmark_tuple)
        return CartesianLandmark(
            identifier=identifier,
            x_m=x_m,
            y_m=y_m,
            z_m=z_m,
            uncertainty_m=0.1
        )

    def save(self, filename: str):
        """Save the store to a file."""
        self._store.save(filename)

    def load(self, filename: str):
        """Load the store from a file."""
        self._store.load(filename)