from pydantic import BaseModel


from pydantic import BaseModel
class EditProviderPackageModel(BaseModel):
    providerId:int
    packageId:int
    newPrice:int
    newSizeMB:int