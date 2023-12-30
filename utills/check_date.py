from datetime import datetime as dt
from datetime import timedelta

format_date = ['%d.%m', '%d/%m', '%d-%m', r'%d\%m']


async def check_format_date(msg_date):
    date = None
    for i in format_date:
        try:
            date = (dt.strptime(msg_date, i)).strftime('%d-%m')
        except BaseException:
            pass
    return date


async def subtract_date(date_birthday, quantity_day):
    return (
        dt.strptime(date_birthday, '%d-%m') - timedelta(
            days=quantity_day)).strftime('%d-%m')
