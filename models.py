from base import Base
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from exceptions import InvalidFormat, InvalidDate
import datetime


def parse_date(str_date):
    if str_date:
        # str_date format => dd-mm-yyyy
        str_date = str_date.split('-')
        try:
            str_date = [int(x) for x in str_date]
            str_date = datetime.date(*str_date[::-1])
        except ValueError:
            raise InvalidFormat(f'Date not in valid format')

        if str_date > datetime.date.today():
            raise InvalidDate(
                'Date created cannot be greater than today\'s date')
    else:
        str_date = datetime.date.today()
    return str_date


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column('title', String(32), nullable=False)
    short_description = Column(
        'short_description', String(100), nullable=False)
    date_created = Column('date_created', Date, nullable=False)
    long_description = Column(
        'long_description', String(1_000), nullable=False)

    def __repr__(self):
        return (
            (f'<Event({self.id}, "{self.title}", "{self.short_description}", "{self.date_created}", '
             f'"{self.long_description}">')
        )

    def __init__(self, title, short_description, long_description, date_created=None):
        self.title = title
        self.short_description = short_description
        self.long_description = long_description
        self.date_created = parse_date(date_created)

    def __str__(self):
        return f'Event({self.id})'


class ReminderDates(Base):
    __tablename__ = 'reminder_dates'
    id = Column(Integer, primary_key=True)
    date = Column('date', Date)
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship("Event", backref=backref(
        "reminder_dates", cascade="all,delete"))

    def __init__(self, event, date=None):
        self.date = parse_date(date)
        self.event = event

    def __repr__(self):
        return f'<ReminderDates({self.id}, "{self.date}", {self.event_id}, {self.event})>'
