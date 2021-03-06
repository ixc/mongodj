import pymongo

from django.db.backends import BaseDatabaseFeatures, \
                               BaseDatabaseWrapper, \
                               BaseDatabaseClient, \
                               BaseDatabaseValidation, \
                               BaseDatabaseIntrospection
from django.core.exceptions import ImproperlyConfigured

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
        
class CursorWrapper():
    """
    Connection is essentially a cursor in mongoDB.
    Let's imitate the methods cursor has
    """
    def __init__(self, conn, NAME):
        self.conn = conn
        self.db_name = NAME
        self.db = conn[NAME]
        
    def commit(self, *args, **kw):
        # TODO - what is the state of 
        # transaction support in mongo?
        return True
        
    def close(self):
        # TODO
        # how to close the damn things?
        # or do we need to?
        pass
    
    def __getattr__(self, attr):
        if not attr in self.__dict__:
            return getattr(self.db, attr)
        self.__dict__[attr]
        
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
        if self.connection is None:
            settings_dict = self.settings_dict
           
            NAME = settings_dict["NAME"]
            HOST = settings_dict["HOST"]
            try:
                PORT = int(settings_dict["PORT"])
            except ValueError:
                raise ImproperlyConfigured("PORT must be an integer, or a string which is easily convertable to an integer")
            
            USER = settings_dict["USER"]
            PASSWORD = settings_dict["PASSWORD"]
            conn = pymongo.Connection(HOST, PORT) 
            
            if USER and PASSWORD:
                auth = conn['admin'].authenticate(USER, PASSWORD)
                if not auth:
                    raise ImproperlyConfigured("Username and/or password for the mongoDB are not correct")
            
            self.connection = CursorWrapper(conn, NAME)
        return self.connection
