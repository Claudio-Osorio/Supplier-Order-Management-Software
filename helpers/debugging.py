import logging
import datetime
import os

def init_logging():
    log_path = "\\logs"
    log_dir_full_path = os.getcwd() + log_path
    if not os.path.exists(log_dir_full_path):
        os.makedirs(log_dir_full_path)
    now = datetime.datetime.now()
    launch_date_time_str = now.strftime("%Y-%m-%d %H-%M-%S")
    log_file_full_path = str(log_dir_full_path + f'/{launch_date_time_str}.log')
    logging.basicConfig(filename=log_file_full_path,
                        encoding='utf-8',
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s',
                        filemode='w')
    logging.info('Program executed and logging initialized')