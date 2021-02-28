from mylifelogger.models import ReminderDates, Event
from mylifelogger import Session, engine, Base
import datetime
Base.metadata.create_all(engine)

session = Session()

anniversary = Event('Parents anniversary',
                    "Parents anniversary", "", datetime.date.today())
birthday = Event('Mother\'s birthday', "", "", datetime.date.today())

rda = ReminderDates(anniversary, datetime.date.today(),
                    date=datetime.date.today())
rda2 = ReminderDates(anniversary, datetime.date.today(),
                     date=datetime.date.today())

# session.add(anniversary)
# session.add(birthday)
session.add(rda)
session.add(rda2)
# session.commit()
# session.close()

rem = session.query(ReminderDates)
ev = session.query(Event)

print(rem.all())
print(ev.all())

u = rem.all()[0]
session.delete(u)
# session.commit()

print(ev.all())
