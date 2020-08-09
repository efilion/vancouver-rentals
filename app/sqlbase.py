from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_mixins import ActiveRecordMixin, SmartQueryMixin, ReprMixin, SerializeMixin

Base = declarative_base()

class BaseModel(Base, ActiveRecordMixin, SmartQueryMixin, ReprMixin, SerializeMixin):
    __abstract__ = True
    __repr__ = ReprMixin.__repr__
