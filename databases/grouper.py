from utils.exeptions import DatabaseNotFoundError
from utils.structures import Databases


class Database:
    def __init__(self, choice: Databases, uri: str):
        if choice not in [e.name for e in Databases]:
            raise DatabaseNotFoundError(
                f'database {choice} not doesn\'t exist plase choose one of the following: {[f"Databases.{e.name}" for e in Databases]}')
        self.uri = uri
        # ^^^ is initial config data
        self.db = self.__set_db__(choice)

    def __set_db__(self, database: str):
        match database.casefold():
            case 'mongodb':
                from databases.mongo import MongoDB
                return MongoDB(self.uri)
            case 'redis':
                from databases.redis import Redis
                return Redis(self.uri)
            case 'postgresql':
                from databases.postgresql import PostGreSQL
                return PostGreSQL(self.uri)
            case _:
                raise DatabaseNotFoundError(f'database {database} was not implemented correctly or the case wording was wrong') #don't kno why this would happen but its good to have


