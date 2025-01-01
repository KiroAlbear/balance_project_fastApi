from Models.responseModels.dataObject import DataObject
class ResponseObject():
    def __init__(self, status, message, data):
        self.status = status
        self.message = message
        self.responseObject = DataObject(data)