import datetime
import calendar
from motor.motor_asyncio import AsyncIOMotorClient

from bot.config import settings

client = AsyncIOMotorClient(host=settings.mongo_host, port=settings.mongo_port)
db = client['db_name']
collection = db['collection_name']


def add_months(source_date: datetime, months: int) -> datetime:
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    day = min(source_date.day, calendar.monthrange(year, month)[1])
    date = datetime.date(year, month, day)
    return datetime.datetime.combine(date, datetime.datetime.min.time())


async def async_get_pay(data: dict) -> dict | None:
    labels = []
    try:
        dt_from = data['dt_from']
        dt_upto = data['dt_upto']
        group_type = data['group_type']
    except KeyError:
        return

    cur_date = datetime.datetime.fromisoformat(dt_from)
    while cur_date <= datetime.datetime.fromisoformat(dt_upto):
        labels.append(cur_date)

        if group_type == 'month':
            cur_date = add_months(source_date=cur_date, months=1)

        elif group_type == 'day':
            cur_date += datetime.timedelta(days=1)

        elif group_type == 'hour':
            cur_date += datetime.timedelta(hours=1)

        elif group_type == 'week':
            cur_date += datetime.timedelta(weeks=1)
        else:
            return

    dataset = []
    for i, dt in enumerate(labels):
        try:
            obj = collection.find({'$and': [{'dt': {'$gte': dt}}, {'dt': {'$lt': labels[i + 1]}}]})
        except IndexError:
            obj = collection.find({'$and': [{'dt': {'$gte': dt}},
                                            {'dt': {'$lte': datetime.datetime.fromisoformat(data['dt_upto'])}}]})
        value_sum = 0
        async for o in obj:
            value_sum += int(o['value'])
        dataset.append(value_sum)
    labels = [label.isoformat() for label in labels]
    return {"dataset": dataset, "labels": labels}
