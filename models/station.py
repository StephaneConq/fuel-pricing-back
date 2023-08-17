from sqlalchemy import Column, Integer, String, JSON, Float

from utils.db import DBUtil

db_utils = DBUtil()


class Station(db_utils.Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, nullable=False)
    lat = Column(Float)
    lng = Column(Float)
    adresse = Column(String)
    region = Column(String)
    departement = Column(String)
    ville = Column(String)
    code_departement = Column(String)
    prix = Column(JSON)
    horaires = Column(JSON)

    def as_dict(self):
        return {
            "id": self.id,
            "lat": self.lat,
            "lng": self.lng,
            "adresse": self.adresse,
            "region": self.region,
            "departement": self.departement,
            "ville": self.ville,
            "code_departement": self.code_departement,
            "prix": self.prix,
            "horaires": self.horaires,
        }
