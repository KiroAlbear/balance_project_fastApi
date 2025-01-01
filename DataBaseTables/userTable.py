from fastapi import HTTPException
import databases
import sqlalchemy
from DataBaseUtils.dataBaseCredintials import DataBaseCredentials
from DataBaseUtils.dataBaseCommonFunction import DataBaseCommonFunctions
from Models.entityModels.loginModel import LoginModel
from Models.entityModels.registerUserModel import RegisterUserModel
from Models.entityModels.walletRechargeOrWithdrawModel import WalletRechargeOrWithdrawModel
from Models.entityModels.deleteUserModel import DeleteUserModel


class UserTable():
    tableName = "users"
    id_ColumnName = "id"
    name_ColumnName = "name"
    wallet_ColumnName = "wallet"
    phoneNumber_ColumnName = "phoneNumber"

    __usersTable = 0

    __dataBaseCred = DataBaseCredentials()
    __dataBaseCommonFunctions = DataBaseCommonFunctions()

    def createAndReturnUserTable(self):
        self.__usersTable = self.__dataBaseCommonFunctions.createTable(self.__getUsersTable)
        return self.__usersTable

    def __getUsersTable(self):
        usersTable = sqlalchemy.Table(
        self.tableName,
        self.__dataBaseCred.metaData,
        sqlalchemy.Column(self.id_ColumnName,sqlalchemy.Integer,primary_key = True),
        sqlalchemy.Column(self.name_ColumnName,sqlalchemy.String(500)),
        sqlalchemy.Column(self.wallet_ColumnName,sqlalchemy.Integer),
        sqlalchemy.Column(self.phoneNumber_ColumnName,sqlalchemy.String(500)))
      
        return usersTable

    async def insertNewUser(self,userModel:RegisterUserModel):
        query = self.__usersTable.insert().values(
        name = userModel.name,
        phoneNumber = userModel.phoneNumber,
        wallet = 0
    )
        ###################################################################################################

        phone_verification_query = "SELECT * FROM {} WHERE {}= '{}'".format(
           self.tableName,
           self.phoneNumber_ColumnName,
           userModel.phoneNumber,
        )
        phone_verification_record = await self.__dataBaseCred.systemDatabase.fetch_all(phone_verification_query)

        if(len(phone_verification_record) > 0):
            raise HTTPException(
             status_code = 400,
             detail = "This Phone Number already exists"
            )
        
        else:
           user_id = await self.__dataBaseCred.systemDatabase.execute(query)
           return await self.getUserData(user_id)
    
    async def getAllUsers(self):
        query = self.__usersTable.select()
        allUsers = await self.__dataBaseCred.systemDatabase.fetch_all(query)
        return {
            "data":allUsers
        }
    
    async def deleteAllUsers(self):
        query = self.__usersTable.delete()
        await self.__dataBaseCred.systemDatabase.execute(query)
        return await self.getAllUsers()
    
    async def deleteOneUser(self,deleteUserModel:DeleteUserModel):
        query = "DELETE FROM {} WHERE {} = '{}'".format(
            self.tableName,
            self.phoneNumber_ColumnName,
            deleteUserModel.phoneNumber
        )
        await self.__dataBaseCred.systemDatabase.execute(query)
        return {}

    async def getUserData(self,userId):

        query = "SELECT {},{},{},{} FROM {} WHERE {}={}".format(
        self.id_ColumnName,
        self.name_ColumnName,
        self.wallet_ColumnName,
        self.phoneNumber_ColumnName,
        self.tableName,
        self.id_ColumnName,
        userId)

        row = await self.__dataBaseCred.systemDatabase.fetch_one(query)
        return {
            self.id_ColumnName:row[0],
            self.name_ColumnName:row[1],
            self.wallet_ColumnName:row[2],
            self.phoneNumber_ColumnName:row[3],
        }



    async def rechargeWallet(self,walletRechargeOrWithdrawModel:WalletRechargeOrWithdrawModel):
        query = "UPDATE {} SET {} = {} + {} WHERE {} = {}".format(
            self.tableName,

            self.wallet_ColumnName,
            self.wallet_ColumnName,
            walletRechargeOrWithdrawModel.value,
            self.id_ColumnName,
            walletRechargeOrWithdrawModel.id
            )

        await self.__dataBaseCred.systemDatabase.execute(query)
        return await self.getUserData(walletRechargeOrWithdrawModel.id)


    async def payWithWallet(self,walletRechargeOrWithdrawModel:WalletRechargeOrWithdrawModel):
        query = "UPDATE {} SET {} = {} - {} WHERE {} = {} and {} > 0".format(
            self.tableName,

            self.wallet_ColumnName,
            self.wallet_ColumnName,
            walletRechargeOrWithdrawModel.value,

            self.id_ColumnName,
            walletRechargeOrWithdrawModel.id,
            self.wallet_ColumnName
            )

        success = await self.__dataBaseCred.systemDatabase.execute(query)
        if(success == 1):
            return await self.getUserData(walletRechargeOrWithdrawModel.id)
        else:
            raise HTTPException(
             status_code = 400,
             detail = "Insufficient funds"
            )
