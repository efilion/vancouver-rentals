from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.sqlbase import Base, BaseModel
from app.craigslist_listing.listing import Listing

class TestListingTable: # pylint: disable=attribute-defined-outside-init

    def setup_class(self):
        self.engine = create_engine('sqlite:///test_listings.db', echo=False)
        session = scoped_session(sessionmaker(bind=self.engine, autocommit=True))
        BaseModel.set_session(session)

    def setup_method(self):
        Base.metadata.create_all(self.engine)

    def teardown_method(self):
        Base.metadata.drop_all(self.engine)

    def test_table_exists(self):

        url = \
            'https://vancouver.craigslist.org/van/apa/d/' +\
            'vancouver-garden-view-2-bedroom/7164076116.html'
        today = datetime.now()
        coords = '(49.2397, -123.0407)'
        latitue = 49.2397
        longitude = -123.0407
        garden_view = 'Garden view 2 Bedroom Vancouver Centrally Located September 1'
        rent = 1550
        killarney = 'East Vancouver Killarney'

        Listing.create(
            link=url,
            created=today,
            geotag=coords,
            lat=latitue,
            lon=longitude,
            name=garden_view,
            price=rent,
            location=killarney,
            cl_id=0
        )

        listing = Listing.first()

        assert listing.link == url
        assert listing.created == today
        assert listing.geotag == coords
        assert listing.lat == latitue
        assert listing.lon == longitude
        assert listing.name == garden_view
        assert listing.price == rent
        assert listing.location == killarney
        assert listing.cl_id == 0
