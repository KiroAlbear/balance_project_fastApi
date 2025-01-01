from fastapi import HTTPException
import databases
import sqlalchemy
from DataBaseTables.providerTable import ProviderTable
from DataBaseUtils.dataBaseCredintials import DataBaseCredentials
from DataBaseUtils.dataBaseCommonFunction import DataBaseCommonFunctions
from Models.entityModels.addProviderPackageModel import AddProviderPackageModel
from Models.entityModels.editProviderPackageModel import EditProviderPackageModel
from Models.entityModels.deleteProviderPackageModel import DeleteProviderPackageModel


class ProviderPackagesTable():

    tableName = "providersPackages"
    providerTableName = ProviderTable().providerTableName
    providerTableId_ColumnName = ProviderTable().id_ColumnName


    id_ColumnName = "id"
    myProviderTableId_ColumnName = "providerId"
    price_ColumnName = "price"
    size_ColumnName = "size"
    __providerPackagesTable = 0

    __dataBaseCred = DataBaseCredentials()
    __dataBaseCommonFunctions = DataBaseCommonFunctions()

    def createAndReturnProviderTable(self):
        self.__providerPackagesTable = self.__dataBaseCommonFunctions.createTable(self.__getProviderPackagesTable)
        return self.__providerPackagesTable



    def __getProviderPackagesTable(self):
        providerPackagesTable = sqlalchemy.Table(
        self.tableName,
        self.__dataBaseCred.metaData,
        sqlalchemy.Column(self.id_ColumnName,sqlalchemy.Integer,primary_key = True),
        sqlalchemy.Column(self.myProviderTableId_ColumnName,sqlalchemy.Integer),
        sqlalchemy.Column(self.price_ColumnName,sqlalchemy.Integer),
        sqlalchemy.Column(self.size_ColumnName,sqlalchemy.Integer))

        return providerPackagesTable

    async def getProviderPackageData(self,provider_id:int):
        query = "SELECT {},{},{},{} FROM {} WHERE {}={}".format(
        self.id_ColumnName,
        self.myProviderTableId_ColumnName,
        self.price_ColumnName,
        self.size_ColumnName,
    
        self.tableName,

        self.myProviderTableId_ColumnName,
        provider_id)

        row = await self.__dataBaseCred.systemDatabase.fetch_all(query)
        packagesList = []
        for i in row:
            asd = {self.id_ColumnName:i[0],
            self.myProviderTableId_ColumnName:i[1],
            self.price_ColumnName:i[2],
            self.size_ColumnName:i[3]}

            packagesList.append(asd)
        return packagesList


    async def insertPackage(self,providerPackageModel:AddProviderPackageModel):
        providerIdExistance_verification_query = "SELECT * FROM {} WHERE {}= '{}'".format(
           self.providerTableName,

           self.providerTableId_ColumnName,
           providerPackageModel.providerId,
        )
        provider_record = await self.__dataBaseCred.systemDatabase.fetch_all(providerIdExistance_verification_query)
        provider_packages = await self.getProviderPackageData(providerPackageModel.providerId)

        if(len(provider_record) == 0): 
            raise HTTPException(
             status_code = 400,
             detail = "The provider is not exist"
            )
        elif(len(provider_packages) > 10 ):
            raise HTTPException(
             status_code = 400,
             detail = "The maximum limit of packages is reached, please edit or remove some packages"
            )
        else:
            insert_package_query = self.__providerPackagesTable.insert().values(
                providerId = providerPackageModel.providerId,
                price = providerPackageModel.price,
                size = providerPackageModel.sizeMB
            )
            package_id = await self.__dataBaseCred.systemDatabase.execute(insert_package_query)
            return await self.getProviderPackageData(providerPackageModel.providerId)

    # async def dropTable(self):
    #     query = "DROP TABLE providersPackages;"
    #     asd = await self.dataBaseCred.systemDatabase.execute(query)
    #     return asd

    async def updatePackage(self,editProviderPackageModel:EditProviderPackageModel):
        query = "UPDATE {} SET {} = {}, {} = {} WHERE {} = {}".format(
            self.tableName,

            self.price_ColumnName,
            editProviderPackageModel.newPrice,

            self.size_ColumnName,
            editProviderPackageModel.newSizeMB,

            self.id_ColumnName,
            editProviderPackageModel.packageId

            )

        success = await self.__dataBaseCred.systemDatabase.execute(query)
        if(success == 1):
            return await self.getProviderPackageData(editProviderPackageModel.providerId)
        else:
            raise HTTPException(
             status_code = 400,
             detail = "Cannot update this package"
            )

    async def deletePackage(self,deleteProviderPackageModel:DeleteProviderPackageModel):
        query = "DELETE FROM {} WHERE {} = {}".format(
            self.tableName,


            self.id_ColumnName,
            deleteProviderPackageModel.packageId

            )

        success = await self.__dataBaseCred.systemDatabase.execute(query)
        if(success == 1):
            return await self.getProviderPackageData(deleteProviderPackageModel.providerId)
        else:
            raise HTTPException(
             status_code = 400,
             detail = "Cannot delete this package"
            )