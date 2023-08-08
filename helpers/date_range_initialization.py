from helpers.configurations import read_custom_search_date_range, read_search_date_range_mode
import datetime
from datetime import *

def initializing_date():
    mode = read_search_date_range_mode()
    # Up to Date is Jan 1st to Present Day of the Current Year
    if mode == 'uptodate':
        start_date = date.today().replace(month=1, day=1)
        end_date = date.today()
    # Natural Year is Jan 1st to Dec 31st of the Current Year
    elif mode == 'naturalyear':
        start_date = date.today().replace(month=1, day=1)
        end_date = date.today().replace(month=12, day=31)
    # Fiscal Year is Oct 1st to Sept 30th of the next year
    elif mode == 'fiscalyear':
        today_date = date.today()
        if today_date.month <= 9:
            start_year = today_date.year - 1
            start_date = date(start_year, 10, 1)
            end_date = date.today().replace(month=9, day=30)
        else:
            start_date = date(date.today().year, 10, 1)
            end_year = date.today().year + 1
            end_date = date(end_year, 9, 31)
    elif mode == 'custom':
        start_date, end_date = read_custom_search_date_range()
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    return start_date, end_date