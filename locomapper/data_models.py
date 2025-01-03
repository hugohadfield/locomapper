
from pydantic import BaseModel


class CartesianLandmark(BaseModel):
    """ Data model for Cartesian landmark data """
    identifier: str
    x_m: float
    y_m: float
    z_m: float
    uncertainty_m: float


class GeodeticLandmark(BaseModel):
    """ Data model for geodetic landmark data """
    identifier: str
    latitude_deg: float
    longitude_deg: float
    altitude_m: float
    latitude_uncertainty_deg: float
    longitude_uncertainty_deg: float
    altitude_uncertainty_m: float

