from helpers.database import store_new_supervisor
class NewSupervisorModel:
    @staticmethod
    def save_data(data):
        store_new_supervisor(data)