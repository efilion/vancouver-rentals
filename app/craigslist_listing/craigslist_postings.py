from dateutil.parser import parse as parse_date
from app.craigslist_listing.listing import Listing

def parse_price(price):
    try:
        return float(price.replace('$', '').replace(',',''))
    except ValueError:
        return None

def isValid(posting):
    try:
        hasLat = float(posting.get('geotag')[0])
        hasLon = float(posting.get('geotag')[1])
        return hasLat and hasLon
    except TypeError:
        return False

class CraigslistListings:

    def __init__(self, listing_provider):
        self.listing_provider = listing_provider

    def read_listings(self, batch_size):
        # return self.postings data formatted as Listing
        postings = self.listing_provider \
            .get_results(sort_by='newest', limit=batch_size, geotagged=True)

        return (Listing(
            cl_id=p.get('id'),
            link=p.get('url'),
            created=parse_date(p.get('datetime')),
            geotag=str(p.get('geotag')),
            lat=p.get('geotag')[0],
            lon=p.get('geotag')[1],
            name=p.get('name'),
            price=parse_price(p.get('price')),
            location=p.get('where')
        ) for p in postings
                if isValid(p))
