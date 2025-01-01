import sqlalchemy
from DataBaseUtils.dataBaseCredintials import DataBaseCredentials
from DataBaseUtils.dataBaseCommonFunction import DataBaseCommonFunctions
from Models.entityModels.registerConnectedUserToProviderModel import (
    RegisterConnectedUserToProviderModel)
from Models.entityModels.getConnectedUserModel import GetConnectedUserModel
from Models.responseModels.responseObject import ResponseObject

class ProviderConnectedUsersTable():
    providerConnectedUsersTableName = "providerConnectedUsers"
    __providerConnectedUsersTable = 0
    __id_ColumnName = "id"
    __provider_uuid_ColumnName = "provider_uuid"
    __userMacAddress_ColumnName = "user_mac_address"
    __userIpAddress_ColumnName = "user_ip_address"
    __userExpireTimeStamp_ColumnName = "user_expire_timeStamp"

    __dataBaseCred = DataBaseCredentials()
    __dataBaseCommonFunctions = DataBaseCommonFunctions()


    async def deleteConnectedUsersTable(self):
       return await self.__dataBaseCommonFunctions.deleteTableFromDataBase(self.providerConnectedUsersTableName)

    def createAndReturnProviderConnectedUsersTable(self):
        self.__providerConnectedUsersTable = self.__dataBaseCommonFunctions.createTable(self.__createProviderConnectedUsersTable)
        return self.__providerConnectedUsersTable
    

    
    def __createProviderConnectedUsersTable(self):
        providerUsersTable = sqlalchemy.Table(
        self.providerConnectedUsersTableName,
        self.__dataBaseCred.metaData,
        sqlalchemy.Column(self.__id_ColumnName,sqlalchemy.Integer,primary_key = True),
        sqlalchemy.Column(self.__userMacAddress_ColumnName,sqlalchemy.String(50),),
        sqlalchemy.Column(self.__provider_uuid_ColumnName,sqlalchemy.String(50),),
        sqlalchemy.Column(self.__userIpAddress_ColumnName,sqlalchemy.String(50),),
        sqlalchemy.Column(self.__userExpireTimeStamp_ColumnName,sqlalchemy.Integer,),
        )

        return providerUsersTable
    
    async def insertNewConnectedUserToProvider(self,registerModel:RegisterConnectedUserToProviderModel):
        try:
            one_day:int = 86400
        
            # tomorrow_timestamp:int = int(time.time() + one_day)

            # print(f"tomorrow timestamp in seconds: {tomorrow_timestamp}")
            # print("***********asdasdasD")
            
            # await self.__dataBaseCommonFunctions.deleteTableFromDataBase(self.providerConnectedUsersTableName)
            self.createAndReturnProviderConnectedUsersTable()
            query = self.__providerConnectedUsersTable.insert().values(
            provider_uuid = registerModel.provider_uuid,
            user_mac_address = registerModel.user_mac_address,
            user_ip_address = registerModel.user_ip_address,
            user_expire_timeStamp = one_day
            ) 
    
            await self.__dataBaseCred.systemDatabase.execute(query)
            return ResponseObject(data=True,message="success",status=True)
        except:
            return ResponseObject(data=False,message="Error has occured",status=False)
         
        
    
    async def getConnectedUsersToSpecificProvider(self,getConnectedUserModel:GetConnectedUserModel):
         getConnectedUsersToProviderQuery = "SELECT * FROM {} WHERE {}= '{}'".format(
           self.providerConnectedUsersTableName,
           self.__provider_uuid_ColumnName,
           getConnectedUserModel.provider_uui,
        )
         record = await self.__dataBaseCred.systemDatabase.fetch_all(getConnectedUsersToProviderQuery)
         list_of_string_mac_address = []
         for i in record:
            list_of_string_mac_address.append(i[1])
         json = {
             "user_mac_address":list_of_string_mac_address
         }

         return ResponseObject(data=json,message="",status=True)