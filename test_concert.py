# test_concert.py

# Import necessary modules and classes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Band, Venue, Concert, Base  # Ensure all necessary imports

# Create the database engine
engine = create_engine('sqlite:///concerts.db')

# Create all tables in the database
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create instances of Band, Venue, and Concert for testing
bands = Band(name="The Rolling Stones", hometown="London")
venue = Venue(title="Wembley Stadium", city="London")
concert = bands.play_in_venue(venue, "2024-09-24")

# Add instances to the session
session.add(bands)
session.add(venue)
session.add(concert)

# Commit the session to save changes to the database
session.commit()

# Optional: Test your methods
print(concert.introduction())  # E.g., "Hello London!!!!! We are The Rolling Stones and we're from London"
print(venue.bands())  # This should show the bands performing at this venue
print(Band.most_performances(session))  # Assuming this method is implemented correctly

# Close the session after operations are complete
session.close()
