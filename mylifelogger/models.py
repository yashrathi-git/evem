from mylifelogger import Base
from sqlalchemy import Column, String, Date, Integer, ForeignKey, Boolean, PickleType
from sqlalchemy.orm import relationship, backref


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    title = Column('title', String(32), nullable=False)
    short_description = Column(
        'short_description', String(100), nullable=False)
    date_created = Column('date_created', Date, nullable=False)
    long_description = Column(
        'long_description', String(1_000), nullable=False)
    html = Column('html', String(10_000), default='')

    def __repr__(self):
        return (
            (f'<Event({self.id}, "{self.title}", "{self.short_description}", "{self.date_created}", '
             f'"{self.long_description}">')
        )

    def __init__(self, title, short_description, long_description, date_created, html=''):
        self.title = title
        self.short_description = short_description
        self.long_description = long_description
        self.date_created = date_created
        self.html = html

    def __str__(self):
        return f'Event({self.id})'


class ReminderDates(Base):
    __tablename__ = 'reminder_dates'
    id = Column(Integer, primary_key=True)
    # Relative delta
    year_delta = Column('year_delta', Integer, nullable=False)
    month_delta = Column('month_delta', Integer, nullable=False)
    day_delta = Column('day_delta', Integer, nullable=False)
    # Reminder Date
    date = Column('date', Date, nullable=False)
    # How many times to repeat
    repeat = Column('repeat', Integer, default=1, nullable=False)
    repeat_forever = Column('repeat_forever', Boolean, default=False)
    # Which event it's associated with
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship("Event", backref=backref(
        "reminder_dates", cascade="all,delete"))

    def __init__(self, event, day_delta, month_delta, year_delta, repeat=1,
                 repeat_forever=False, date=None):
        self.date = date
        self.repeat = repeat
        self.repeat_forever = repeat_forever
        self.event = event
        self.day_delta = day_delta
        self.month_delta = month_delta
        self.year_delta = year_delta

    def __repr__(self):
        repres = ('<ReminderDates('
                  f'event = {self.event}, '
                  f'day_delta = {self.day_delta}, '
                  f'month_delta = {self.month_delta}, '
                  f'year_delta = {self.year_delta}, '
                  f'repeat = {self.repeat}, '
                  f'repeat_forever = {self.repeat_forever}, '
                  f'date = {self.date})>')
        return repres
