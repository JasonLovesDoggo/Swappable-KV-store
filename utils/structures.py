import enum


class Databases(enum.Enum):
    """
    Enum of databases
    """
    Redis = 'redis'
    MongoDB = 'mongodb'
    PostgreSQL = 'postgresql'

