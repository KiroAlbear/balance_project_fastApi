
from pydantic import BaseModel


class RegisterUserModel(BaseModel):
    name:str
    phoneNumber:str

