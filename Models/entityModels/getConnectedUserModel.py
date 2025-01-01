
from pydantic import BaseModel


class GetConnectedUserModel(BaseModel):
    provider_uui:str

