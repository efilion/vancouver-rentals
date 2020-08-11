import logging
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.sqlbase import Base, BaseModel
from app.craigslist_listing.listing import Listing # pylint: disable=unused-import
from app.craigslist_listing.craigslist_postings import read_listings

def main():

    logging.basicConfig(level=int(getenv('LOGLEVEL')))

    engine = create_engine('sqlite:///listings.db', echo=False)
    session = scoped_session(sessionmaker(bind=engine, autocommit=True))
    BaseModel.set_session(session)

    Base.metadata.create_all(engine)

    batch_size = 200
    postings = read_listings(batch_size)

    _saved = 0
    for p in postings:
        try:
            Listing.create(**p.to_dict())
            _saved = _saved + 1
        except SQLAlchemyError as err:
            logging.warning(err)

    logging.info("(%s/%s) postings saved to the database.", _saved, batch_size)

if __name__ == "__main__":
    main()
