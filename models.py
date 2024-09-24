from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Band(Base):
    __tablename__ = 'bands'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hometown = Column(String, nullable=False)
    
    # Relationship to Concert
    concerts = relationship("Concert", back_populates="band")
    
    def concerts(self):
        return self.concerts
    
    def venues(self):
        return [concert.venue for concert in self.concerts]
    
    def play_in_venue(self, venue, date):
        new_concert = Concert(date=date, venue=venue, band=self)
        return new_concert
    
    def all_introductions(self):
        return [concert.introduction() for concert in self.concerts]

    @classmethod
    def most_performances(cls, session):
        return session.query(cls).join(Concert).group_by(cls.id).order_by(func.count(Concert.id).desc()).first()

class Venue(Base):
    __tablename__ = 'venues'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    city = Column(String, nullable=False)
    
    # Relationship to Concert
    concerts = relationship("Concert", back_populates="venue")
    
    def concerts(self):
        return self.concerts
    
    def bands(self):
        return [concert.bands for concert in self.concerts]
    
    def concert_on(self, date):
        return next((concert for concert in self.concerts if concert.date == date), None)
    
    def most_frequent_band(self):
        band_count = {}
        for concert in self.concerts:
            band = concert.band
            band_count[band] = band_count.get(band, 0) + 1
        return max(band_count, key=band_count.get)

class Concert(Base):
    __tablename__ = 'concerts'
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    band_id = Column(Integer, ForeignKey('bands.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    
    # Relationships
    band = relationship("Band", back_populates="concerts")
    venue = relationship("Venue", back_populates="concerts")
    
    def band(self):
        return self.band
    
    def venue(self):
        return self.venue
    
    def hometown_show(self):
        return self.band.hometown == self.venue.city
    
    def introduction(self):
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"
