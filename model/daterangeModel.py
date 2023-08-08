import datetime
from datetime import *
from helpers.configurations import store_custom_search_date_range, store_search_date_range_mode

class DateRangeModel:
    @staticmethod
    def store_setting(data):
        store_search_date_range_mode(data['option'])
        if data['option'] == 'custom':
            start_date = data['start_date']
            end_date = data['end_date']
            store_custom_search_date_range(start_date, end_date)