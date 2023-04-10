from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config.base_settings import get_settings


class DatabaseSessionAsync:
    """A class for an asynchronous database session.

    Attributes:
        engine (AsyncIOMotorClient): A client for MongoDB that is used to connect to the database.
    """

    def __init__(self) -> None:
        """Initialize a new instance of the DatabaseSessionAsync class."""
        self._engine = None

    @property
    def get_database(self) -> AsyncIOMotorDatabase:
        """Returns the database object.

        Raises:
            Exception: If the engine object has not been initialized.
        """
        if self._engine is None:
            raise Exception(
                "The value of the engine object is None, please execute the init method "
                "to initialize the engine object."
            )
        return self._engine.get_default_database()

    def init(self) -> None:
        """Initialize the engine object with the database configuration.

        Raises:
            Exception: If the value of the connection string in the settings module is None.
        """
        if get_settings().DATABASE_URL is None:
            raise Exception(
                "Database connection error. The value of the connection string is None, "
                "please create an environment variable named DB_CONFIG_MDB_CRABAPI to "
                "store the connection string."
            )
        if self._engine is None:
            self._engine = AsyncIOMotorClient(get_settings().DATABASE_URL)


# initialize the DatabaseSessionAsync instance
db_session = DatabaseSessionAsync()
