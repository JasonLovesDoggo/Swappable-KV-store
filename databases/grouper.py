from configparser import ConfigParser

from utils.exeptions import DatabaseNotFoundError, InvalidConfigurationError
from utils.structures import Databases

config = ConfigParser()
config.read('./config.ini')

class Database:
    def __init__(self, choice: Databases, table_name: str = 'primary'):
        self.table_name = table_name
        if choice not in [e.name for e in Databases]:
            raise DatabaseNotFoundError(
                f'database {choice} not doesn\'t exist plase choose one of the following: {[f"Databases.{e.name}" for e in Databases]}')
        if config[str(choice).casefold()]['Uri'] is None:
            raise DatabaseNotFoundError(f'database {choice} has no uri')
        else:
            self.uri = config[str(choice).casefold()]['Uri']
            self.db = self.__set_db__(choice)

    def __call__(self, *args, **kwargs):
        return self.db

    def __set_db__(self, database: str):
        # check database specific config
        if database.casefold() == 'mongodb' and not self.table_name:
            raise InvalidConfigurationError('table name is required for mongodb')

        match database.casefold():  # I want to use match, but it's not supported in any version of python < 3.10 :(
            case 'mongodb':
                from databases.mongo import MongoDB
                return MongoDB(self.uri)[self.table_name]
            case 'redis':
                from databases.redis import Redis
                return Redis(self.uri)
            case 'postgresql':
                from databases.postgresql import PostGreSQL
                return PostGreSQL(self.uri, table_name=self.table_name)
            case _:
                raise DatabaseNotFoundError(
                    f'database {database} was not implemented correctly or the case wording was wrong')  # don't kno why this would happen but its good to have
