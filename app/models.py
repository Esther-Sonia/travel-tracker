from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow,nullable=False )

    trips = relationship("Trip", back_populates="user")

class Destination(Base):
    __tablename__ = 'destinations'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    continent = Column(String)

    trips = relationship("Trip", back_populates="destination")

class Trip(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    destination_id = Column(Integer, ForeignKey('destinations.id'))
    start_date = Column(Date)
    end_date = Column(Date)
    notes = Column(String)

    user = relationship("User", back_populates="trips")
    destination = relationship("Destination", back_populates="trips")

