from atexit import register
import email
from importlib.metadata import metadata
from lib2to3.pytree import Base
import re
from unicodedata import name
from fastapi import Depends, FastAPI
import databases
from imports import *;
from Models.entityModels.deleteUserModel import DeleteUserModel

# from StripePayment.stripePayments import StripePayments


# DATABASE_URL = "sqlite:///./users.db"
# usersDatabase = databases.Database(DATABASE_URL)

userTableFunctions =  UserTable()
providerTableFunctions =  ProviderTable()
providerConnectedUsersTableFunctions =  ProviderConnectedUsersTable()

providerPackagesTableFunctions =  ProviderPackagesTable()


# stripePayment = StripePayments()


userTableFunctions.createAndReturnUserTable()
providerTableFunctions.createAndReturnProviderTable()
providerPackagesTableFunctions.createAndReturnProviderTable()
providerConnectedUsersTableFunctions.createAndReturnProviderConnectedUsersTable()
# providerConnectedUsersTableFunctions.deleteConnectedUsersTable()

# metaData = sqlalchemy.MetaData()
# register = sqlalchemy.Table(
#     "register",
#     metaData,
#     sqlalchemy.Column("id",sqlalchemy.Integer,primary_key = True),
#     sqlalchemy.Column("name",sqlalchemy.String(500)),
#     sqlalchemy.Column("email",sqlalchemy.String(500)),
#     sqlalchemy.Column("wallet",sqlalchemy.Integer),
#     sqlalchemy.Column("phoneNumber",sqlalchemy.String(500)),
#     sqlalchemy.Column("password",sqlalchemy.String(500)),
# )
# engine = sqlalchemy.create_engine(
#     DATABASE_URL,connect_args={"check_same_thread": False}
# )
# metaData.create_all(engine)



app = FastAPI()


# @app.on_event("startup")
# async def connect():
#     await usersDatabase.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await usersDatabase.disconnect()

## User APIS
######################################################################################

# @app.get("/Users")
# async def getAllUsers():
#     query =  register.select()
#     allUsers = await usersDatabase.fetch_all(query)
#     return allUsers

# @app.post('/create-payment-intent')
# async def getStripeClientSecret():
#     return stripePayment.getClientSecret()

@app.post('/registerUser')
async def addUser(r:RegisterUserModel):
    return await userTableFunctions.insertNewUser(r)

@app.get('/getAllUsers')
async def getAllUsers():
    return await userTableFunctions.getAllUsers()

@app.get('/deleteAllUsers')
async def deleteUsers():
    return await userTableFunctions.deleteAllUsers()

@app.post('/deleteOneUser')
async def deleteOneUsers(r:DeleteUserModel):
    return await userTableFunctions.deleteOneUser(r)

@app.post('/addToUserWallet')
async def rechargeUserWallet(r:WalletRechargeOrWithdrawModel):
    return await userTableFunctions.rechargeWallet(r)

@app.post('/withdrawFromUserWallet')
async def pay(r:WalletRechargeOrWithdrawModel):
    return await userTableFunctions.payWithWallet(r)

## Provider APIS
######################################################################################

@app.post('/registerProvider')
async def addProvicer(r:RegisterProviderModel):
    return await providerTableFunctions.insertNewProvider(r)

@app.post('/getConnectedUsersToProvider')
async def getConnectedUsersToProvider(r:GetConnectedUserModel):
    return await providerConnectedUsersTableFunctions.getConnectedUsersToSpecificProvider(r)

@app.post('/registerConnectedUsersToProvider')
async def registerConnectedUsersToProvider(r:RegisterConnectedUserToProviderModel):
    return await providerConnectedUsersTableFunctions.insertNewConnectedUserToProvider(r)

@app.post('/deleteConnectedUsersToProviderTable')
async def deleteConnectedUsersToProviderTable():
    return await providerConnectedUsersTableFunctions.deleteConnectedUsersTable()

@app.post('/createConnectedUsersToProviderTable')
async def createConnectedUsersToProviderTable():
    return  providerConnectedUsersTableFunctions.createAndReturnProviderConnectedUsersTable()


@app.post('/loginProvider')
async def loginUser(r:LoginModel):
    return await providerTableFunctions.loginProvider(r)

@app.post('/addToProviderWallet')
async def rechargeUserWallet(r:WalletRechargeOrWithdrawModel):
    return await providerTableFunctions.addToWallet(r)

@app.post('/deleteProviderTable')
async def deleteProviderTable():
    return await providerTableFunctions.deleteProviderTable()

@app.post('/withdrawFromProviderWallet')
async def pay(r:WalletRechargeOrWithdrawModel):
    return await providerTableFunctions.declineFromWallet(r)


@app.post('/addProviderPackage')
async def addProviderPackage(r:AddProviderPackageModel):
    return await providerPackagesTableFunctions.insertPackage(r)

@app.get('/getProviderPackages/{provider_id}')
async def getProviderPackages(provider_id:int):
    return await providerPackagesTableFunctions.getProviderPackageData(provider_id)

@app.post('/updateProviderPackage')
async def updateProviderPackage(r:EditProviderPackageModel):
    return await providerPackagesTableFunctions.updatePackage(r)

@app.post('/deleteProviderPackage')
async def updateProviderPackage(r:DeleteProviderPackageModel):
    return await providerPackagesTableFunctions.deletePackage(r)


