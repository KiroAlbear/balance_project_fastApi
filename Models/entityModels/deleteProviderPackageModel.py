from pydantic import BaseModel


from pydantic import BaseModel
class DeleteProviderPackageModel(BaseModel):
    providerId:int
    packageId:int