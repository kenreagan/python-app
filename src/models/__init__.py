from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, DateTime, String, Integer

Base = declarative_base()


class EarthQuakes(Base):
    __tablename__ = "earthquake"
    index = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(150))
    time = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    depth = Column(Float)
    mag = Column(Float)
    magType = Column(Float)
    nst = Column(Float)
    gap = Column(Float)
    dmin = Column(Float)
    rms = Column(Float)
    net = Column(String(20))
    updated = Column(DateTime)
    place = Column(String(250))
    type = Column(String(100))
    horizontalError = Column(Float)
    depthError = Column(Float)
    magError = Column(Float)
    magNst = Column(Float)
    status = Column(String(100))
    locationSource = Column(String(100))
    magSource = Column(String(100))

    def to_json(self):
        return {
                "index": self.index,
                "id": self.id,
                "time": self.time,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "depth": self.depth,
                "mag": self.mag,
                "magType": self.magType,
                "nst": self.nst,
                "gap": self.gap,
                "dmin": self.dmin,
                "rms": self.rms,
                "net": self.net,
                "updated": self.updated,
                "place": self.place,
                "type": self.type,
                "horizontalError": self.horizontalError,
                "depthError": self.depthError,
                "magError": self.magError,
                "magNst": self.magNst,
                "status": self.status,
                "locationSource": self.locationSource,
                "magSource": self.magSource
            }
