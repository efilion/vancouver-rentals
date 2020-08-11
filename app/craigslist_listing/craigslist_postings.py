from dateutil.parser import parse as parse_date
from craigslist import CraigslistHousing
from app.craigslist_listing.listing import Listing

def read_listings(batch_size):
    # return self.postings data formatted as Listing
    postings = \
      CraigslistHousing(site='vancouver', area='van', category='apa') \
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

def parse_price(price):
    try:
        return float(price.replace("$", ""))
    except ValueError:
        return None

def isValid(posting):
    try:
        hasLat = float(posting.get('geotag')[0])
        hasLon = float(posting.get('geotag')[1])
        return hasLat and hasLon
    except TypeError:
        return False
