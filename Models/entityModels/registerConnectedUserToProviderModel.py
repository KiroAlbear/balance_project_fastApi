from pydantic import BaseModel

class RegisterConnectedUserToProviderModel(BaseModel):
    provider_uuid: str
    user_mac_address: str
    user_ip_address: str