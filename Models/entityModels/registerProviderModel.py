
from pydantic import BaseModel


class RegisterProviderModel(BaseModel):
    uuid:str
    name:str
    email:str
    phoneNumber:str
    password:str

