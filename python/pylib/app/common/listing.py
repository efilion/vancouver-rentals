from mongoengine import Document, StringField, DateTimeField, FloatField, IntField

class Listing(Document):
    link = StringField(unique=True)
    created = DateTimeField()
    geotag = StringField()
    lat = FloatField()
    lon = FloatField()
    name = StringField()
    price = FloatField()
    location = StringField()
    num_bedrooms = FloatField()
    num_bathrooms = FloatField()
    cl_id = IntField(unique=True)
    duration_value = IntField()
    duration_text = StringField()
