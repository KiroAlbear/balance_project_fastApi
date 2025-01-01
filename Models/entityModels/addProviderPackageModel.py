from pydantic import BaseModel


from pydantic import BaseModel
class AddProviderPackageModel(BaseModel):
    providerId:int
    price:int
    sizeMB:int