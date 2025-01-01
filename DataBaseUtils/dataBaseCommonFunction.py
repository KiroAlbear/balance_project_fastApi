from DataBaseUtils.dataBaseCredintials import DataBaseCredentials
import sqlalchemy
class DataBaseCommonFunctions():
    dataBaseCred = DataBaseCredentials()


    async def deleteTableFromDataBase(self, tableName):
        query = f"DROP Table '{tableName}'"
        return await self.dataBaseCred.systemDatabase.execute(query)
    
    def createTable(self,funtionToCreateTable):
        newTable = funtionToCreateTable()
        engine = sqlalchemy.create_engine(
        self.dataBaseCred.DATABASE_URL,connect_args={"check_same_thread": False}
        )
        self.dataBaseCred.metaData.create_all(engine)
        return newTable
    