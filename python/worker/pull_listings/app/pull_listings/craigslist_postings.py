from dateutil.parser import parse as dateutil_parse, ParserError
from app.common.listing import Listing

def parse_price(price):
    try:
        return float(price.replace('$', '').replace(',',''))
    except ValueError:
        return None

def parse_date(date):
    try:
        return dateutil_parse(date)
    except ParserError:
        return None

def parse_bathrooms(num_bathrooms):
    if num_bathrooms == "shared":
        return 0.5
    else:
        return num_bathrooms

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
            .get_results(sort_by='newest', limit=batch_size, geotagged=True, include_details=True)

        return (Listing(
            cl_id=p.get('id'),
            link=p.get('url'),
            created=parse_date(p.get('datetime')),
            geotag=str(p.get('geotag')),
            lat=p.get('geotag')[0],
            lon=p.get('geotag')[1],
            name=p.get('name'),
            price=parse_price(p.get('price')),
            location=p.get('where'),
            num_bedrooms=p.get('bedrooms'),
            num_bathrooms=parse_bathrooms(p.get('bathrooms'))
        ) for p in postings
                if isValid(p))
