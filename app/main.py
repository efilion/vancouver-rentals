from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.sqlbase import Base, BaseModel
from app.craigslist_listing.listing import Listing # pylint: disable=unused-import
from app.craigslist_listing.craigslist_postings import read_listings

engine = create_engine('sqlite:///listings.db', echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit=True))
BaseModel.set_session(session)

Base.metadata.create_all(engine)

postings = read_listings()

for p in postings:
    try:
        Listing.create(**p.to_dict())
    except SQLAlchemyError as err:
        print(err)
