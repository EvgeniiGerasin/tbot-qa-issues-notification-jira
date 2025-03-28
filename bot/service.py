from data import SqlManager


class DataForUser:

    def __init__(self):
        self.sql = SqlManager()

    def get_all_issues(self) -> str:
        pass

    def get_all_issues_for_period(self, period) -> str:
        pass

    def get_user_id(self) -> set:
        try:
            data = set(self.sql.get_all_chat_ids())
        finally:
            self.sql.close()
        return data

    def get_data_new_issues(self) -> str:
        pass


class DataForJira:
