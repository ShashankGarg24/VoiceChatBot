import datetime
import pytz

date = "2023-04-11"
dtArray = str(date).split("-")
dt = datetime.date(int(dtArray[0]), int(dtArray[1]), int(dtArray[2]))
date = datetime.datetime.combine(dt, datetime.datetime.min.time())
print(date)
end_date = datetime.datetime.combine(dt, datetime.datetime.max.time())
print(end_date)
utc = pytz.UTC
print(utc)
date = date.astimezone(utc)
print(date)
end_date = end_date.astimezone(utc)

print(end_date)