from dateutil.parser import parse as parse_date
from craigslist import CraigslistHousing
from app.craigslist_listing.listing import Listing

def read_listings():
    # return self.postings data formatted as Listing
    postings = \
      CraigslistHousing(site='vancouver', area='van', category='apa') \
        .get_results(sort_by='newest', limit=200, geotagged=True)

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
    ) for p in postings)

def parse_price(price):
    try:
        return float(price.replace("$", ""))
    except ValueError:
        return None
