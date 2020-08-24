from sqlalchemy import Column, Integer, String, DateTime, Float

from app.sqlbase import BaseModel

class Listing(BaseModel):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    created = Column(DateTime)
    geotag = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(String)
    price = Column(Float)
    location = Column(String)
    cl_id = Column(Integer, unique=True)
    duration_value = Column(Integer)
    duration_text = Column(String)
