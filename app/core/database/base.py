from sqlalchemy.ext.automap import automap_base
from sqlalchemy_mixins.activerecord import ActiveRecordMixin
from sqlalchemy_mixins.repr import ReprMixin
from sqlalchemy_mixins.smartquery import SmartQueryMixin

Base = automap_base()


class BaseModel(Base, SmartQueryMixin, ActiveRecordMixin, ReprMixin):
    __abstract__ = True
    __repr__ = ReprMixin.__repr__
    pass
