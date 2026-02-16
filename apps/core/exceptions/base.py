from rest_framework.exceptions import APIException

class BaseCustomException(APIException):
    def __init__(self, error_enum):
        self.status_code = error_enum.status_code
        self.default_code = error_enum.code
        self.default_detail = error_enum.message
        super().__init__(detail=self.default_detail, code=self.default_code)