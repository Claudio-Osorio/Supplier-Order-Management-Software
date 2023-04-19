import logging
import os
import numpy as np
import pandas as pd
import datetime
from helpers.database import *
from helpers.configurations import read_attachment_partial_path
import shutil
from pathlib import Path, PureWindowsPath
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

class ImportModel:
    @staticmethod
    def import_excel_file(file_path):
        order_column_list = ['Date', 'Type', 'Company',
                             'Project', 'Lot_Blk', 'Address',
                             'Amount', 'Order', 'Employee',
                             'Supervisor', 'Status', 'Tracking',
                             'Note']
        succeeded = 0
        failed = 0
        try:
            df_orders = pd.read_excel(file_path,
                sheet_name='Sheet1',
                usecols=order_column_list,
                dtype={'Date':str,
                       'Type':str,
                       'Company':str,
                       'Project':str,
                       'Lot_Blk':str,
                       'Address':str,
                       'Amount':'float64',
                       'Order':'int64',
                       'Employee':str,
                       'Supervisor':str,
                       'Status':str,
                       'Tracking':str,
                       'Note':str})

            # Fill NaN values
            df_orders = df_orders.fillna('')
            df_orders = df_orders[order_column_list]
            logging.info(f"Successfully read excel file")
        except:
            logging.warning(f"Excel file could not be read."
                            f" Check that it can be read and expected column format"
                            f" is present.")
            return None

        num_rows = df_orders.shape[0]
        lists = {
            "Column": order_column_list,
            "Type": get_all_types(),
            "Company":get_name_of_all_companies(),
            "Employee":get_name_of_all_employees(),
            "Supervisor":get_name_of_all_supervisors(),
            "Status":get_all_order_status()
        }
        # True if one or more orders fail to be added
        failures = False
        with ThreadPoolExecutor(max_workers=20) as executor:
            for row in range(num_rows):
                result = executor.map(ImportModel.match_and_insert_order(
                    row, file_path, df_orders, lists))
                if result:
                    succeeded += 1
                else:
                    failed += 1
        return (succeeded, failed)

    @staticmethod
    def match_and_insert_order(row, file_path, df_orders, lists):
        field = 'Date'
        try:
            xl_order = df_orders.iloc[row]
            data = dict()
            # DATE
            col_list = lists['Column']
            xl_col = col_list.index(field)
            xl_date = datetime.datetime. \
                strptime(xl_order[xl_col], '%Y-%m-%d %H:%M:%S')
            data["_date"] = xl_date.strftime('%Y-%m-%d')

            xl_order_col_need_id = ['Type', 'Company', 'Project', 'Employee',
                                    'Supervisor', 'Status']
            company_id = None
            list_projects = None

            for field in col_list:
                if field in xl_order_col_need_id:
                    xl_col = col_list.index(field)

                    if field == 'Project':
                        lists[field] = get_all_projects(company_id)

                    result = ImportModel. \
                        get_id_if_exists_in_db(xl_order[xl_col], lists[field])

                    if field == 'Employee':
                        if not result:
                            data["employee_id"] = get_preferred_employee(data["project_id"])
                        else:
                            data["employee_id"] = result
                    elif result is not None:
                        if field == 'Type':
                            data["_type_id"] = result
                        elif field == 'Company':
                            company_id = result
                        elif field == 'Project':
                            data["project_id"] = result
                        elif field == 'Supervisor':
                            data["supervisor_id"] = result
                        elif field == 'Status':
                            data["_status_id"] = result
                    else:
                        raise ValueError

            data["unit_address"] = xl_order[4]
            data["full_address"] = xl_order[5]
            data["amount"] = int(round(xl_order[6], 2) * 100)
            data["order_number"] = int(xl_order[7])
            data["external_tracking"] = xl_order[11]
            data["note"] = xl_order[12]

            # Storing Order Attachment
            xl_attachment_path = Path(file_path)
            xl_attachment_path = xl_attachment_path.parent
            expected_file_name = str(data["order_number"]) + '.pdf'
            order_file_path = PureWindowsPath. \
                joinpath(xl_attachment_path).joinpath(expected_file_name)

            if Path(order_file_path).exists():
                data['attachment_name'] = order_file_path
                store_new_order(data)
            else:
                field = f'Attachment \"{expected_file_name}\" does not exist'
                raise FileNotFoundError

            return True
        except:
            logging.warning(f'Failed to insert order Excel file.'
                            f' Could not match \"{field}\" from row# {row + 1}:\n'
                            f'{str(xl_order)}')
            return False

    # Takes in the value of the cell from the Excel file and the
    # list of values in the database. If it finds it returns the id
    @staticmethod
    def get_id_if_exists_in_db(xl_val, list_elements):
        for id, element in list_elements:
            if (str(xl_val).lower()).strip() == element.lower():
                return int(id)
        else:
            return None