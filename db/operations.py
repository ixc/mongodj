from django.db.backends import BaseDatabaseOperations

class DatabaseOperations(BaseDatabaseOperations):
    compiler_module = 'mongodj.db.compiler'

    def quote_name(self, name):
        return name

    def value_to_db_date(self, value):
        # value is a date here, no need to check it
        return value

    def value_to_db_datetime(self, value):
        # value is a datetime here, no need to check it
        return value

    def value_to_db_time(self, value):
        # value is a time here, no need to check it
        return value

    def prep_for_like_query(self, value):
        return value

    def check_aggregate_support(self, aggregate):
        raise NotImplementedError("MongoDB backend does not support aggregation")