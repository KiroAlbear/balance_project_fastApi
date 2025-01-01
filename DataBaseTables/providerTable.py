
from ast import walk
from fastapi import HTTPException
import email
from importlib.metadata import metadata
from select import select
from typing_extensions import Self
from unicodedata import name
import databases
from fastapi import Query
import sqlalchemy
from DataBaseUtils.dataBaseCredintials import DataBaseCredentials
from DataBaseUtils.dataBaseCommonFunction import DataBaseCommonFunctions
from Models.entityModels.loginModel import LoginModel
from Models.entityModels.registerProviderModel import RegisterProviderModel
from Models.entityModels.walletRechargeOrWithdrawModel import WalletRechargeOrWithdrawModel



class ProviderTable():

    providerTableName = "providers"
    id_ColumnName = "id"
    uuid_ColumnName = "uuid"
    name_ColumnName = "name"
    email_ColumnName = "email"
    wallet_ColumnName = "wallet"
    phoneNumber_ColumnName = "phoneNumber"
    password_ColumnName = "password"

    __providerTable = 0

    __dataBaseCred = DataBaseCredentials()
    __dataBaseCommonFunctions = DataBaseCommonFunctions()

    async def deleteProviderTable(self):
        return await self.__dataBaseCommonFunctions.deleteTableFromDataBase(self.providerTableName)
         
    def createAndReturnProviderTable(self):
        self.__providerTable = self.__dataBaseCommonFunctions.createTable(self.__getProviderTable)
        return self.__providerTable
    
    
    def __getProviderTable(self):
        providerTable = sqlalchemy.Table(
        self.providerTableName,
        self.__dataBaseCred.metaData,
        sqlalchemy.Column(self.id_ColumnName,sqlalchemy.Integer,primary_key = True),
        sqlalchemy.Column(self.uuid_ColumnName,sqlalchemy.String,),
        sqlalchemy.Column(self.name_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.email_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.wallet_ColumnName,sqlalchemy.Integer),
        sqlalchemy.Column(self.phoneNumber_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.password_ColumnName,sqlalchemy.String(500)))

        return providerTable
    


    async def loginProvider(self,loginModel:LoginModel):
        
        verification_query = "SELECT * FROM {} WHERE {}='{}' and {} = '{}'".format(
            self.providerTableName,

            self.email_ColumnName,
            loginModel.email,

            self.password_ColumnName,
            loginModel.password
        )

        record = await self.__dataBaseCred.systemDatabase.fetch_one(verification_query)
        if(record != None):
            return record
        else:
            raise HTTPException(
             status_code = 400,
             detail = "Wrong email or password"
            )
         

    async def insertNewProvider(self,registerModel:RegisterProviderModel):

        query = self.__providerTable.insert().values(
        uuid = registerModel.uuid,
        name = registerModel.name,
        email = registerModel.email,
        phoneNumber = registerModel.phoneNumber,
        password = registerModel.password,
        wallet = 0
    ) 
        ###################################################################################################

        phone_verification_query = "SELECT * FROM {} WHERE {}= '{}'".format(
           self.providerTableName,

           self.phoneNumber_ColumnName,
           registerModel.phoneNumber,
        )
        phone_verification_record = await self.__dataBaseCred.systemDatabase.fetch_all(phone_verification_query)

        ###################################################################################################

        email_verification_query = "SELECT * FROM {} WHERE {}= '{}' ".format(
           self.providerTableName,

           self.email_ColumnName,
           registerModel.email,
        )
        email_verification_record = await self.__dataBaseCred.systemDatabase.fetch_all(email_verification_query)

        ###################################################################################################

        uuid_verification_query = "SELECT * FROM {} WHERE {}= '{}' ".format(
           self.providerTableName,

           self.uuid_ColumnName,
           registerModel.uuid,
        )
        uuid_verification_record = await self.__dataBaseCred.systemDatabase.fetch_all(uuid_verification_query)

        ###################################################################################################

        if(len(uuid_verification_record) > 0):
            raise HTTPException(
             status_code = 400,
             detail = "This uuid Number already exists"
            )
     
        # elif(len(phone_verification_record) > 0):
        #     raise HTTPException(
        #      status_code = 400,
        #      detail = "This Phone Number already exists"
        #     )
          
        # elif(len(email_verification_record) > 0):
        #     raise HTTPException(
        #      status_code = 400,
        #      detail = "This Email already exists"
        #     )
        else:
           provider_id = await self.__dataBaseCred.systemDatabase.execute(query)
           return await self.getProviderData(provider_id)
    


    async def getProviderData(self,provider_id):

        query = "SELECT {},{},{},{},{} FROM {} WHERE {}={}".format(
        self.id_ColumnName,
        self.name_ColumnName,
        self.email_ColumnName,
        self.wallet_ColumnName,
        self.phoneNumber_ColumnName,
        self.providerTableName,
        self.id_ColumnName,
    
        provider_id)
        row = await self.__dataBaseCred.systemDatabase.fetch_one(query)
        return {
            self.id_ColumnName:row[0],
            self.name_ColumnName:row[1],
            self.email_ColumnName:row[2],
            self.wallet_ColumnName:row[3],
            self.phoneNumber_ColumnName:row[4],
        }



    async def addToWallet(self,providerWalletModel:WalletRechargeOrWithdrawModel):
        query = "UPDATE {} SET {} = {} + {} WHERE {} = {}".format(
            self.providerTableName,

            self.wallet_ColumnName,
            self.wallet_ColumnName,
            providerWalletModel.value,
            self.id_ColumnName,
            providerWalletModel.id
            )

        await self.__dataBaseCred.systemDatabase.execute(query)
        return await self.getProviderData(providerWalletModel.id)


    async def declineFromWallet(self,providerWalletModel:WalletRechargeOrWithdrawModel):
        query = "UPDATE {} SET {} = {} - {} WHERE {} = {} and {} > 0".format(
            self.providerTableName,

            self.wallet_ColumnName,
            self.wallet_ColumnName,
            providerWalletModel.value,

            self.id_ColumnName,
            providerWalletModel.id,
            self.wallet_ColumnName
            )

        success = await self.__dataBaseCred.systemDatabase.execute(query)
        if(success == 1):
            return await self.getProviderData(providerWalletModel.id)
        else:
            raise HTTPException(
             status_code = 400,
             detail = "Insufficient funds"
            )
