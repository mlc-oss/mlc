import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.types import Enum
from sqlalchemy.orm import declarative_mixin, declared_attr
from pytz import timezone
import re

from app.common.status import Status


@declarative_mixin
class BaseMixin:
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake(cls.__name__)

    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)


@declarative_mixin
class TimeMixin(BaseMixin):
    created_at = Column(DateTime, default=datetime.datetime.now(timezone('Asia/Seoul')))
    last_modified_at = Column(DateTime, default=datetime.datetime.now(timezone('Asia/Seoul')))
    status = Column(Enum(Status), default=Status.RUNNING)


# code from https://gist.github.com/jaytaylor/3660565

_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(s):
    """
    Is it ironic that this function is written in camel case, yet it
    converts to snake case? hmm..
    """
    subbed = _underscorer1.sub(r'\1_\2', s)
    return _underscorer2.sub(r'\1_\2', subbed).lower()
