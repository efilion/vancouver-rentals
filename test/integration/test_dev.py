import time
from itertools import cycle

from unittest import TestCase
from unittest.mock import patch
from hypothesis import given
from hypothesis.strategies import composite, lists, tuples, booleans, \
        integers, floats, text, datetimes
from hypothesis.provisional import urls

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.main import main

def initialize_resources(postings, distance_matrices):

    resources = dict()

    engine = create_engine('sqlite:///:memory:', echo=False)
    session = scoped_session(sessionmaker(bind=engine, autocommit=True))

    resources['database_engine'] = engine
    resources['database_session'] = session

    resources['craigslist_provider'] = craigslist_mock(postings)
    resources['distance_matrix_provider'] = gmaps_mock(distance_matrices)

    return resources

def craigslist_mock(postings):
    mock = type("CraigslistHousingProvider", (object,), {
        "postings": postings,
        "get_results":
            lambda self, sort_by, limit, geotagged: (x for x in self.postings[:limit])
    })

    return mock()

@composite
def craigslist_responses(draw):
    return {
        'id': '{0}'.format(draw(integers(min_value=0))),
        'repost_of': None,
        'name': draw(text()),
        'url': draw(urls()),
        'datetime': draw(datetimes()).strftime('%Y-%m-%d %H:%M'),
        'last_updated': draw(datetimes()).strftime('%Y-%m-%d %H:%M'),
        'price': '${0}'.format(draw(integers(min_value=0))),
        'where': draw(text()),
        'has_image': draw(booleans()),
        'geotag': draw(tuples(floats(), floats())),
        'deleted': draw(booleans())
    }

def gmaps_mock(distance_matrices):
    mock = type("DistanceMatrixProviderMock", (object,), {
        "distance_matrices": cycle(distance_matrices),
        "distance_matrix":
            lambda self, origin, destination, mode, transit_routing_preference:
                next(self.distance_matrices)
    })

    return mock()

@composite
def gmaps_responses(draw):
    distance = draw(integers(min_value=0, max_value=(2**31)))
    duration = draw(integers(min_value=0, max_value=(2**31)))
    return {
        'rows': [
            {
                'elements': [
                    {
                        'distance': {'text': '{:,} km'.format(distance // 1000), 'value': distance},
                        'duration': {
                            'text': time.strftime("%H hours %M minutes", time.gmtime(duration)),
                            'value': duration
                        },
                        'status': 'OK'
                    }
                ]
            }
        ]
    }

class TestDevIntegration(TestCase):

    @patch('app.main.initialize_resources')
    @given(
        postings=lists(craigslist_responses()), # pylint: disable=no-value-for-parameter
        distance_matrices=lists(gmaps_responses(), min_size=1)) # pylint: disable=no-value-for-parameter
    def test_main(self, mock, postings, distance_matrices):
        mock.return_value = initialize_resources(postings, distance_matrices)
        main()
