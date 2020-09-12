import logging
from os import getenv

from mongoengine import connect, OperationError
from craigslist import CraigslistHousing
import googlemaps

from app.craigslist_listing.listing import Listing # pylint: disable=unused-import
from app.craigslist_listing.craigslist_postings import CraigslistListings
from app.distance import Distance

def main():

    logging.basicConfig(level=int(getenv('LOGLEVEL')))

    resources = initialize_resources()

    batch_size = 3000

    craigslist = CraigslistListings(resources['craigslist_provider'])
    postings = craigslist.read_listings(batch_size)

    dist = Distance(resources['distance_matrix_provider'])
    ubc_coords = (49.2455604, -123.2899276)

    for p in postings:
        try:
            Listing.objects(cl_id=p.cl_id).upsert_one(**p.to_mongo())

            duration_value, duration_text = dist.commute_time(ubc_coords, (p.lat, p.lon))
            p.duration_value=duration_value
            p.duration_text=duration_text
            p.save()
        except OperationError as err:
            logging.warning(err)
        except ValueError as err:
            logging.warning("%s in %s", err, p.to_json())

def initialize_resources():
    resources = dict()

    database_connection = connect('vancouver-rentals', **{
        'host': 'localhost',
        'port': 27017
    })
    resources['database_connection'] = database_connection

    craigslist_provider = CraigslistHousing(site='vancouver', area='van', category='apa')
    resources['craigslist_provider'] = craigslist_provider

    google_maps = googlemaps.Client(key=getenv("GOOGLE_API_KEY"))
    resources['distance_matrix_provider'] = google_maps

    return resources

if __name__ == "__main__":
    main()
