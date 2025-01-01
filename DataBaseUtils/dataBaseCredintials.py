import databases
import sqlalchemy

class DataBaseCredentials():
    DATABASE_URL = "sqlite:///./users.db"
    systemDatabase = databases.Database(DATABASE_URL)
    metaData = sqlalchemy.MetaData()
