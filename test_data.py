from models import ReminderDates, Event
from base import Session, engine, Base

Base.metadata.create_all(engine)

session = Session()

anniversary = Event('Parents anniversary', "Parents anniversary", "")
birthday = Event('Mother\'s birthday', "", "")

rda = ReminderDates(anniversary)
rda2 = ReminderDates(anniversary, '12-03-2020')

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
