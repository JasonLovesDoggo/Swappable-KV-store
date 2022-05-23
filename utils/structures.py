import enum
from databases import postgresql, redis


class Databases(enum.Enum):
    """
    Enum of databases
    """
    Redis = 'redis'
    MongoDB = 'mongodb'
    PostgreSQL = 'postgresql'

