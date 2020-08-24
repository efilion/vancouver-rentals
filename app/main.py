import logging
from os import getenv

from craigslist import CraigslistHousing
import googlemaps
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.sqlbase import Base, BaseModel
from app.craigslist_listing.listing import Listing # pylint: disable=unused-import
from app.craigslist_listing.craigslist_postings import CraigslistListings
from app.distance import Distance

def main():

    logging.basicConfig(level=int(getenv('LOGLEVEL')))

    resources = initialize_resources()

    BaseModel.set_session(resources['database_session'])
    Base.metadata.create_all(resources['database_engine'])

    batch_size = 200

    craigslist = CraigslistListings(resources['craigslist_provider'])
    postings = craigslist.read_listings(batch_size)

    dist = Distance(resources['distance_matrix_provider'])
    ubc_coords = (49.2455604, -123.2899276)

    _saved = 0
    for p in postings:
        try:
            Listing.create(**p.to_dict())
            _saved = _saved + 1

            duration_value, duration_text = dist.commute_time(ubc_coords, (p.lat, p.lon))
            p.update(duration_value=duration_value, duration_text=duration_text)
        except SQLAlchemyError as err:
            logging.warning(err)

    logging.info("(%s/%s) postings saved to the database.", _saved, batch_size)

def initialize_resources():
    resources = dict()
    engine = create_engine('sqlite:///listings.db', echo=False)
    session = scoped_session(sessionmaker(bind=engine, autocommit=True))

    resources['database_engine'] = engine
    resources['database_session'] = session

    craigslist_provider = CraigslistHousing(site='vancouver', area='van', category='apa')
    resources['craigslist_provider'] = craigslist_provider

    google_maps = googlemaps.Client(key=getenv("GOOGLE_API_KEY"))
    resources['distance_matrix_provider'] = google_maps

    return resources

if __name__ == "__main__":
    main()
