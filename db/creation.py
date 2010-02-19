from django.db.backends.creation import BaseDatabaseCreation

class DatabaseCreation(BaseDatabaseCreation):
    # TODO - check datatypes
    data_types = {
        'DateTimeField':                'datetime',
        'DateField':                    'date',
        'TimeField':                    'time',
        'FloatField':                   'float',
        'EmailField':                   'unicode',
        'URLField':                     'unicode',
        'BooleanField':                 'bool',
        'NullBooleanField':             'bool',
        'CharField':                    'unicode',
        'CommaSeparatedIntegerField':   'unicode',
        'IPAddressField':               'unicode',
        'SlugField':                    'unicode',
        'FileField':                    'unicode',
        'FilePathField':                'unicode',
        'TextField':                    'unicode',
        'XMLField':                     'unicode',
        'IntegerField':                 'int',
        'SmallIntegerField':            'int',
        'PositiveIntegerField':         'int',
        'PositiveSmallIntegerField':    'int',
        'BigIntegerField':              'int',
        'GenericAutoField':             'objectid',
        'OneToOneField':                'int',
        'DecimalField':                 'float',
    }
    
