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

EMULATED_OPS = {
    'exact': lambda x, y: x == y,
    'iexact': lambda x, y: x.lower() == y.lower(),
    'startswith': lambda x, y: x.startswith(y),
    'istartswith': lambda x, y: x.lower().startswith(y.lower()),
    'isnull': lambda x, y: x is None if y else x is not None,
    'in': lambda x, y: x in y,
    'lt': lambda x, y: x < y,
    'lte': lambda x, y: x <= y,
    'gt': lambda x, y: x > y,
    'gte': lambda x, y: x >= y,
}

# Valid query types (a dictionary is used for speedy lookups).
OPERATORS_MAP = {
    'exact': '=',
    'gt': '>',
    'gte': '>=',
    'lt': '<',
    'lte': '<=',

    # The following operators are supported with special code below:
    'isnull': None,
    'startswith': None,

    # TODO: support these filters
    # in, range
}

NEGATION_MAP = {
    'gt': '<=',
    'gte': '<',
    'lt': '>=',
    'lte': '>',
    # TODO: support these filters
    #'exact': '!=', # this might actually become individual '<' and '>' queries
}

class SQLCompiler(SQLCompiler):
    """
    A simple query: no joins, no distinct, etc.
    """
    
    def execute_sql(self, result_type=MULTI):
        # TODO
        pass

    def results_iter(self):
        """
        Returns an iterator over the results from executing this query.
        """
        # TODO 
        pass

    def has_results(self):
        # TODO
        pass


class SQLInsertCompiler(SQLCompiler):
    # TODO
    pass

class SQLUpdateCompiler(SQLCompiler):
    # TODO 
    pass

class SQLDeleteCompiler(SQLCompiler):
    # TODO 
    pass