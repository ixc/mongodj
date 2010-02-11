import pymongo as Database

from django.db.backends import BaseDatabaseFeatures, \
                               BaseDatabaseWrapper, \
                               BaseDatabaseClient, \
                               BaseDatabaseValidation, \
                               BaseDatabaseIntrospection

from .creation import DatabaseCreation
from .operations import DatabaseOperations

class DatabaseFeatures(BaseDatabaseFeatures):
    distinguishes_insert_from_update = False
    supports_deleting_related_objects = False
    supports_multi_table_inheritance = False

class DatabaseClient(BaseDatabaseClient):
    pass

class DatabaseValidation(BaseDatabaseValidation):
    pass

class DatabaseIntrospection(BaseDatabaseIntrospection):
    def table_names(self):
        """
        Show defined models
        """
        return self.django_table_names()

class FakeCursor(object):
    def __getattribute__(self, name):
        raise NotImplementedError("The MongoDB backend doesn't support cursors.")

    def __setattr__(self, name, value):
        raise NotImplementedError("The MongoDB backend doesn't support cursors.")

class DatabaseWrapper(BaseDatabaseWrapper):
    def __init__(self, *args, **kwds):
        super(DatabaseWrapper, self).__init__(*args, **kwds)
        self.features = DatabaseFeatures()
        self.ops = DatabaseOperations()
        self.client = DatabaseClient(self)
        self.creation = DatabaseCreation(self)
        self.validation = DatabaseValidation(self)
        self.introspection = DatabaseIntrospection(self)

    def _cursor(self):
        if not self.connection:
            settings_dict = self.settings_dict
           
            NAME = settings_dict["NAME"]
            
            HOST = settings_dict["HOST"]
            PORT = settings_dict["PORT"]
            
            USER = settings_dict["USER"]
            PASSWORD = settings_dict["PASSWORD"]
            
            conn = Connection(HOST, PORT) 
            
            if USER and PASSWORD:
                auth = conn['admin'].authenticate(USER, PASSWORD)
                if not auth:
                    raise ImproperlyConfigured("Username and/or password for the mongoDB are not correct")
            
            db = conn[NAME]
            
            # TODO - do we need namespace injectors?
            #db.add_son_manipulator(NamespaceInjector()) # inject _ns
            #db.add_son_manipulator(AutoReference(db))
            
            self.connection = db
        return self.connection
