import datetime
import sys

import pymongo

from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql import aggregates as sqlaggregates
from django.db.models.sql.constants import LOOKUP_SEP, MULTI, SINGLE
from django.db.models.sql.where import AND, OR
from django.db.utils import DatabaseError, IntegrityError
from django.utils.tree import Node

from django.conf import settings

TYPE_MAPPING = {
    "unicode":  lambda val: unicode(val),
    "int":      lambda val: int(val),
    "float":    lambda val: float(val),
}

def python2db(db_type, value):
    # TODO - error checking?
    return TYPE_MAPPING[db_type](value)
    
def db2python(db_type, value):
    return TYPE_MAPPING[db_type](value)

class SQLCompiler(SQLCompiler):
    """
    A simple query: no joins, no distinct, etc.
    
    Internal attributes of interest:
        x connection - DatabaseWrapper instance
        x query - query object, which is to be
            executed
    """
    
    def __init__(self, *args, **kw):
        super(SQLCompiler, self).__init__(*args, **kw)
        self.cursor = self.connection._cursor
    
    def execute_sql(self, result_type=MULTI):
        # TODO
        """
        Apparently this method has something to do with the aggregation
        """
        pass
    

    def results_iter(self):
        """
        Returns an iterator over the results from executing this query.
        
        self.query - the query created by the ORM
        self.query.where - conditions imposed by the query
        """
        # TODO - OR queries
        # TODO - limits
        query = {}
        
        where = self.query.where
        if where.connector == OR:
            raise NotImplementedError("OR- queries not supported yet")
        
        # testing - for now we just want this thing to work with one single child
        if len(where.children) == 0:
            res = self.cursor()[self.query.model._meta.db_table].find()
            
        else:
            child = where.children[0]
            constraint, lookup_type, annotation, value = child
            (table_alias, column, db_type), value = constraint.process(lookup_type, value, self.connection)
            # since there are no joins "table_alias" should be the same as the table name
            # TODO
            
            OPERATORS_MAP = {
                'exact':    lambda val: val,
                'gt':       lambda val: {"$gt": val},
                'gte':      lambda val: {"$gte": val},
                'lt':       lambda val: {"$lt": val},
                'lte':      lambda val: {"$lte": val},
            }
            query[column] = OPERATORS_MAP[lookup_type](python2db(db_type, value))
    
            res = self.cursor().find(query)
            
        for document in res:
            result = []
            for field in self.query.get_meta().local_fields:
                result.append(db2python(field.db_type(
                    connection=self.connection), document.get(field.column, field.default)))
            yield result
            
    def has_results(self):
        # TODO
        return True
                        
    
class SQLInsertCompiler(SQLCompiler):
    def execute_sql(self, return_id=False):
        """
        self.query - the data that should be inserted
        """
        dat = {}
        for (field, value), column in zip(self.query.values, self.query.columns):
            # TODO - prettier version?
            if column == "_id":
                continue
            dat[column] = python2db(field.db_type(connection=self.connection), value)
        self.connection._cursor()[self.query.get_meta().db_table].insert(dat)

class SQLUpdateCompiler(SQLCompiler):
    # TODO 
    pass

class SQLDeleteCompiler(SQLCompiler):
    # TODO 
    pass